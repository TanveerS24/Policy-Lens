from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field


class RuleOperatorEnum(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    IN_LIST = "in_list"
    NOT_IN_LIST = "not_in_list"
    RANGE = "range"
    CONTAINS = "contains"


class RuleFieldEnum(str, Enum):
    AGE = "age"
    STATE = "state"
    GENDER = "gender"
    INCOME = "income"
    BENEFICIARY_CATEGORY = "beneficiary_category"
    DISABILITY_FLAG = "disability_flag"


class RuleCondition(BaseModel):
    field: RuleFieldEnum
    operator: RuleOperatorEnum
    value: Any
    value_end: Optional[Any] = Field(None, description="End value for range operator")


class EligibilityRuleBase(BaseModel):
    scheme_id: str = Field(..., description="Scheme ID this rule belongs to")
    rule_name: str = Field(..., max_length=200, description="Human-readable rule name")
    conditions: List[RuleCondition] = Field(..., description="List of conditions (AND logic)")
    logic: str = Field(default="AND", description="AND or OR logic for conditions")
    active: bool = Field(default=True)
    description: Optional[str] = Field(None, max_length=500, description="Rule description")


class EligibilityRuleCreate(EligibilityRuleBase):
    pass


class EligibilityRuleUpdate(EligibilityRuleBase):
    pass


class EligibilityRuleInDB(EligibilityRuleBase):
    id: str = Field(..., alias="_id")
    version: int = Field(default=1)
    created_by: str = Field(..., description="Admin user ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class EligibilityRulePublic(EligibilityRuleInDB):
    pass


class EligibilityCheckRequest(BaseModel):
    scheme_id: str
    profile: Dict[str, Any] = Field(..., description="Patient profile data for evaluation")


class EligibilityCheckResult(BaseModel):
    eligible: bool
    eligibility_status: str = Field(..., description="likely_eligible, possibly_eligible, not_eligible")
    reason: str
    missing_requirements: List[str] = []
    matched_rules: List[str] = []
    failed_rules: List[str] = []


class EligibilityCheckLog(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    scheme_id: str
    inputs: Dict[str, Any]
    result: str
    reason: str
    checked_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
