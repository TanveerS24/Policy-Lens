from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DistrictBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    state_id: str = Field(..., description="Foreign key to State")
    std_code: Optional[str] = Field(None, max_length=10)
    pin_code_range: Optional[str] = Field(None, max_length=50, description="e.g., '110001-110099'")


class DistrictCreate(DistrictBase):
    pass


class DistrictInDB(DistrictBase):
    id: str = Field(..., alias="_id")
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class DistrictPublic(DistrictInDB):
    pass
