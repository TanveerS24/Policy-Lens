from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UploadBase(BaseModel):
    filename: str
    content_type: Optional[str]
    size: Optional[int]


class UploadInDB(UploadBase):
    id: str = Field(..., alias="_id")
    owner_id: str
    policy_id: Optional[str]
    status: str = "pending"  # pending, approved, rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class UploadPublic(UploadInDB):
    pass
