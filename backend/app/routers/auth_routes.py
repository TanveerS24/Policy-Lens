"""
Authentication Routes
User registration, login, OTP verification, and token refresh
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.database.mongodb import get_db
from app.models.database_models import UserModel, UserRole
from app.schemas.schemas import (
    RegisterRequest,
    OTPVerificationRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)
from app.config.security import TokenManager, PasswordManager
from app.utils.otp_service import generate_otp, store_otp, verify_otp
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/register", response_model=dict)
async def register(request: RegisterRequest):
    """
    Register a new user
    Sends OTP to email
    """
    try:
        from app.utils.otp_service import redis_client
        
        db = get_db()
        
        # Check if user already exists
        existing_user = await db["users"].find_one({"email": request.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Generate OTP
        otp = generate_otp()
        
        # Store OTP in Redis
        otp_stored = await store_otp(request.email, otp)
        if not otp_stored:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate OTP",
            )
        
        # Store temporary user data in Redis
        import json
        temp_user_data = {
            "name": request.name,
            "email": request.email,
            "password_hash": PasswordManager.hash_password(request.password),
            "age": request.age,
            "gender": request.gender,
            "state": request.state,
        }
        
        temp_user_key = f"temp_user:{request.email}"
        await redis_client.setex(
            temp_user_key,
            settings.OTP_EXPIRY_MINUTES * 60,
            json.dumps(temp_user_data)
        )
        
        # TODO: Send OTP via email (implement email service)
        logger.info(f"OTP for {request.email}: {otp}")  # Remove in production
        
        return {
            "message": "OTP sent to email",
            "email": request.email,
            "otp_expiry_minutes": settings.OTP_EXPIRY_MINUTES,
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp_endpoint(request: OTPVerificationRequest):
    """
    Verify OTP and create user account
    Returns access and refresh tokens
    """
    try:
        from app.utils.otp_service import redis_client
        import json
        
        # Verify OTP
        otp_valid = await verify_otp(request.email, request.otp)
        if not otp_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP",
            )
        
        # Get temporary user data from Redis
        temp_user_key = f"temp_user:{request.email}"
        temp_user_data = await redis_client.get(temp_user_key)
        
        if not temp_user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration session expired, please register again",
            )
        
        user_data = json.loads(temp_user_data)
        
        db = get_db()
        
        # Create user account
        user_doc = {
            "name": user_data["name"],
            "email": user_data["email"],
            "password_hash": user_data["password_hash"],
            "age": user_data.get("age"),
            "gender": user_data.get("gender"),
            "state": user_data.get("state"),
            "role": UserRole.CLIENT,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        result = await db["users"].insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Delete temporary user data
        await redis_client.delete(temp_user_key)
        
        # Create tokens
        token_data = {
            "sub": user_id,
            "email": user_data["email"],
            "role": UserRole.CLIENT,
        }
        
        access_token = TokenManager.create_access_token(token_data)
        refresh_token = TokenManager.create_refresh_token(token_data)
        
        logger.info(f"✅ User registered and verified: {request.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            email=user_data["email"],
            role=UserRole.CLIENT,
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"OTP verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OTP verification failed",
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    User login
    Returns access and refresh tokens
    """
    try:
        db = get_db()
        
        # Find user by email
        user = await db["users"].find_one({"email": request.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        # Verify password
        if not PasswordManager.verify_password(request.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        # Check if user is active
        if not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not active",
            )
        
        # Create tokens
        user_id = str(user["_id"])
        token_data = {
            "sub": user_id,
            "email": user["email"],
            "role": user.get("role", UserRole.CLIENT),
        }
        
        access_token = TokenManager.create_access_token(token_data)
        refresh_token = TokenManager.create_refresh_token(token_data)
        
        logger.info(f"✅ User logged in: {request.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
            email=user["email"],
            role=user.get("role", UserRole.CLIENT),
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token
    """
    try:
        # Verify refresh token
        payload = TokenManager.verify_token(request.refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        
        # Get user info
        db = get_db()
        user = await db["users"].find_one({"_id": ObjectId(payload.get("sub"))})
        
        if not user or not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user",
            )
        
        # Create new access token
        token_data = {
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user.get("role", UserRole.CLIENT),
        }
        
        new_access_token = TokenManager.create_access_token(token_data)
        new_refresh_token = TokenManager.create_refresh_token(token_data)
        
        logger.info(f"✅ Token refreshed for {user['email']}")
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user_id=str(user["_id"]),
            email=user["email"],
            role=user.get("role", UserRole.CLIENT),
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed",
        )


# Import at the end to avoid circular imports
from app.config.settings import settings
