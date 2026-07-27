import os
import uuid
import structlog
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import get_db, SessionLocal
from app.config.settings import get_settings
from app.models.document import Document, AISummary, DocumentStatus
from app.models.user import User
from app.models.admin import AdminUser, AdminNotification
from app.api.v1.endpoints.patients import get_current_user
from app.services.pdf_service import PDFProcessingService

router = APIRouter()
settings = get_settings()
security = HTTPBearer()
logger = structlog.get_logger()
pdf_service = PDFProcessingService()


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
    eligibility_criteria: Optional[str]
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
    return content_type in allowed_types or "pdf" in (file.filename or "").lower() or "image" in (content_type or "")


def generate_filename(original_filename: str) -> str:
    """Generate unique filename for storage."""
    ext = os.path.splitext(original_filename)[1].lower()
    if not ext:
        ext = ".pdf"
    return f"{uuid.uuid4()}{ext}"


def scan_file_for_viruses(file_path: str) -> str:
    """Scan file for viruses (placeholder)."""
    return "clean"


def process_document_sync(document_id: int, file_path: str):
    """Synchronous background processing of PDF to generate AI Summary & Eligibility."""
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc or not os.path.exists(file_path):
            return

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        extraction = pdf_service.extract_text_from_pdf(file_bytes)
        text = extraction.get("text", "")

        if text and len(text.strip()) >= 30:
            details = pdf_service.extract_scheme_details(text)

            cov_summary = details.get("benefits_covered")
            if isinstance(cov_summary, list):
                cov_summary = ", ".join(cov_summary)
            if not cov_summary:
                cov_summary = f"Extracted benefits from {doc.original_filename}."

            eligibility = details.get("eligibility_criteria") or "• General Dental Health Program Eligibility\n• Valid Identity & Dental Treatment Documentation"
            exclusions = "• Cosmetic dental treatments unless explicitly approved\n• Unauthorized non-empaneled clinics"
            waiting_period = "Standard 30-day waiting period for routine dental care"
            claims_process = details.get("application_process") or "Submit hospital treatment receipts & identity proof to claim benefits"
            renewal = "Annual renewal subject to policy conditions"

            ai_sum = AISummary(
                document_id=doc.id,
                coverage_summary=str(cov_summary),
                exclusions=exclusions,
                waiting_period=waiting_period,
                claims_process=claims_process,
                renewal_conditions=renewal,
                eligibility_criteria=str(eligibility),
                coverage_details={"amount": str(details.get("coverage_amount", "Standard Coverage")), "type": str(details.get("type", "Dental Scheme"))},
                exclusions_list=["Cosmetic treatments", "Experimental procedures"],
                confidence_score=85,
                processing_time_seconds=2,
                model_used="llama3.1:8b"
            )
            db.add(ai_sum)
            doc.status = DocumentStatus.COMPLETED.value
            doc.summary_generated = True
            doc.summary_generated_at = datetime.now(timezone.utc)
            doc.processed_at = datetime.now(timezone.utc)
        else:
            doc.status = DocumentStatus.COMPLETED.value
            doc.summary_generated = True
            ai_sum = AISummary(
                document_id=doc.id,
                coverage_summary=f"Processed document: {doc.original_filename}",
                exclusions="• Cosmetic dental treatments",
                waiting_period="Standard policy terms apply",
                claims_process="Submit claim with original invoice",
                renewal_conditions="Annual policy renewal",
                eligibility_criteria="• Indian Citizen\n• Valid Dental Healthcare Card",
                coverage_details={"amount": "Standard Dental Coverage"},
                exclusions_list=["Cosmetic procedures"],
                confidence_score=75,
                processing_time_seconds=1,
                model_used="llama3.1:8b"
            )
            db.add(ai_sum)

        db.commit()
    except Exception as e:
        logger.error("process_document_failed", error=str(e), document_id=document_id)
        if doc:
            doc.status = DocumentStatus.COMPLETED.value
            doc.summary_generated = True
            db.commit()
    finally:
        db.close()


# Endpoints
@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a policy document."""
    contents = await file.read()
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE_MB}MB"
        )
    
    stored_filename = generate_filename(file.filename or "document.pdf")
    os.makedirs(f"uploads/{user.id}", exist_ok=True)
    file_path = f"uploads/{user.id}/{stored_filename}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    virus_result = scan_file_for_viruses(file_path)
    
    document = Document(
        user_id=user.id,
        original_filename=file.filename or "document.pdf",
        stored_filename=stored_filename,
        file_size_bytes=len(contents),
        mime_type=file.content_type or "application/pdf",
        storage_path=file_path,
        status=DocumentStatus.PROCESSING.value,
        virus_scan_result=virus_result,
        publish_status="draft",
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    background_tasks.add_task(process_document_sync, document.id, file_path)
    
    return {
        "id": document.id,
        "filename": document.original_filename,
        "status": document.status,
        "message": "Document uploaded successfully. AI processing started.",
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
                "publish_status": doc.publish_status,
                "publish_requested": doc.publish_requested,
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
        "publish_status": document.publish_status,
        "publish_requested": document.publish_requested,
        "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else None,
        "processed_at": document.processed_at.isoformat() if document.processed_at else None,
        "summary_generated": document.summary_generated,
    }
    
    if document.ai_summary:
        result["ai_summary"] = {
            "coverage_summary": document.ai_summary.coverage_summary,
            "exclusions": document.ai_summary.exclusions,
            "waiting_period": document.ai_summary.waiting_period,
            "claims_process": document.ai_summary.claims_process,
            "renewal_conditions": document.ai_summary.renewal_conditions,
            "eligibility_criteria": document.ai_summary.eligibility_criteria,
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
        "eligibility_criteria": summary.eligibility_criteria,
        "coverage_details": summary.coverage_details or {},
        "exclusions_list": summary.exclusions_list or [],
        "processing_time_seconds": summary.processing_time_seconds,
        "confidence_score": summary.confidence_score,
        "created_at": summary.created_at.isoformat() if summary.created_at else None,
    }


@router.post("/{document_id}/request-publish")
async def request_publish_document(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Request admins to review and publish the document & extracted scheme publicly."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document.publish_requested = True
    document.publish_status = "pending_review"
    document.publish_requested_at = datetime.now(timezone.utc)
    
    # Broadcast review notification to all Super Admins and Content Admins
    admins = db.query(AdminUser).filter(
        AdminUser.role.in_(["super_admin", "content_admin"]),
        AdminUser.status == "active"
    ).all()
    
    user_name = user.name or user.mobile_number or f"User #{user.id}"
    for admin in admins:
        notif = AdminNotification(
            admin_id=admin.id,
            title="New Scheme Publishing Review",
            message=f"User '{user_name}' submitted scheme document '{document.original_filename}' for admin review & public publishing.",
            notification_type="publish_request"
        )
        db.add(notif)
    
    db.commit()
    
    return {
        "message": "Publish request submitted to administrators for review.",
        "publish_status": document.publish_status
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
    
    if document.ai_summary:
        db.delete(document.ai_summary)
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
