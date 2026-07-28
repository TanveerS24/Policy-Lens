"""Authentication endpoints."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
import bcrypt
import re
import structlog

from app.config.database import get_db
from app.config.settings import get_settings
from app.models.user import User
from app.models.admin import AdminUser
from app.models.notification import OTP
from app.services.jwt_service import JWTService
from app.services.otp_service import OTPService

logger = structlog.get_logger()

router = APIRouter()
settings = get_settings()
jwt_service = JWTService()
otp_service = OTPService()
security = HTTPBearer()


# Schemas
class RequestOTPRequest(BaseModel):
    email: Optional[str] = None
    mobile: Optional[str] = None
    purpose: str = Field(default="login")  # registration, login, password_reset


class VerifyOTPRequest(BaseModel):
    email: Optional[str] = None
    mobile: Optional[str] = None
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

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
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
    """Request OTP for email (primary) or mobile (secondary) verification."""
    email = request.email.strip() if request.email and request.email.strip() else None
    mobile = request.mobile.strip() if request.mobile and request.mobile.strip() else None
    target = email or mobile

    if not target:
        raise HTTPException(status_code=400, detail="Either email or mobile number must be provided")

    # For registration, check if user exists to avoid unnecessary OTP generation
    if request.purpose == 'registration':
        from sqlalchemy import or_
        filters = []
        if email:
            filters.append(User.email == email)
        if mobile:
            filters.append(User.mobile == mobile)

        if filters:
            existing = db.query(User).filter(or_(*filters)).first()
            if existing:
                logger.warning("user_already_exists_before_otp", target=target)
                raise HTTPException(
                    status_code=400,
                    detail="User already exists with this email or mobile. Please login or use different credentials."
                )

    # Rate limiting check
    recent_count = otp_service.count_recent_requests(db, target)
    if recent_count >= settings.OTP_MAX_REQUESTS_PER_HOUR:
        raise HTTPException(
            status_code=429,
            detail="Too many OTP requests. Please try again later."
        )

    # Generate and send OTP
    otp_code = otp_service.generate_otp()

    logger.info("otp_generated", target=target, purpose=request.purpose)

    # Save OTP to database
    try:
        otp_record = OTP(
            email=email,
            mobile=mobile,
            otp_code=otp_code,
            purpose=request.purpose,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
            ip_address=x_forwarded_for,
        )

        db.add(otp_record)
        db.commit()
        db.refresh(otp_record)
    except Exception as e:
        logger.error("otp_save_failed", error=str(e), target=target)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save OTP")

    # Dispatch OTP via Email or SMS
    if email:
        otp_service.send_email_otp(email, otp_code)
    elif mobile:
        otp_service.send_sms(mobile, f"Your Policy-Lens OTP is {otp_code}")

    # Include dev_otp for local development/testing when DEBUG is enabled or SMTP is not set
    include_dev_otp = settings.DEBUG or not bool(settings.SMTP_HOST)

    return {
        "message": f"OTP sent successfully to {'email' if email else 'mobile'}",
        "expires_in_minutes": settings.OTP_EXPIRE_MINUTES,
        "dev_otp": otp_code if include_dev_otp else None
    }


@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP code."""
    email = request.email.strip() if request.email and request.email.strip() else None
    mobile = request.mobile.strip() if request.mobile and request.mobile.strip() else None
    target = email or mobile

    if not target:
        raise HTTPException(status_code=400, detail="Either email or mobile number must be provided")

    is_valid = otp_service.verify_otp(db, target, request.otp)
    if not is_valid and email:
        is_valid = otp_service.verify_otp(db, email, request.otp)
    if not is_valid and mobile:
        is_valid = otp_service.verify_otp(db, mobile, request.otp)

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    return {"verified": True, "target": target}


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new patient."""
    logger.info("register_request_start", mobile=request.mobile, email=request.email, name=request.name)

    # Verify OTP first (by email if provided, otherwise mobile)
    target = request.email or request.mobile
    is_valid = otp_service.verify_otp(db, target, request.otp)
    if not is_valid and request.mobile:
        is_valid = otp_service.verify_otp(db, request.mobile, request.otp)

    if not is_valid:
        logger.error("otp_verification_failed", target=target)
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    logger.info("otp_verified_successfully", target=target)

    # Check if user exists
    existing = db.query(User).filter(
        (User.mobile == request.mobile) | (User.email == request.email)
    ).first()
    if existing:
        logger.warning("user_already_exists", mobile=request.mobile)
        raise HTTPException(
            status_code=409,
            detail="User already exists. Please login instead.",
            headers={"X-Error-Code": "USER_EXISTS"}
        )

    # Hash password
    try:
        hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    except Exception as e:
        logger.error("password_hashing_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Password processing failed")

    # Parse date of birth
    try:
        date_of_birth = datetime.strptime(request.date_of_birth, "%Y-%m-%d").date()
    except Exception as e:
        logger.error("date_parsing_failed", date_of_birth=request.date_of_birth, error=str(e))
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Create user
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
            last_seen=datetime.now(timezone.utc),
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info("user_created_successfully", user_id=user.id)

    except Exception as e:
        logger.error("user_creation_failed", error=str(e))
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
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=423, detail="Account locked. Try again later.")

    # Verify password
    if not bcrypt.checkpw(request.password.encode(), user.hashed_password.encode()):
        # Increment failed attempts
        user.failed_login_attempts += 1

        # Lock account after max failed attempts
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)

        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Reset failed attempts and update last seen
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_seen = datetime.now(timezone.utc)
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
