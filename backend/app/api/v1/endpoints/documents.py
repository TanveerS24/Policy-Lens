"""Document upload and AI summary endpoints."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import uuid

from app.config.database import get_db
from app.config.settings import get_settings
from app.models.document import Document, AISummary, DocumentStatus
from app.models.user import User
from app.api.v1.endpoints.patients import get_current_user

router = APIRouter()
settings = get_settings()
security = HTTPBearer()


# Schemas
class DocumentUploadResponse(BaseModel):
    id: int
    filename: str
    status: str
    message: str


class AISummaryResponse(BaseModel):
    id: int
    document_id: int
    coverage_summary: Optional[str]
    exclusions: Optional[str]
    waiting_period: Optional[str]
    claims_process: Optional[str]
    renewal_conditions: Optional[str]
    coverage_details: dict
    exclusions_list: list
    processing_time_seconds: Optional[int]
    confidence_score: Optional[int]
    created_at: str


# Helper functions
def validate_file_type(file: UploadFile) -> bool:
    """Validate file type against allowed types."""
    allowed_types = settings.ALLOWED_FILE_TYPES
    content_type = file.content_type
    return content_type in allowed_types


def generate_filename(original_filename: str) -> str:
    """Generate unique filename for storage."""
    ext = os.path.splitext(original_filename)[1].lower()
    return f"{uuid.uuid4()}{ext}"


def scan_file_for_viruses(file_path: str) -> str:
    """Scan file for viruses (placeholder)."""
    # TODO: Integrate with virus scanning service (ClamAV, etc.)
    return "clean"


async def process_document_with_ai(document_id: int, db: Session):
    """Process document with AI to generate summary."""
    # This would be a background task
    # TODO: Integrate with Claude/OpenAI API
    pass


# Endpoints
@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a policy document."""
    # Validate file type
    if not validate_file_type(file):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    # Check file size (read first chunk to check)
    contents = await file.read()
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    
    # Reset file position
    await file.seek(0)
    
    # Generate unique filename
    stored_filename = generate_filename(file.filename)
    storage_path = f"uploads/{user.id}/{stored_filename}"
    
    # TODO: Upload to S3/cloud storage
    # For now, save to local storage
    os.makedirs(f"uploads/{user.id}", exist_ok=True)
    file_path = f"uploads/{user.id}/{stored_filename}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Scan for viruses
    virus_result = scan_file_for_viruses(file_path)
    
    # Create document record
    document = Document(
        user_id=user.id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_size_bytes=len(contents),
        mime_type=file.content_type or "application/octet-stream",
        storage_path=storage_path,
        status=DocumentStatus.PENDING.value,
        virus_scan_result=virus_result,
    )
    
    if virus_result != "clean":
        document.status = DocumentStatus.QUARANTINED.value
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # If clean, trigger AI processing in background
    if virus_result == "clean":
        document.status = DocumentStatus.PROCESSING.value
        db.commit()
        # background_tasks.add_task(process_document_with_ai, document.id, db)
    
    return {
        "id": document.id,
        "filename": file.filename,
        "status": document.status,
        "message": "Document uploaded successfully" if virus_result == "clean" else "Document quarantined for security review",
    }


@router.get("")
async def list_documents(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all documents for current user."""
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
                "processed_at": doc.processed_at.isoformat() if doc.processed_at else None,
                "summary_generated": doc.summary_generated,
            }
            for doc in documents
        ]
    }


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document details."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    result = {
        "id": document.id,
        "filename": document.original_filename,
        "file_size": document.file_size_bytes,
        "mime_type": document.mime_type,
        "status": document.status,
        "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else None,
        "processed_at": document.processed_at.isoformat() if document.processed_at else None,
        "summary_generated": document.summary_generated,
    }
    
    # Include AI summary if available
    if document.ai_summary:
        result["ai_summary"] = {
            "coverage_summary": document.ai_summary.coverage_summary,
            "exclusions": document.ai_summary.exclusions,
            "waiting_period": document.ai_summary.waiting_period,
            "claims_process": document.ai_summary.claims_process,
            "renewal_conditions": document.ai_summary.renewal_conditions,
            "coverage_details": document.ai_summary.coverage_details,
            "exclusions_list": document.ai_summary.exclusions_list,
            "confidence_score": document.ai_summary.confidence_score,
        }
    
    return result


@router.get("/{document_id}/summary", response_model=AISummaryResponse)
async def get_document_summary(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI summary for a document."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.ai_summary:
        raise HTTPException(status_code=404, detail="AI summary not yet generated")
    
    summary = document.ai_summary
    
    return {
        "id": summary.id,
        "document_id": summary.document_id,
        "coverage_summary": summary.coverage_summary,
        "exclusions": summary.exclusions,
        "waiting_period": summary.waiting_period,
        "claims_process": summary.claims_process,
        "renewal_conditions": summary.renewal_conditions,
        "coverage_details": summary.coverage_details or {},
        "exclusions_list": summary.exclusions_list or [],
        "processing_time_seconds": summary.processing_time_seconds,
        "confidence_score": summary.confidence_score,
        "created_at": summary.created_at.isoformat() if summary.created_at else None,
    }


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # TODO: Delete from storage
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
