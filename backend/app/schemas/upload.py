from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    id: str = Field(..., alias="_id")
    filename: str
    content_type: Optional[str]
    size: Optional[int]
    owner_id: str
    policy_id: Optional[str]
    status: str
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class PublishRequest(BaseModel):
    upload_id: str
