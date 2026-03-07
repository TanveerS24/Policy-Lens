"""
Admin Routes
Policy management, upload approval/rejection
"""

from fastapi import APIRouter, HTTPException, status, Header
from bson import ObjectId
from datetime import datetime

from app.database.mongodb import get_db
from app.schemas.schemas import (
    CreatePolicyRequest,
    UpdatePolicyRequest,
    ApproveUploadRequest,
    RejectUploadRequest,
)
from app.utils.token_service import get_current_admin
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/policy")
async def create_policy(
    request: CreatePolicyRequest,
    authorization: str = Header(None),
):
    """
    Create a new policy (admin only)
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get admin user
        current_admin = await get_current_admin(token)
        
        db = get_db()
        
        # Create policy
        policy_doc = {
            "title": request.title,
            "short_description": request.short_description,
            "summary": request.summary,
            "eligibility_criteria": request.eligibility_criteria,
            "covered_benefits": request.covered_benefits,
            "important_notes": request.important_notes,
            "category": request.category,
            "state": request.state,
            "created_by": current_admin["user_id"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        result = await db["policies"].insert_one(policy_doc)
        
        logger.info(f"✅ Policy created: {request.title}")
        
        return {
            "message": "Policy created successfully",
            "policy_id": str(result.inserted_id),
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error creating policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create policy",
        )


@router.put("/policy/{policy_id}")
async def update_policy(
    policy_id: str,
    request: UpdatePolicyRequest,
    authorization: str = Header(None),
):
    """
    Update a policy (admin only)
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get admin user
        current_admin = await get_current_admin(token)
        
        db = get_db()
        
        # Prepare update data
        update_data = {}
        if request.title:
            update_data["title"] = request.title
        if request.short_description:
            update_data["short_description"] = request.short_description
        if request.summary:
            update_data["summary"] = request.summary
        if request.eligibility_criteria:
            update_data["eligibility_criteria"] = request.eligibility_criteria
        if request.covered_benefits:
            update_data["covered_benefits"] = request.covered_benefits
        if request.important_notes:
            update_data["important_notes"] = request.important_notes
        if request.category:
            update_data["category"] = request.category
        if request.state:
            update_data["state"] = request.state
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Update policy
        await db["policies"].update_one(
            {"_id": ObjectId(policy_id)},
            {"$set": update_data}
        )
        
        logger.info(f"✅ Policy updated: {policy_id}")
        
        return {"message": "Policy updated successfully"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update policy",
        )


@router.delete("/policy/{policy_id}")
async def delete_policy(
    policy_id: str,
    authorization: str = Header(None),
):
    """
    Delete a policy (admin only)
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get admin user
        current_admin = await get_current_admin(token)
        
        db = get_db()
        
        # Delete policy
        await db["policies"].delete_one({"_id": ObjectId(policy_id)})
        
        logger.info(f"✅ Policy deleted: {policy_id}")
        
        return {"message": "Policy deleted successfully"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete policy",
        )


@router.get("/uploads/pending")
async def get_pending_uploads(authorization: str = Header(None)):
    """
    Get pending uploads for approval (admin only)
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get admin user
        current_admin = await get_current_admin(token)
        
        db = get_db()
        
        # Get pending uploads
        uploads = await db["uploads"].find(
            {"status": "pending"}
        ).sort("created_at", 1).to_list(None)
        
        return {
            "uploads": uploads,
            "total": len(uploads),
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching pending uploads: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch pending uploads",
        )


@router.post("/uploads/{upload_id}/approve")
async def approve_upload(
    upload_id: str,
    request: ApproveUploadRequest,
    authorization: str = Header(None),
):
    """
    Approve an upload and create policy (admin only)
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get admin user
        current_admin = await get_current_admin(token)
        
        db = get_db()
        
        # Get upload
        upload = await db["uploads"].find_one({"_id": ObjectId(upload_id)})
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found",
            )
        
        # TODO: Extract PDF text and generate embeddings
        
        # Create policy from upload
        policy_doc = {
            "title": upload.get("title", "Untitled Policy"),
            "short_description": upload.get("short_description", ""),
            "summary": upload.get("summary", ""),
            "eligibility_criteria": upload.get("eligibility", {}),
            "covered_benefits": [],
            "important_notes": [],
            "category": request.category,
            "state": request.state,
            "created_by": current_admin["user_id"],
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        policy_result = await db["policies"].insert_one(policy_doc)
        
        # Update upload status
        await db["uploads"].update_one(
            {"_id": ObjectId(upload_id)},
            {
                "$set": {
                    "status": "approved",
                    "approved_at": datetime.utcnow(),
                    "approved_by": current_admin["user_id"],
                }
            }
        )
        
        # Notify user
        notification_doc = {
            "user_id": upload["user_id"],
            "title": "Policy Upload Approved",
            "message": f"Your uploaded policy has been approved and is now live.",
            "type": "policy_approved",
            "is_read": False,
            "created_at": datetime.utcnow(),
        }
        
        await db["notifications"].insert_one(notification_doc)
        
        logger.info(f"✅ Upload approved: {upload_id}")
        
        return {
            "message": "Upload approved successfully",
            "policy_id": str(policy_result.inserted_id),
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error approving upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve upload",
        )


@router.post("/uploads/{upload_id}/reject")
async def reject_upload(
    upload_id: str,
    request: RejectUploadRequest,
    authorization: str = Header(None),
):
    """
    Reject an upload (admin only)
    """
    try:
        # Extract token
        token = authorization.replace("Bearer ", "") if authorization else None
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization required",
            )
        
        # Get admin user
        current_admin = await get_current_admin(token)
        
        db = get_db()
        
        # Get upload
        upload = await db["uploads"].find_one({"_id": ObjectId(upload_id)})
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found",
            )
        
        # Update upload status
        await db["uploads"].update_one(
            {"_id": ObjectId(upload_id)},
            {
                "$set": {
                    "status": "rejected",
                    "rejection_reason": request.reason,
                }
            }
        )
        
        # Notify user
        notification_doc = {
            "user_id": upload["user_id"],
            "title": "Policy Upload Rejected",
            "message": f"Your uploaded policy has been rejected. Reason: {request.reason}",
            "type": "policy_rejected",
            "is_read": False,
            "created_at": datetime.utcnow(),
        }
        
        await db["notifications"].insert_one(notification_doc)
        
        logger.info(f"✅ Upload rejected: {upload_id}")
        
        return {"message": "Upload rejected successfully"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error rejecting upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject upload",
        )
