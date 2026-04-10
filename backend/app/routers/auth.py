from fastapi import APIRouter, Depends, HTTPException, status

from app.database.client import get_db
from app.schemas.auth import LoginRequest, OTPVerificationRequest, RefreshRequest, RegisterRequest, Token, UserResponse
from app.services.auth_service import auth_service
from app.utils.security import create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(request: RegisterRequest, db=Depends(get_db)):
    try:
        user_id = await auth_service.create_user(db, request.email, request.password, request.full_name)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    access_token, refresh_token = await auth_service.create_tokens(user_id)
    # Create OTP for email verification (placeholder: no email sent)
    otp = await auth_service.create_otp(request.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "otp": otp,
    }


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db=Depends(get_db)):
    user_id = await auth_service.authenticate(db, request.email, request.password)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token, refresh_token = await auth_service.create_tokens(user_id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/verify-otp")
async def verify_otp(request: OTPVerificationRequest):
    ok = await auth_service.verify_otp(request.email, request.otp)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
    return {"success": True}


@router.post("/refresh", response_model=Token)
async def refresh(request: RefreshRequest):
    user_id = await auth_service.verify_refresh_token(request.refresh_token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token, refresh_token = await auth_service.create_tokens(user_id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
