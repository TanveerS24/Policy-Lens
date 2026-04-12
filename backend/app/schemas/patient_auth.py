from pydantic import BaseModel, Field


class RequestOTPRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    purpose: str = Field(default="registration", description="registration, login, forgot_password, mobile_change")


class VerifyOTPRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
    purpose: str = Field(default="registration", description="registration, login, forgot_password, mobile_change")


class PatientRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: str = Field(..., description="DD/MM/YYYY format")
    gender: str = Field(..., description="Male/Female/Transgender/Prefer not to say")
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    email: str | None = Field(None)
    state_id: str = Field(...)
    district_id: str = Field(...)
    pin_code: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")


class PatientLoginRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    password: str = Field(..., min_length=1)


class ForgotPasswordRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")


class ResetPasswordRequest(BaseModel):
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class OTPResponse(BaseModel):
    success: bool
    message: str
    expires_in: int | None = None
