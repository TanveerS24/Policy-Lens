from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field


class DocumentStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AIStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentBase(BaseModel):
    original_name: str = Field(..., max_length=255)
    mime_type: str = Field(..., max_length=100)
    file_size: int = Field(..., ge=0)
    storage_key: str = Field(..., description="GridFS file ID")


class DocumentCreate(DocumentBase):
    pass


class DocumentInDB(DocumentBase):
    id: str = Field(..., alias="_id")
    user_id: str
    upload_status: DocumentStatusEnum = Field(default=DocumentStatusEnum.PENDING)
    ai_status: AIStatusEnum = Field(default=AIStatusEnum.PENDING)
    reprocess_count: int = Field(default=0, ge=0)
    display_name: Optional[str] = Field(None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class DocumentPublic(DocumentInDB):
    pass


class DocumentSummary(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    summary_json: Dict[str, Any] = Field(..., description="Structured summary with coverage, exclusions, etc.")
    model_version: str = Field(..., description="Ollama model version used")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class SummaryStructure(BaseModel):
    """Structure for AI-generated document summary"""
    coverage_scope: str = Field(..., description="Summary of what the policy covers")
    exclusions: List[str] = Field(default_factory=list, description="List of exclusions")
    waiting_periods: List[str] = Field(default_factory=list, description="Waiting period information")
    premium_copay: str = Field(default="", description="Premium and co-pay details")
    claim_process: List[str] = Field(default_factory=list, description="Claim process steps")
    renewal_conditions: str = Field(default="", description="Renewal conditions")
    grievance_redressal: str = Field(default="", description="Grievance redressal process")
    disclaimer: str = Field(default="This summary is AI-generated and for informational purposes only. Please refer to the original document for binding terms.")
