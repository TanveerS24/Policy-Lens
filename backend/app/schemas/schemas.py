"""
API Schema Models
Request/Response validation using Pydantic
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# ============ Authentication Schemas ============

class RegisterRequest(BaseModel):
    """User registration schema"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None


class OTPVerificationRequest(BaseModel):
    """OTP verification schema"""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class LoginRequest(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


# ============ User Schemas ============

class UserResponse(BaseModel):
    """User response schema"""
    id: str = Field(..., alias="_id")
    name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    role: str
    created_at: datetime
    
    class Config:
        populate_by_name = True


class UserProfileUpdate(BaseModel):
    """User profile update schema"""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    income: Optional[int] = None


# ============ Policy Schemas ============

class PolicyResponse(BaseModel):
    """Policy response schema"""
    id: str = Field(..., alias="_id")
    title: str
    short_description: str
    summary: str
    eligibility_criteria: dict
    covered_benefits: List[str]
    important_notes: List[str]
    category: str
    state: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True


class PolicyListResponse(BaseModel):
    """Policy list response"""
    id: str = Field(..., alias="_id")
    title: str
    short_description: str
    category: str
    state: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True


class PolicyFilterRequest(BaseModel):
    """Policy filter request"""
    state: Optional[str] = None
    category: Optional[str] = None
    health_type: Optional[str] = None
    age_group: Optional[str] = None
    search: Optional[str] = None
    skip: int = 0
    limit: int = 10


# ============ Eligibility Check Schemas ============

class EligibilityCheckForMe(BaseModel):
    """Check eligibility for current user"""
    policy_id: str


class EligibilityCheckForOther(BaseModel):
    """Check eligibility for another person"""
    policy_id: str
    age: int
    gender: str
    state: str
    income: int


class EligibilityResponse(BaseModel):
    """Eligibility check response"""
    eligible: bool
    reason: str
    missing_requirements: List[str] = []
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)


# ============ Policy Q&A Schemas ============

class PolicyQuestionRequest(BaseModel):
    """Ask question about policy"""
    policy_id: str
    question: str = Field(..., min_length=5, max_length=500)


class PolicyQuestionResponse(BaseModel):
    """Policy question response"""
    question: str
    answer: str
    confidence_score: float = Field(0.0, ge=0.0, le=1.0)


# ============ Upload Schemas ============

class UploadStatusEnum(str, Enum):
    """Upload status enum"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class UploadResponse(BaseModel):
    """Upload response schema"""
    id: str = Field(..., alias="_id")
    pdf_filename: str
    status: UploadStatusEnum
    summary: Optional[str] = None
    eligibility: Optional[dict] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True


class UploadListResponse(BaseModel):
    """List of uploads"""
    uploads: List[UploadResponse]
    total: int


class PublishUploadRequest(BaseModel):
    """Request to publish upload"""
    upload_id: str
    title: str = Field(..., min_length=5, max_length=200)
    short_description: str = Field(..., min_length=10, max_length=500)
    category: str
    state: Optional[str] = None


# ============ Admin Schemas ============

class CreatePolicyRequest(BaseModel):
    """Create policy request (admin)"""
    title: str = Field(..., min_length=5, max_length=200)
    short_description: str = Field(..., min_length=10, max_length=500)
    summary: str = Field(..., min_length=20)
    eligibility_criteria: dict
    covered_benefits: List[str] = []
    important_notes: List[str] = []
    category: str
    state: Optional[str] = None


class UpdatePolicyRequest(BaseModel):
    """Update policy request (admin)"""
    title: Optional[str] = None
    short_description: Optional[str] = None
    summary: Optional[str] = None
    eligibility_criteria: Optional[dict] = None
    covered_benefits: Optional[List[str]] = None
    important_notes: Optional[List[str]] = None
    category: Optional[str] = None
    state: Optional[str] = None


class ApproveUploadRequest(BaseModel):
    """Approve upload request"""
    upload_id: str
    category: str
    state: Optional[str] = None


class RejectUploadRequest(BaseModel):
    """Reject upload request"""
    upload_id: str
    reason: str


class PendingUploadsResponse(BaseModel):
    """Pending uploads response"""
    uploads: List[UploadResponse]
    total: int


# ============ Notification Schemas ============

class NotificationResponse(BaseModel):
    """Notification response schema"""
    id: str = Field(..., alias="_id")
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        populate_by_name = True
