from datetime import datetime, date
from typing import Optional, Literal
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, validator


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    TRANSGENDER = "Transgender"
    PREFER_NOT_TO_SAY = "Prefer not to say"


class AccountStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEACTIVATED = "deactivated"
    DELETED = "deleted"


class PatientBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100, description="2-100 chars, alphabets and spaces only")
    date_of_birth: date = Field(..., description="Must be in past, age 0-120")
    gender: GenderEnum = Field(..., description="Male/Female/Transgender/Prefer not to say")
    mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$", description="10 digits, must start with 6-9")
    email: Optional[EmailStr] = Field(None, description="Optional email address")
    state_id: str = Field(..., description="Foreign key to State")
    district_id: str = Field(..., description="Foreign key to District")
    pin_code: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$", description="6 digits")
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if not v.replace(' ', '').isalpha():
            raise ValueError('Full name must contain only alphabets and spaces')
        if v != v.strip():
            raise ValueError('Full name cannot have leading/trailing spaces')
        return v
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        age = (date.today() - v).days // 365
        if age < 0 or age > 120:
            raise ValueError('Age must be between 0 and 120')
        return v


class PatientCreate(PatientBase):
    password: str = Field(..., min_length=8, description="Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char")
    confirm_password: str = Field(..., description="Must match password")
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    state_id: Optional[str] = None
    district_id: Optional[str] = None
    pin_code: Optional[str] = Field(None, min_length=6, max_length=6, pattern=r"^\d{6}$")
    profile_photo_url: Optional[str] = Field(None, max_length=500)
    notification_sms: Optional[bool] = True
    notification_push: Optional[bool] = True
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if v is not None:
            if not v.replace(' ', '').isalpha():
                raise ValueError('Full name must contain only alphabets and spaces')
            if v != v.strip():
                raise ValueError('Full name cannot have leading/trailing spaces')
        return v


class MobileUpdate(BaseModel):
    new_mobile: str = Field(..., min_length=10, max_length=10, pattern=r"^[6-9]\d{9}$")
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")


class PasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=1)
    
    @validator('new_password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class PatientInDB(PatientBase):
    id: str = Field(..., alias="_id")
    hashed_password: str
    mobile_verified: bool = False
    email_verified: bool = False
    profile_photo_url: Optional[str] = None
    notification_sms: bool = True
    notification_push: bool = True
    status: AccountStatusEnum = AccountStatusEnum.ACTIVE
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    deactivated_at: Optional[datetime] = None
    deletion_requested_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat(), date: lambda v: v.isoformat()}


class PatientPublic(BaseModel):
    id: str = Field(..., alias="_id")
    full_name: str
    date_of_birth: date
    gender: GenderEnum
    mobile: str
    email: Optional[str] = None
    state_id: str
    district_id: str
    pin_code: str
    profile_photo_url: Optional[str] = None
    notification_sms: bool
    notification_push: bool
    status: AccountStatusEnum
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat(), date: lambda v: v.isoformat()}
