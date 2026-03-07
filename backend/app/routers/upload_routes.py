"""
Upload Routes
Handle PDF uploads, approve/reject user uploads
"""

from fastapi import APIRouter, HTTPException, status, UploadFile, File, Header
import os
from datetime import datetime

from app.database.mongodb import get_db
from app.schemas.schemas import (
    UploadResponse,
    UploadListResponse,
    PublishUploadRequest,
)
from app.utils.token_service import get_current_user
from app.utils.logger import setup_logger
from app.config.settings import settings

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    authorization: str = Header(None),
):
    """
    Upload a PDF policy
    Extract text, generate summary and eligibility
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get current user
        current_user = await get_current_user(token)
        
        # Validate file
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed",
            )
        
        # Create uploads directory
        os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
        
        # Save file
        file_path = os.path.join(settings.UPLOADS_DIR, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        db = get_db()
        
        # TODO: Extract text from PDF
        # TODO: Generate summary using Gemma3
        # TODO: Extract eligibility criteria
        # TODO: Create embeddings and store in FAISS
        
        # Store upload request
        upload_doc = {
            "user_id": current_user["user_id"],
            "pdf_path": file_path,
            "pdf_filename": file.filename,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
        
        result = await db["uploads"].insert_one(upload_doc)
        
        logger.info(f"✅ PDF uploaded: {file.filename}")
        
        return {
            "message": "PDF uploaded successfully",
            "upload_id": str(result.inserted_id),
            "filename": file.filename,
            "status": "pending",
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error uploading PDF: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload PDF",
        )


@router.get("/my", response_model=dict)
async def get_my_uploads(authorization: str = Header(None)):
    """
    Get current user's uploads
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get current user
        current_user = await get_current_user(token)
        
        db = get_db()
        
        # Get user uploads
        uploads = await db["uploads"].find(
            {"user_id": current_user["user_id"]}
        ).sort("created_at", -1).to_list(None)
        
        return {
            "uploads": uploads,
            "total": len(uploads),
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching uploads: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch uploads",
        )


@router.delete("/{upload_id}")
async def delete_upload(
    upload_id: str,
    authorization: str = Header(None),
):
    """
    Delete an upload
    """
    try:
        from bson import ObjectId
        
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get current user
        current_user = await get_current_user(token)
        
        db = get_db()
        
        # Check upload exists and belongs to user
        upload = await db["uploads"].find_one({
            "_id": ObjectId(upload_id),
            "user_id": current_user["user_id"],
        })
        
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found",
            )
        
        # Delete file if exists
        if os.path.exists(upload["pdf_path"]):
            os.remove(upload["pdf_path"])
        
        # Delete from database
        await db["uploads"].delete_one({"_id": ObjectId(upload_id)})
        
        logger.info(f"✅ Upload deleted: {upload_id}")
        
        return {"message": "Upload deleted successfully"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete upload",
        )


@router.post("/{upload_id}/publish")
async def publish_upload(
    upload_id: str,
    request: PublishUploadRequest,
    authorization: str = Header(None),
):
    """
    Publish upload (send request to admin)
    """
    try:
        from bson import ObjectId
        
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get current user
        current_user = await get_current_user(token)
        
        db = get_db()
        
        # Check upload exists and belongs to user
        upload = await db["uploads"].find_one({
            "_id": ObjectId(upload_id),
            "user_id": current_user["user_id"],
        })
        
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found",
            )
        
        # Update upload request details
        await db["uploads"].update_one(
            {"_id": ObjectId(upload_id)},
            {
                "$set": {
                    "title": request.title,
                    "short_description": request.short_description,
                    "category": request.category,
                    "state": request.state,
                }
            }
        )
        
        logger.info(f"✅ Upload published for approval: {upload_id}")
        
        return {"message": "Upload sent for approval"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error publishing upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to publish upload",
        )
