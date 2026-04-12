from datetime import datetime
from typing import Optional, Literal
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class AdminRoleEnum(str, Enum):
    SUPER_ADMIN = "super_admin"
    CONTENT_ADMIN = "content_admin"
    SUPPORT_ADMIN = "support_admin"


class AdminStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class AdminUserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: AdminRoleEnum = Field(..., description="super_admin, content_admin, support_admin")
    ip_whitelist: Optional[list[str]] = Field(None, description="List of allowed IP addresses")


class AdminUserCreate(AdminUserBase):
    password: str = Field(..., min_length=12, description="Min 12 chars, complexity enforced")
    force_password_change: bool = Field(default=True, description="Force password change on first login")


class AdminUserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[AdminRoleEnum] = None
    status: Optional[AdminStatusEnum] = None
    ip_whitelist: Optional[list[str]] = None


class AdminUserInDB(AdminUserBase):
    id: str = Field(..., alias="_id")
    hashed_password: str
    mfa_secret: Optional[str] = Field(None, description="TOTP secret for MFA")
    mfa_enabled: bool = Field(default=False)
    status: AdminStatusEnum = AdminStatusEnum.ACTIVE
    force_password_change: bool = False
    last_login: Optional[datetime] = None
    last_password_change: Optional[datetime] = None
    created_by: Optional[str] = Field(None, description="Admin user ID who created this admin")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class AdminUserPublic(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: str
    role: AdminRoleEnum
    status: AdminStatusEnum
    mfa_enabled: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
