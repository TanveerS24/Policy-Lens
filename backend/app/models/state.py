from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=10)
    capital: str = Field(..., min_length=2, max_length=100)
    zone: str = Field(..., description="North/South/East/West/Central/Northeast")


class StateCreate(StateBase):
    pass


class StateInDB(StateBase):
    id: str = Field(..., alias="_id")
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class StatePublic(StateInDB):
    pass
