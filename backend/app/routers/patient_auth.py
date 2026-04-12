from fastapi import APIRouter, Depends, HTTPException, status, Request
from datetime import datetime

from app.database.client import get_db
from app.schemas.patient_auth import (
    ForgotPasswordRequest,
    OTPResponse,
    PatientLoginRequest,
    PatientRegisterRequest,
    RequestOTPRequest,
    ResetPasswordRequest,
    Token,
    VerifyOTPRequest,
)
from app.services.patient_auth_service import patient_auth_service

router = APIRouter(prefix="/auth", tags=["patient-auth"])


@router.post("/request-otp", response_model=OTPResponse)
async def request_otp(request: RequestOTPRequest, http_request: Request):
    """
    Request OTP for mobile number verification
    
    Purpose options: registration, login, forgot_password, mobile_change
    """
    client_ip = http_request.client.host if http_request.client else None
    device_fingerprint = http_request.headers.get("user-agent")
    
    result = await patient_auth_service.create_otp(
        mobile=request.mobile,
        purpose=request.purpose,
        ip=client_ip,
        device_fingerprint=device_fingerprint
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.post("/verify-otp", response_model=OTPResponse)
async def verify_otp(request: VerifyOTPRequest):
    """Verify OTP code for mobile number"""
    result = await patient_auth_service.verify_otp(
        mobile=request.mobile,
        otp=request.otp,
        purpose=request.purpose
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result


@router.post("/register", response_model=Token)
async def register(request: PatientRegisterRequest, db=Depends(get_db)):
    """
    Register new patient after OTP verification
    
    Flow:
    1. User requests OTP via /auth/request-otp with purpose=registration
    2. User verifies OTP via /auth/verify-otp
    3. User registers with verified mobile and OTP
    """
    # Verify OTP first
    otp_result = await patient_auth_service.verify_otp(
        mobile=request.mobile,
        otp=request.otp,
        purpose="registration"
    )
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Parse date of birth
    try:
        from datetime import datetime
        dob = datetime.strptime(request.date_of_birth, "%d/%m/%Y").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use DD/MM/YYYY"
        )
    
    # Prepare patient data
    patient_data = request.dict()
    patient_data["date_of_birth"] = dob
    patient_data.pop("confirm_password")
    patient_data.pop("otp")
    
    try:
        user_id = await patient_auth_service.create_patient(db, patient_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    
    access_token, refresh_token = await patient_auth_service.create_tokens(user_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
async def login(request: PatientLoginRequest, db=Depends(get_db)):
    """Login with mobile number and password"""
    try:
        user_id = await patient_auth_service.authenticate(db, request.mobile, request.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc)
        )
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number or password"
        )
    
    access_token, refresh_token = await patient_auth_service.create_tokens(user_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh(request: dict):
    """Refresh access token using refresh token"""
    refresh_token = request.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token required"
        )
    
    user_id = await patient_auth_service.verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    access_token, refresh_token = await patient_auth_service.create_tokens(user_id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(request: dict):
    """Logout and revoke refresh token"""
    from app.utils.security import decode_token
    
    access_token = request.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Access token required"
        )
    
    payload = decode_token(access_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("sub")
    if user_id:
        await patient_auth_service.revoke_all_sessions(user_id)
    
    return {"message": "Logged out successfully"}


@router.post("/forgotpassword")
async def forgot_password(request: ForgotPasswordRequest):
    """
    Initiate password reset flow
    
    1. User enters mobile number
    2. System sends OTP to mobile
    3. User verifies OTP and resets password
    """
    result = await patient_auth_service.create_otp(
        mobile=request.mobile,
        purpose="forgot_password"
    )
    
    if not result["success"]:
        # Don't reveal if mobile exists or not for security
        return {"message": "If the mobile number is registered, you will receive an OTP"}
    
    return {"message": "If the mobile number is registered, you will receive an OTP"}


@router.post("/resetpassword")
async def reset_password(request: ResetPasswordRequest, db=Depends(get_db)):
    """Reset password after OTP verification"""
    # Verify OTP first
    otp_result = await patient_auth_service.verify_otp(
        mobile=request.mobile,
        otp=request.otp,
        purpose="forgot_password"
    )
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Validate passwords match
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    # Find patient
    patient = await db["patients"].find_one({"mobile": request.mobile})
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Hash new password
    from app.utils.security import hash_password
    hashed_password = hash_password(request.new_password)
    
    # Update password and reset failed login attempts
    await db["patients"].update_one(
        {"_id": patient["_id"]},
        {
            "$set": {
                "hashed_password": hashed_password,
                "failed_login_attempts": 0,
                "locked_until": None,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Revoke all sessions
    await patient_auth_service.revoke_all_sessions(str(patient["_id"]))
    
    return {"message": "Password reset successfully. Please login with your new password"}
