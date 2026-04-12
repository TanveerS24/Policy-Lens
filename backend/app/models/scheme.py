from datetime import datetime, date
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl, validator


class SchemeTypeEnum(str, Enum):
    NATIONAL = "national"
    STATE = "state"


class SchemeStatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class SchemeBase(BaseModel):
    scheme_name: str = Field(..., min_length=3, max_length=200, description="3-200 chars, unique per state")
    scheme_type: SchemeTypeEnum = Field(..., description="national or state")
    state_id: Optional[str] = Field(None, description="State ID, null for national schemes")
    sponsoring_ministry: str = Field(..., max_length=200, description="Sponsoring Ministry/Department")
    launch_date: date = Field(..., description="Cannot be future date")
    active_status: SchemeStatusEnum = Field(default=SchemeStatusEnum.ACTIVE)
    short_description: str = Field(..., min_length=50, max_length=500, description="50-500 chars")
    detailed_description: str = Field(..., max_length=5000, description="Rich text, max 5000 chars")
    eligibility_criteria: str = Field(..., max_length=3000, description="Rich text, max 3000 chars")
    beneficiary_categories: List[str] = Field(..., description="Multi-select tags from beneficiary_categories master")
    income_ceiling: Optional[int] = Field(None, ge=0, description="INR/year, 0 = no limit")
    age_min: Optional[int] = Field(None, ge=0, le=120)
    age_max: Optional[int] = Field(None, ge=0, le=120)
    services_covered: List[str] = Field(..., description="Multi-select tags from dental_services master")
    coverage_amount: Optional[int] = Field(None, ge=0, description="INR, 0 = fully free")
    enrolment_process: str = Field(..., max_length=2000, description="Rich text, max 2000 chars")
    required_documents: List[str] = Field(..., max_items=20, description="List of required documents")
    helpline_number: Optional[str] = Field(None, pattern=r"^(\d{10}|1800\d{6,7})$", description="10-digit or 1800 format")
    official_website_url: Optional[HttpUrl] = Field(None, description="HTTPS preferred")
    reference_order: Optional[str] = Field(None, max_length=100, description="Government order reference")
    
    @validator('launch_date')
    def validate_launch_date(cls, v):
        if v > date.today():
            raise ValueError('Launch date cannot be in the future')
        return v
    
    @validator('age_max')
    def validate_age_range(cls, v, values):
        if 'age_min' in values and values['age_min'] is not None and v is not None:
            if v < values['age_min']:
                raise ValueError('age_max must be greater than or equal to age_min')
        return v
    
    @validator('state_id')
    def validate_state_id(cls, v, values):
        if values.get('scheme_type') == SchemeTypeEnum.STATE and not v:
            raise ValueError('state_id is required for state schemes')
        if values.get('scheme_type') == SchemeTypeEnum.NATIONAL and v:
            raise ValueError('state_id should be null for national schemes')
        return v


class SchemeCreate(SchemeBase):
    pass


class SchemeUpdate(BaseModel):
    scheme_name: Optional[str] = Field(None, min_length=3, max_length=200)
    scheme_type: Optional[SchemeTypeEnum] = None
    state_id: Optional[str] = None
    sponsoring_ministry: Optional[str] = Field(None, max_length=200)
    launch_date: Optional[date] = None
    active_status: Optional[SchemeStatusEnum] = None
    short_description: Optional[str] = Field(None, min_length=50, max_length=500)
    detailed_description: Optional[str] = Field(None, max_length=5000)
    eligibility_criteria: Optional[str] = Field(None, max_length=3000)
    beneficiary_categories: Optional[List[str]] = None
    income_ceiling: Optional[int] = Field(None, ge=0)
    age_min: Optional[int] = Field(None, ge=0, le=120)
    age_max: Optional[int] = Field(None, ge=0, le=120)
    services_covered: Optional[List[str]] = None
    coverage_amount: Optional[int] = Field(None, ge=0)
    enrolment_process: Optional[str] = Field(None, max_length=2000)
    required_documents: Optional[List[str]] = Field(None, max_items=20)
    helpline_number: Optional[str] = Field(None, pattern=r"^(\d{10}|1800\d{6,7})$")
    official_website_url: Optional[HttpUrl] = None
    reference_order: Optional[str] = Field(None, max_length=100)


class SchemeInDB(SchemeBase):
    id: str = Field(..., alias="_id")
    version: int = Field(default=1, description="Version number for change tracking")
    last_updated_by: Optional[str] = Field(None, description="Admin user ID")
    last_updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat(), date: lambda v: v.isoformat()}


class SchemePublic(SchemeInDB):
    pass


class SchemeVersion(BaseModel):
    id: str = Field(..., alias="_id")
    scheme_id: str
    version_number: int
    snapshot: dict = Field(..., description="Full scheme data snapshot")
    changed_by: str = Field(..., description="Admin user ID")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    change_reason: Optional[str] = Field(None, max_length=500)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
