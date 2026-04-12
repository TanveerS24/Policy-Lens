from datetime import datetime
from typing import Optional, Literal
from enum import Enum

from pydantic import BaseModel, Field


class NotificationTypeEnum(str, Enum):
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class NotificationStatusEnum(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"


class NotificationBase(BaseModel):
    title: str = Field(..., max_length=200)
    message: str = Field(..., max_length=1000)
    user_id: Optional[str] = None
    notification_type: NotificationTypeEnum = Field(default=NotificationTypeEnum.IN_APP)
    link: Optional[str] = Field(None, max_length=500)
    data: Optional[dict] = Field(default=None, description="Additional data for push notifications")


class NotificationCreate(NotificationBase):
    pass


class NotificationInDB(NotificationBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)
    read_at: Optional[datetime] = None
    status: NotificationStatusEnum = Field(default=NotificationStatusEnum.PENDING)
    sent_at: Optional[datetime] = None
    delivery_attempts: int = Field(default=0, ge=0)
    error_message: Optional[str] = Field(None, max_length=500)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class NotificationPublic(NotificationInDB):
    pass


class NotificationPreference(BaseModel):
    user_id: str
    sms_enabled: bool = Field(default=True)
    push_enabled: bool = Field(default=True)
    in_app_enabled: bool = Field(default=True)
    eligibility_updates: bool = Field(default=True)
    scheme_updates: bool = Field(default=True)
    document_updates: bool = Field(default=True)

