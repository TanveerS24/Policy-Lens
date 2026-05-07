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
import structlog

from app.config.database import get_db
from app.config.settings import get_settings
from app.models.user import User
from app.models.admin import AdminUser
from app.models.notification import OTP
from app.services.jwt_service import JWTService
from app.services.otp_service import OTPService
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = structlog.get_logger()

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
    # Check if user already exists before OTP
    logger.info("checking_existing_user_before_otp", mobile=request.mobile, email=request.email if hasattr(request, 'email') else None)
    
    # For registration, check if user exists to avoid unnecessary OTP generation
    if request.purpose == 'registration':
        existing = db.query(User).filter(
            (User.mobile == request.mobile) | 
            (User.email == request.email if hasattr(request, 'email') and request.email else False)
        ).first()
        if existing:
            logger.error("user_already_exists_before_otp", mobile=request.mobile, email=getattr(request, 'email', None))
            raise HTTPException(
                status_code=400, 
                detail="User already exists with this mobile or email. Please login or use different credentials."
            )
    
    # Generate and send OTP
    otp_code = otp_service.generate_otp()
    
    # Log OTP for development purposes
    logger.info("otp_generated", mobile=request.mobile, otp_code=otp_code, purpose=request.purpose)
    
    # Save OTP to database
    logger.info("saving_otp_to_db", mobile=request.mobile, otp_code=otp_code, purpose=request.purpose)
    
    try:
        otp_record = OTP(
            mobile=request.mobile,
            otp_code=otp_code,
            purpose=request.purpose,
            expires_at=datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
            ip_address=x_forwarded_for,
        )
        logger.info("otp_record_created", record=otp_record.__dict__)
        
        db.add(otp_record)
        logger.info("otp_added_to_session")
        
        db.commit()
        logger.info("otp_committed_to_db", record_id=otp_record.id)
        
        # Refresh to get the ID
        db.refresh(otp_record)
        logger.info("otp_refreshed", final_record=otp_record.__dict__)
        
    except Exception as e:
        logger.error("otp_save_failed", error=str(e), mobile=request.mobile)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save OTP")
    
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
    # Log incoming request data for debugging
    logger.info("register_request_start", 
                mobile=request.mobile, 
                name=request.name, 
                email=request.email,
                date_of_birth=request.date_of_birth,
                gender=request.gender,
                state=request.state,
                district=request.district,
                pin_code=request.pin_code,
                otp=request.otp,
                password_length=len(request.password) if request.password else 0
    )
    
    # Verify OTP first
    is_valid = otp_service.verify_otp(db, request.mobile, request.otp)
    if not is_valid:
        logger.error("otp_verification_failed", mobile=request.mobile)
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    logger.info("otp_verified_successfully", mobile=request.mobile)
    
    # Check if user exists
    logger.info("checking_existing_user", mobile=request.mobile, email=request.email)
    existing = db.query(User).filter(
        (User.mobile == request.mobile) | (User.email == request.email)
    ).first()
    if existing:
        logger.error("user_already_exists", mobile=request.mobile, email=request.email)
        # Instead of raising error, suggest login
        raise HTTPException(
            status_code=409, 
            detail="User already exists. Please login instead.",
            headers={"X-Error-Code": "USER_EXISTS"}
        )
    
    logger.info("creating_new_user", mobile=request.mobile)
    
    # Hash password
    try:
        hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
        logger.info("password_hashed_successfully")
    except Exception as e:
        logger.error("password_hashing_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Password processing failed")
    
    # Parse date of birth
    try:
        date_of_birth = datetime.strptime(request.date_of_birth, "%Y-%m-%d").date()
        logger.info("date_parsed_successfully", date_of_birth=str(date_of_birth))
    except Exception as e:
        logger.error("date_parsing_failed", date_of_birth=request.date_of_birth, error=str(e))
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Create user
    logger.info("starting_user_creation", data={
        "name": request.name,
        "email": request.email, 
        "mobile": request.mobile,
        "date_of_birth": str(date_of_birth),
        "gender": request.gender,
        "state": request.state,
        "district": request.district,
        "pin_code": request.pin_code
    })
    
    try:
        user = User(
            name=request.name,
            email=request.email,
            mobile=request.mobile,
            date_of_birth=date_of_birth,
            gender=request.gender,
            state=request.state,
            district=request.district,
            pin_code=request.pin_code,
            hashed_password=hashed_password,
            is_verified=True,
        )
        logger.info("user_object_created", user_object=user.__dict__)
        
        db.add(user)
        logger.info("user_added_to_session")
        
        db.commit()
        logger.info("user_committed_to_db", user_id=user.id if hasattr(user, 'id') else 'unknown')
        
        db.refresh(user)
        logger.info("user_refreshed", final_user=user.__dict__)
        
        # Double-check by querying the database
        check_user = db.query(User).filter(User.mobile == request.mobile).first()
        logger.info("user_verification_check", found=check_user is not None, user_id=check_user.id if check_user else None)
        
    except Exception as e:
        logger.error("user_creation_failed", error=str(e), rollback=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="User creation failed")
    except Exception as e:
        logger.error("user_creation_failed", error=str(e), rollback=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="User creation failed")
    
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
