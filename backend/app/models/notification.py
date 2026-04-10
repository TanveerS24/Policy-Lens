from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    title: str
    message: str
    user_id: Optional[str] = None
    link: Optional[str] = None


class NotificationInDB(NotificationBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class NotificationPublic(NotificationInDB):
    pass
