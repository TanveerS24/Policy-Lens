from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.policy import EligibilityResult, PolicyPublic


class PolicyListResponse(BaseModel):
    total: int
    items: List[PolicyPublic]


class PolicyCreateRequest(BaseModel):
    title: str
    short_description: Optional[str]
    category: Optional[str]
    state: Optional[str]
    pdf_url: Optional[str]


class EligibilityCheckRequest(BaseModel):
    policy_id: str
    profile: dict
    for_someone_else: bool = False


class AskRequest(BaseModel):
    policy_id: str
    question: str


class PolicySummaryResponse(BaseModel):
    title: str
    short_description: Optional[str]
    summary: Optional[str]
    eligibility_criteria: Optional[str]
    benefits: Optional[str]
    notes: Optional[str]


class EligibilityResponse(BaseModel):
    eligible: bool
    reason: str
    missing_requirements: List[str] = []


class AskResponse(BaseModel):
    answer: str
