from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from bson import ObjectId
from datetime import datetime
import imghdr

from app.database.client import get_db
from app.models.document import DocumentCreate, DocumentInDB, DocumentPublic
from app.services.document_summary_service import document_summary_service
from app.utils.dependencies import get_current_patient
from app.utils.gridfs_helper import gridfs_helper

router = APIRouter(prefix="/patients/me/documents", tags=["documents"])


@router.get("", response_model=list[DocumentPublic])
async def list_documents(
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """List patient's uploaded documents"""
    query = {"user_id": patient.id, "deleted_at": None}
    
    total = await db["documents"].count_documents(query)
    cursor = db["documents"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    documents = [doc async for doc in cursor]
    
    return documents


@router.post("")
async def upload_document(
    file: UploadFile = File(...),
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Upload new document (PDF, JPG, PNG, TIFF)"""
    # Validate file type
    allowed_mime_types = ["application/pdf", "image/jpeg", "image/png", "image/tiff", "image/jpg"]
    if not file.content_type or file.content_type not in allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, JPG, PNG, and TIFF files are allowed"
        )
    
    # Read file data
    file_data = await file.read()
    
    # Validate file size (max 10MB)
    if len(file_data) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10MB limit"
        )
    
    # Validate actual file type
    if file.content_type.startswith("image/"):
        image_type = imghdr.what(None, h=file_data)
        if image_type not in ["jpeg", "png", "tiff"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image format"
            )
    
    # Check document limit (max 20 per user)
    doc_count = await db["documents"].count_documents({
        "user_id": patient.id,
        "deleted_at": None
    })
    if doc_count >= 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum document limit (20) reached"
        )
    
    # Upload file to GridFS
    file_id = await gridfs_helper.upload_file(
        filename=file.filename,
        file_data=file_data,
        content_type=file.content_type,
        metadata={
            "user_id": patient.id,
            "original_name": file.filename,
            "uploaded_at": datetime.utcnow().isoformat()
        }
    )
    
    # Create document record
    document_doc = {
        "user_id": patient.id,
        "original_name": file.filename,
        "mime_type": file.content_type,
        "file_size": len(file_data),
        "storage_key": file_id,
        "upload_status": "pending",
        "ai_status": "pending",
        "reprocess_count": 0,
        "display_name": file.filename,
        "created_at": datetime.utcnow(),
        "deleted_at": None
    }
    
    result = await db["documents"].insert_one(document_doc)
    
    # Trigger async AI summary generation
    asyncio.create_task(
        document_summary_service.process_document_async(
            result.inserted_id,
            patient.id,
            file_id,
            db
        )
    )
    
    return {"id": str(result.inserted_id), "message": "Document uploaded. AI summary will be generated shortly."}


@router.get("/{document_id}", response_model=DocumentPublic)
async def get_document(
    document_id: str,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Get document details with summary"""
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document id")
    
    document = await db["documents"].find_one({
        "_id": ObjectId(document_id),
        "user_id": patient.id,
        "deleted_at": None
    })
    
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    # Get summary if available
    summary = await db["document_summaries"].find_one({"document_id": document_id})
    if summary:
        document["summary"] = summary["summary_json"]
    
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Soft delete document"""
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document id")
    
    document = await db["documents"].find_one({
        "_id": ObjectId(document_id),
        "user_id": patient.id,
        "deleted_at": None
    })
    
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    # Soft delete (file will be removed after 30 days)
    await db["documents"].update_one(
        {"_id": ObjectId(document_id)},
        {"$set": {"deleted_at": datetime.utcnow()}}
    )
    
    return {"deleted": True}


@router.post("/{document_id}/reprocess")
async def reprocess_document(
    document_id: str,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Re-trigger AI summary generation (max 3 re-processes)"""
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document id")
    
    document = await db["documents"].find_one({
        "_id": ObjectId(document_id),
        "user_id": patient.id,
        "deleted_at": None
    })
    
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    # Check reprocess limit
    if document.get("reprocess_count", 0) >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum re-process limit (3) reached"
        )
    
    # Increment reprocess count
    await db["documents"].update_one(
        {"_id": ObjectId(document_id)},
        {
            "$inc": {"reprocess_count": 1},
            "$set": {"ai_status": "pending"}
        }
    )
    
    # Delete old summary
    await db["document_summaries"].delete_many({"document_id": document_id})
    
    # Trigger async AI summary generation
    asyncio.create_task(
        document_summary_service.process_document_async(
            ObjectId(document_id),
            patient.id,
            document["storage_key"],
            db
        )
    )
    
    return {"message": "Document re-queued for AI summary generation"}


@router.patch("/{document_id}/rename")
async def rename_document(
    document_id: str,
    new_name: str,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Rename document (display name only)"""
    if not ObjectId.is_valid(document_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document id")
    
    if not new_name or len(new_name) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid display name"
        )
    
    document = await db["documents"].find_one({
        "_id": ObjectId(document_id),
        "user_id": patient.id,
        "deleted_at": None
    })
    
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    await db["documents"].update_one(
        {"_id": ObjectId(document_id)},
        {"$set": {"display_name": new_name}}
    )
    
    return {"renamed": True}
