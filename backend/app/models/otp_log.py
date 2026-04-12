from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class OTPTaskEnum(str):
    REGISTRATION = "registration"
    LOGIN = "login"
    FORGOT_PASSWORD = "forgot_password"
    MOBILE_CHANGE = "mobile_change"
    EMAIL_VERIFICATION = "email_verification"


class OTPStatusEnum(str):
    PENDING = "pending"
    VERIFIED = "verified"
    EXPIRED = "expired"
    FAILED = "failed"


class OTPLogBase(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    otp_hash: str = Field(..., description="Hashed OTP for security")
    purpose: str = Field(..., description="Purpose of OTP: registration, login, forgot_password, etc.")
    attempt_count: int = Field(default=0, ge=0, description="Number of verification attempts")
    status: str = Field(default="pending", description="pending, verified, expired, failed")
    ip_address: Optional[str] = Field(None, max_length=50)
    device_fingerprint: Optional[str] = Field(None, max_length=100)


class OTPLogInDB(OTPLogBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    verified_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class OTPLogPublic(BaseModel):
    id: str = Field(..., alias="_id")
    mobile: str
    purpose: str
    status: str
    created_at: datetime
    expires_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
