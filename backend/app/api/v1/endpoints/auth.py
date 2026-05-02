"""Authentication endpoints."""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
import bcrypt
import re
import random

from app.config.database import get_db
from app.config.settings import get_settings
from app.models.user import User
from app.models.admin import AdminUser
from app.models.notification import OTP
from app.services.jwt_service import JWTService
from app.services.otp_service import OTPService

router = APIRouter()
settings = get_settings()
jwt_service = JWTService()
otp_service = OTPService()
security = HTTPBearer()


# Schemas
class RequestOTPRequest(BaseModel):
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$')
    purpose: str = Field(default="login")  # registration, login, password_reset


class VerifyOTPRequest(BaseModel):
    mobile: str
    otp: str = Field(..., min_length=6, max_length=6)


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: Optional[str] = None
    mobile: str = Field(..., pattern=r'^[6-9]\d{9}$')
    date_of_birth: str
    gender: str = Field(..., pattern=r'^(male|female|other)$')
    state: str
    district: str
    pin_code: str = Field(..., pattern=r'^\d{6}$')
    password: str = Field(..., min_length=8)
    otp: str
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class LoginRequest(BaseModel):
    mobile_or_email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


# Endpoints
@router.post("/request-otp")
async def request_otp(
    request: RequestOTPRequest,
    db: Session = Depends(get_db),
    x_forwarded_for: Optional[str] = Header(None)
):
    """Request OTP for mobile verification."""
    # Check rate limits
    recent_requests = otp_service.count_recent_requests(db, request.mobile)
    if recent_requests >= settings.OTP_MAX_REQUESTS_PER_HOUR:
        raise HTTPException(status_code=429, detail="Too many OTP requests. Please try again later.")
    
    # Generate and send OTP
    otp_code = otp_service.generate_otp()
    
    # Save OTP to database
    otp_record = OTP(
        mobile=request.mobile,
        otp_code=otp_code,
        purpose=request.purpose,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        ip_address=x_forwarded_for,
    )
    db.add(otp_record)
    db.commit()
    
    # TODO: Send actual SMS
    # For development, return OTP in response
    return {
        "message": "OTP sent successfully",
        "expires_in_minutes": settings.OTP_EXPIRE_MINUTES,
        "dev_otp": otp_code if settings.DEBUG else None
    }


@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP code."""
    is_valid = otp_service.verify_otp(db, request.mobile, request.otp)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    return {"verified": True, "mobile": request.mobile}


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new patient."""
    # Verify OTP first
    is_valid = otp_service.verify_otp(db, request.mobile, request.otp)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Check if user exists
    existing = db.query(User).filter(
        (User.mobile == request.mobile) | (User.email == request.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists with this mobile or email")
    
    # Hash password
    hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    
    # Create user
    user = User(
        name=request.name,
        email=request.email,
        mobile=request.mobile,
        date_of_birth=datetime.strptime(request.date_of_birth, "%Y-%m-%d").date(),
        gender=request.gender,
        state=request.state,
        district=request.district,
        pin_code=request.pin_code,
        hashed_password=hashed_password,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generate tokens
    access_token, refresh_token = jwt_service.create_tokens(user.id, "patient")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": user.id,
            "name": user.name,
            "mobile": user.mobile,
            "email": user.email,
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login with mobile/email and password."""
    # Find user
    user = db.query(User).filter(
        (User.mobile == request.mobile_or_email) | (User.email == request.mobile_or_email)
    ).first()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check lockout
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(status_code=423, detail="Account locked. Try again later.")
    
    # Verify password
    if not bcrypt.checkpw(request.password.encode(), user.hashed_password.encode()):
        # Increment failed attempts
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            user.locked_until = datetime.utcnow() + timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
        
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Reset failed attempts
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()
    
    # Generate tokens
    access_token, refresh_token = jwt_service.create_tokens(user.id, "patient")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": user.id,
            "name": user.name,
            "mobile": user.mobile,
            "email": user.email,
        }
    }


@router.post("/refresh")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    token = credentials.credentials
    
    # Verify refresh token
    payload = jwt_service.verify_token(token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Generate new tokens
    access_token, refresh_token = jwt_service.create_tokens(user.id, "patient")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user (client should discard tokens)."""
    # In a more complex system, you might blacklist tokens here
    return {"message": "Logged out successfully"}
