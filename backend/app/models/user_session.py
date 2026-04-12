from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserSessionBase(BaseModel):
    user_id: str
    token_hash: str = Field(..., description="Hashed access token")
    device_type: Optional[str] = Field(None, max_length=50, description="iOS/Android/Web")
    device_info: Optional[str] = Field(None, max_length=500, description="User agent string")
    ip_address: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)


class UserSessionInDB(UserSessionBase):
    id: str = Field(..., alias="_id")
    refresh_token_hash: str = Field(..., description="Hashed refresh token")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    revoked: bool = False
    revoked_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class UserSessionPublic(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    device_type: Optional[str]
    ip_address: Optional[str]
    location: Optional[str]
    created_at: datetime
    expires_at: datetime
    revoked: bool
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
