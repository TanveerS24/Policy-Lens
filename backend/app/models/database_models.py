"""
MongoDB Data Models
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId


class UserRole(str, Enum):
    """User roles"""
    ADMIN = "admin"
    CLIENT = "client"


class UserModel(BaseModel):
    """User database model"""
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: str
    password_hash: str
    age: Optional[int] = None
    gender: Optional[str] = None  # Male, Female, Other
    state: Optional[str] = None
    income: Optional[int] = None
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class PolicyModel(BaseModel):
    """Policy database model"""
    id: Optional[str] = Field(None, alias="_id")
    title: str
    short_description: str
    summary: str
    eligibility_criteria: dict
    covered_benefits: List[str] = []
    important_notes: List[str] = []
    category: str  # Health type
    state: Optional[str] = None
    created_by: str  # User ID
    embeddings: Optional[List[float]] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class UploadStatus(str, Enum):
    """Upload status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class UploadModel(BaseModel):
    """Policy upload request model"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    pdf_path: str
    pdf_filename: str
    summary: Optional[str] = None
    eligibility: Optional[dict] = None
    status: UploadStatus = UploadStatus.PENDING
    rejection_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class NotificationModel(BaseModel):
    """Notification model"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: Optional[str] = None  # None means broadcast to all
    title: str
    message: str
    type: str  # policy_approved, new_policy, rejection, etc.
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
