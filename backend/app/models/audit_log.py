from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class AuditLogBase(BaseModel):
    actor_type: str = Field(..., description="patient, admin, system")
    actor_id: str = Field(..., description="User ID or system identifier")
    action: str = Field(..., description="Action performed (create, update, delete, etc.)")
    entity_type: str = Field(..., description="Entity type (scheme, patient, document, etc.)")
    entity_id: Optional[str] = Field(None, description="Entity ID if applicable")
    before_json: Optional[Dict[str, Any]] = Field(None, description="State before change")
    after_json: Optional[Dict[str, Any]] = Field(None, description="State after change")
    ip_address: Optional[str] = Field(None, max_length=50)
    user_agent: Optional[str] = Field(None, max_length=500)


class AuditLogInDB(AuditLogBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class AuditLogPublic(AuditLogInDB):
    pass
