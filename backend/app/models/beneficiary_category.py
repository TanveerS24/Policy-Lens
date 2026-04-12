from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BeneficiaryCategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=2, max_length=20, unique=True)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=50, description="Icon identifier")


class BeneficiaryCategoryCreate(BeneficiaryCategoryBase):
    pass


class BeneficiaryCategoryInDB(BeneficiaryCategoryBase):
    id: str = Field(..., alias="_id")
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class BeneficiaryCategoryPublic(BeneficiaryCategoryInDB):
    pass
