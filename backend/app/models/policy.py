from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class PolicyBase(BaseModel):
    title: str
    short_description: Optional[str]
    summary: Optional[str]
    eligibility_criteria: Optional[str]
    benefits: Optional[str]
    notes: Optional[str]
    category: Optional[str]
    state: Optional[str]


class PolicyCreate(PolicyBase):
    pdf_url: Optional[str]


class PolicyInDB(PolicyBase):
    id: str = Field(..., alias="_id")
    pdf_url: Optional[str]
    approved: bool = False
    published_at: Optional[datetime]
    created_by: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict[str, Any]] = None

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class PolicyPublic(PolicyInDB):
    pass


class PolicySummary(BaseModel):
    title: str
    short_description: Optional[str]
    summary: Optional[str]
    eligibility_criteria: Optional[str]
    benefits: Optional[str]
    notes: Optional[str]


class EligibilityResult(BaseModel):
    eligible: bool
    reason: str
    missing_requirements: List[str] = []
