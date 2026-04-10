from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NotificationResponse(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    message: str
    user_id: Optional[str]
    link: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
