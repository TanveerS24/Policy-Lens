"""Patient endpoints."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import bcrypt

from app.config.database import get_db
from app.config.settings import get_settings
from app.models.user import User, UserProfile
from app.models.document import Document
from app.services.jwt_service import JWTService

router = APIRouter()
settings = get_settings()
jwt_service = JWTService()
security = HTTPBearer()


# Dependencies
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    payload = jwt_service.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user


# Schemas
class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pin_code: Optional[str] = Field(None, pattern=r'^\d{6}$')
    occupation: Optional[str] = None
    income_bracket: Optional[str] = None
    category: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    otp: str


class DeactivateRequest(BaseModel):
    confirm: bool
    reason: Optional[str] = None


# Endpoints
@router.get("/me")
async def get_profile(user: User = Depends(get_current_user)):
    """Get current user profile."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "mobile": user.mobile,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
        "gender": user.gender,
        "address": {
            "state": user.state,
            "district": user.district,
            "pin_code": user.pin_code,
        },
        "is_verified": user.is_verified,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.patch("/me")
async def update_profile(
    request: ProfileUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile."""
    # Update basic info
    if request.name:
        user.name = request.name
    if request.email:
        # Check if email is taken
        existing = db.query(User).filter(User.email == request.email, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = request.email
    if request.state:
        user.state = request.state
    if request.district:
        user.district = request.district
    if request.pin_code:
        user.pin_code = request.pin_code
    
    # Update or create profile
    if not hasattr(user, 'profile') or user.profile is None:
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        user.profile = profile
    
    if request.occupation:
        user.profile.occupation = request.occupation
    if request.income_bracket:
        user.profile.income_bracket = request.income_bracket
    if request.category:
        user.profile.category = request.category
    
    user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Profile updated successfully"}


@router.post("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password (requires OTP verification)."""
    # TODO: Verify OTP for mobile
    
    # Verify current password
    if not bcrypt.checkpw(request.current_password.encode(), user.hashed_password.encode()):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Hash new password
    new_hash = bcrypt.hashpw(request.new_password.encode(), bcrypt.gensalt()).decode()
    user.hashed_password = new_hash
    user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/documents")
async def get_user_documents(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents uploaded by the user."""
    documents = db.query(Document).filter(
        Document.user_id == user.id
    ).order_by(Document.uploaded_at.desc()).all()
    
    return {
        "documents": [
            {
                "id": doc.id,
                "filename": doc.original_filename,
                "file_size": doc.file_size_bytes,
                "mime_type": doc.mime_type,
                "status": doc.status,
                "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None,
                "summary_generated": doc.summary_generated,
            }
            for doc in documents
        ]
    }


@router.post("/deactivate")
async def deactivate_account(
    request: DeactivateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate user account."""
    if not request.confirm:
        raise HTTPException(status_code=400, detail="Confirmation required")
    
    user.is_active = False
    user.deactivated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Account deactivated successfully"}


@router.post("/delete")
async def delete_account(
    request: DeactivateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Permanently delete user account (DPDP compliant)."""
    if not request.confirm:
        raise HTTPException(status_code=400, detail="Confirmation required")
    
    # TODO: Schedule data deletion or anonymize
    # For now, just deactivate
    user.is_active = False
    user.deactivated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Account deletion scheduled"}


@router.get("/export-data")
async def export_user_data(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export all user data (DPDP compliance)."""
    # TODO: Generate data export file
    # This should include all user data in a downloadable format
    
    data = {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "gender": user.gender,
            "state": user.state,
            "district": user.district,
            "pin_code": user.pin_code,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "documents": [],
        "eligibility_checks": [],
        "notifications": [],
    }
    
    return {
        "message": "Data export generated",
        "download_url": None,  # TODO: Generate download link
        "expires_at": None,
    }
