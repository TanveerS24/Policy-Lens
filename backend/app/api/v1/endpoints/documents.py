import os
import uuid
import structlog
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.security import HTTPBearer
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.config.database import get_db, SessionLocal
from app.config.settings import get_settings
from app.models.document import Document, AISummary, DocumentChunk, DocumentStatus
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
    coverage_summary: Optional[str] = None
    exclusions: Optional[str] = None
    waiting_period: Optional[str] = None
    claims_process: Optional[str] = None
    renewal_conditions: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    coverage_details: dict
    exclusions_list: list
    processing_time_seconds: Optional[int] = None
    confidence_score: Optional[int] = None
    created_at: str

    @field_validator(
        "coverage_summary",
        "exclusions",
        "waiting_period",
        "claims_process",
        "renewal_conditions",
        "eligibility_criteria",
        mode="before"
    )
    @classmethod
    def coerce_string_fields(cls, v):
        if v is None:
            return None
        return str(v)


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

        if not text or len(text.strip()) < 20:
            doc.status = DocumentStatus.FAILED.value
            doc.summary_generated = False
            db.commit()
            return

        # 1. Validate if document is related to dental/oral health
        val_result = pdf_service.validate_dental_scheme_content(text)
        if not val_result.get("is_dental_scheme"):
            reason = val_result.get("reasoning", "The uploaded document does not contain dental or oral health content.")
            logger.warning("document_rejected_non_dental", document_id=document_id, reasoning=reason)
            doc.status = DocumentStatus.FAILED.value
            doc.summary_generated = False
            doc.publish_status = "non_dental"

            # Remove previous AI summary if exists
            if doc.ai_summary:
                db.delete(doc.ai_summary)

            # Store explicit non-dental error summary so mobile app displays rejection & blocks AI querying
            ai_sum = AISummary(
                document_id=doc.id,
                coverage_summary=f"Non-Dental Document: This file is not related to dental care or oral health. Reasoning: {reason}",
                exclusions="Non-Dental Document — AI Extraction & Eligibility querying blocked.",
                waiting_period="N/A",
                claims_process="N/A",
                renewal_conditions="N/A",
                eligibility_criteria="Non-Dental Document — Eligibility Query Blocked",
                coverage_details={"amount": "N/A", "type": "Non-Dental Document", "is_non_dental": True},
                exclusions_list=["Non-Dental Document"],
                confidence_score=0,
                processing_time_seconds=1,
                model_used="validation"
            )
            db.add(ai_sum)
            db.commit()
            return

        # 2. Extract detailed scheme & dental information
        details = pdf_service.extract_scheme_details(text)

        cov_summary = details.get("about_scheme") or details.get("benefits_covered")
        if isinstance(cov_summary, list):
            cov_summary = ", ".join(cov_summary)
        if not cov_summary:
            cov_summary = f"Comprehensive dental healthcare summary for {doc.original_filename}."

        eligibility = details.get("eligibility_criteria") or "- Age requirement: None / Open to all\n- Income criteria: No income restriction\n- Target category: Open to all citizens\n- Required documents: Standard Identity Proof"

        # 3. Compare uploaded document with existing active schemes using Relevance Score (No brute force)
        scheme_comparison = pdf_service.compare_document_with_schemes(db, text, details)

        # Remove previous AI summary if re-analyzing
        if doc.ai_summary:
            db.delete(doc.ai_summary)

        ai_sum = AISummary(
            document_id=doc.id,
            coverage_summary=str(cov_summary),
            exclusions="• Cosmetic dental procedures unless medically indicated",
            waiting_period="Standard policy terms apply",
            claims_process=details.get("application_process") or "Submit hospital treatment receipts & identity proof to claim benefits.",
            renewal_conditions="Annual policy renewal",
            eligibility_criteria=str(eligibility),
            coverage_details={
                "amount": str(details.get("coverage_amount", "Standard Coverage")),
                "type": str(details.get("type", "national")),
                "has_eligibility_restrictions": details.get("has_eligibility_restrictions", True),
                "is_non_dental": False,
                "scheme_comparison": scheme_comparison
            },
            exclusions_list=["Cosmetic dental procedures"],
            confidence_score=90,
            processing_time_seconds=3,
            model_used="llama3.1:8b"
        )
        db.add(ai_sum)
        doc.status = DocumentStatus.COMPLETED.value
        doc.summary_generated = True
        doc.summary_generated_at = datetime.now(timezone.utc)
        doc.processed_at = datetime.now(timezone.utc)
        db.commit()

    except Exception as e:
        logger.error("process_document_failed", error=str(e), document_id=document_id)
        if doc:
            doc.status = DocumentStatus.FAILED.value
            doc.summary_generated = False
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
    if not pdf_service.is_ai_healthy():
        raise HTTPException(
            status_code=503,
            detail="AI Service is currently offline or unreachable. Please ensure Ollama is running."
        )

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
            "coverage_summary": str(document.ai_summary.coverage_summary) if document.ai_summary.coverage_summary is not None else None,
            "exclusions": str(document.ai_summary.exclusions) if document.ai_summary.exclusions is not None else None,
            "waiting_period": str(document.ai_summary.waiting_period) if document.ai_summary.waiting_period is not None else None,
            "claims_process": str(document.ai_summary.claims_process) if document.ai_summary.claims_process is not None else None,
            "renewal_conditions": str(document.ai_summary.renewal_conditions) if document.ai_summary.renewal_conditions is not None else None,
            "eligibility_criteria": str(document.ai_summary.eligibility_criteria) if document.ai_summary.eligibility_criteria is not None else None,
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
        "coverage_summary": str(summary.coverage_summary) if summary.coverage_summary is not None else None,
        "exclusions": str(summary.exclusions) if summary.exclusions is not None else None,
        "waiting_period": str(summary.waiting_period) if summary.waiting_period is not None else None,
        "claims_process": str(summary.claims_process) if summary.claims_process is not None else None,
        "renewal_conditions": str(summary.renewal_conditions) if summary.renewal_conditions is not None else None,
        "eligibility_criteria": str(summary.eligibility_criteria) if summary.eligibility_criteria is not None else None,
        "coverage_details": summary.coverage_details or {},
        "exclusions_list": summary.exclusions_list or [],
        "processing_time_seconds": summary.processing_time_seconds,
        "confidence_score": summary.confidence_score,
        "created_at": summary.created_at.isoformat() if summary.created_at else None,
    }


@router.get("/{document_id}/matching-schemes")
async def get_matching_schemes(
    document_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get relevance-scored matching schemes for an uploaded document."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.ai_summary:
        raise HTTPException(status_code=404, detail="Document processing not completed yet")

    comparison = (document.ai_summary.coverage_details or {}).get("scheme_comparison")

    if not comparison and os.path.exists(document.storage_path):
        try:
            with open(document.storage_path, "rb") as f:
                content = f.read()
            extraction = pdf_service.extract_text_from_pdf(content)
            if extraction.get("text"):
                details = pdf_service.extract_scheme_details(extraction["text"])
                comparison = pdf_service.compare_document_with_schemes(db, extraction["text"], details)
        except Exception as e:
            logger.warning("on_demand_scheme_comparison_failed", error=str(e))

    return comparison or {
        "matched_schemes": [],
        "comparison_summary": "No scheme comparison available.",
        "total_schemes_evaluated": 0
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
    """Delete a document and all associated data safely."""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Delete associated document chunks (if any)
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete(synchronize_session=False)
        
        # Delete associated AI summary (if any)
        if document.ai_summary:
            db.delete(document.ai_summary)
        
        # Remove physical storage file if it exists on disk
        if document.storage_path and os.path.exists(document.storage_path):
            try:
                os.remove(document.storage_path)
            except Exception as file_err:
                logger.warning("failed_to_delete_physical_file", path=document.storage_path, error=str(file_err))
        
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error("delete_document_error", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")


@router.post("/{document_id}/reanalyze")
async def reanalyze_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Re-analyze and summarize a document with AI."""
    if not pdf_service.is_ai_healthy():
        raise HTTPException(
            status_code=503,
            detail="AI Service is currently offline or unreachable. Please ensure Ollama is running."
        )

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.storage_path or not os.path.exists(document.storage_path):
        raise HTTPException(status_code=400, detail="Document file does not exist on server. Please upload again.")

    # Remove existing AI summary if present
    if document.ai_summary:
        db.delete(document.ai_summary)
        db.commit()

    document.status = DocumentStatus.PROCESSING.value
    document.summary_generated = False
    document.publish_status = "draft"
    db.commit()

    background_tasks.add_task(process_document_sync, document.id, document.storage_path)

    return {
        "id": document.id,
        "status": document.status,
        "message": "AI re-analysis and summarization started."
    }
