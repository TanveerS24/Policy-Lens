from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from bson import ObjectId
from datetime import datetime, timedelta
import imghdr
from io import BytesIO
from PIL import Image

from app.database.client import get_db
from app.models.patient import PatientUpdate, MobileUpdate, PasswordUpdate
from app.services.patient_auth_service import patient_auth_service
from app.utils.dependencies import get_current_patient
from app.utils.security import hash_password, verify_password
from app.utils.gridfs_helper import gridfs_helper

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me")
async def get_profile(patient=Depends(get_current_patient)):
    """Get current patient profile"""
    return patient


@router.patch("/me")
async def update_profile(
    request: PatientUpdate,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Update patient profile"""
    update_data = request.dict(exclude_unset=True)
    
    # Validate state and district if provided
    if "state_id" in update_data:
        state = await db["states"].find_one({"_id": ObjectId(update_data["state_id"]), "active": True})
        if not state:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state")
    
    if "district_id" in update_data:
        district = await db["districts"].find_one({"_id": ObjectId(update_data["district_id"]), "active": True})
        if not district:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid district")
        
        # Validate district belongs to state
        state_id = update_data.get("state_id", str(patient.state_id))
        if str(district["state_id"]) != state_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="District does not belong to the selected state")
    
    # Update profile
    update_data["updated_at"] = datetime.utcnow()
    
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {"$set": update_data}
    )
    
    return {"updated": True}


@router.post("/me/mobile")
async def update_mobile(
    request: MobileUpdate,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Update mobile number with OTP verification"""
    # Verify OTP for new mobile
    otp_result = await patient_auth_service.verify_otp(
        mobile=request.new_mobile,
        otp=request.otp,
        purpose="mobile_change"
    )
    
    if not otp_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Check if new mobile already exists
    existing = await db["patients"].find_one({"mobile": request.new_mobile})
    if existing and str(existing["_id"]) != patient.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )
    
    # Update mobile
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "mobile": request.new_mobile,
                "mobile_verified": True,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"updated": True}


@router.post("/me/password")
async def update_password(
    request: PasswordUpdate,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Update password with current password verification"""
    # Verify current password
    if not verify_password(request.current_password, patient.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    # Hash new password
    hashed_password = hash_password(request.new_password)
    
    # Update password
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "hashed_password": hashed_password,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Revoke all sessions for security
    await patient_auth_service.revoke_all_sessions(patient.id)
    
    return {"updated": True}


@router.post("/me/deactivate")
async def deactivate_account(patient=Depends(get_current_patient), db=Depends(get_db)):
    """Deactivate account (soft-delete, 90-day retention)"""
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "status": "deactivated",
                "deactivated_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Revoke all sessions
    await patient_auth_service.revoke_all_sessions(patient.id)
    
    return {"deactivated": True}


@router.post("/me/reactivate")
async def reactivate_account(patient=Depends(get_current_patient), db=Depends(get_db)):
    """Reactivate deactivated account (within 90 days)"""
    if patient.status != "deactivated":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is not deactivated"
        )
    
    # Check if within 90-day window
    if patient.deactivated_at:
        days_since_deactivation = (datetime.utcnow() - patient.deactivated_at).days
        if days_since_deactivation > 90:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account cannot be reactivated after 90 days. Please register a new account."
            )
    
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "status": "active",
                "deactivated_at": None,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"reactivated": True}


@router.post("/me/delete-request")
async def request_account_deletion(patient=Depends(get_current_patient), db=Depends(get_db)):
    """Request permanent account deletion (30-day cooling period)"""
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "deletion_requested_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Deletion request submitted. Account will be permanently deleted after 30-day cooling period."}


@router.post("/me/delete-confirm")
async def confirm_account_deletion(patient=Depends(get_current_patient), db=Depends(get_db)):
    """Confirm account deletion (after 30-day cooling period)"""
    if not patient.deletion_requested_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No deletion request found"
        )
    
    # Check if 30-day cooling period has passed
    days_since_request = (datetime.utcnow() - patient.deletion_requested_at).days
    if days_since_request < 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account cannot be deleted until 30-day cooling period ends. {30 - days_since_request} days remaining."
        )
    
    # Mark as deleted (DPDP compliance - data will be erased after additional period)
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "status": "deleted",
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Revoke all sessions
    await patient_auth_service.revoke_all_sessions(patient.id)
    
    return {"deleted": True}


@router.get("/me/data-export")
async def export_my_data(patient=Depends(get_current_patient), db=Depends(get_db)):
    """Export patient data (DPDP compliance)"""
    # Get patient profile
    patient_data = await db["patients"].find_one({"_id": ObjectId(patient.id)})
    
    # Get uploaded documents metadata
    documents = await db["documents"].find({"user_id": patient.id}).to_list(None)
    
    # Get eligibility check history
    eligibility_checks = await db["eligibility_checks"].find({"user_id": patient.id}).to_list(None)
    
    # Prepare export data
    export_data = {
        "profile": patient_data,
        "documents": documents,
        "eligibility_checks": eligibility_checks,
        "exported_at": datetime.utcnow().isoformat()
    }
    
    return export_data


@router.post("/me/photo")
async def upload_profile_photo(
    file: UploadFile = File(...),
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Upload profile photo (JPEG/PNG, max 2MB, auto-cropped to 1:1)"""
    # Validate file type
    if not file.content_type or file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG and PNG images are allowed"
        )
    
    # Read file data
    file_data = await file.read()
    
    # Validate file size (max 2MB)
    if len(file_data) > 2 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 2MB limit"
        )
    
    # Validate actual image type
    image_type = imghdr.what(None, h=file_data)
    if image_type not in ["jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format"
        )
    
    # Process image - crop to 1:1 ratio
    try:
        img = Image.open(BytesIO(file_data))
        
        # Get dimensions
        width, height = img.size
        
        # Calculate square crop
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        
        # Crop to square
        img_cropped = img.crop((left, top, right, bottom))
        
        # Resize to standard size (e.g., 300x300)
        img_resized = img_cropped.resize((300, 300), Image.Resampling.LANCZOS)
        
        # Convert back to bytes
        output = BytesIO()
        img_resized.save(output, format="JPEG" if image_type == "jpeg" else "PNG")
        processed_data = output.getvalue()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing image: {str(e)}"
        )
    
    # Delete old photo if exists
    if patient.profile_photo_url:
        # Extract file ID from URL (assuming format: /api/v1/files/{file_id})
        if patient.profile_photo_url.startswith("/api/v1/files/"):
            old_file_id = patient.profile_photo_url.split("/")[-1]
            await gridfs_helper.delete_file(old_file_id)
    
    # Upload new photo to GridFS
    file_id = await gridfs_helper.upload_file(
        filename=f"profile_{patient.id}.{image_type}",
        file_data=processed_data,
        content_type=file.content_type,
        metadata={"user_id": patient.id, "uploaded_at": datetime.utcnow().isoformat()}
    )
    
    # Update patient profile with new photo URL
    photo_url = f"/api/v1/files/{file_id}"
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "profile_photo_url": photo_url,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"photo_url": photo_url}


@router.delete("/me/photo")
async def delete_profile_photo(patient=Depends(get_current_patient), db=Depends(get_db)):
    """Delete profile photo"""
    if not patient.profile_photo_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No profile photo to delete"
        )
    
    # Delete file from GridFS
    if patient.profile_photo_url.startswith("/api/v1/files/"):
        file_id = patient.profile_photo_url.split("/")[-1]
        await gridfs_helper.delete_file(file_id)
    
    # Remove photo URL from profile
    await db["patients"].update_one(
        {"_id": ObjectId(patient.id)},
        {
            "$set": {
                "profile_photo_url": None,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"deleted": True}
