from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DentalServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=20, unique=True)
    category: str = Field(..., description="Preventive/Restorative/Surgical/Cosmetic")


class DentalServiceCreate(DentalServiceBase):
    pass


class DentalServiceInDB(DentalServiceBase):
    id: str = Field(..., alias="_id")
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class DentalServicePublic(DentalServiceInDB):
    pass
