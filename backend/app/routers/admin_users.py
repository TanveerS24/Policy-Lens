from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId
from datetime import datetime

from app.database.client import get_db
from app.models.admin_user import AdminUserCreate, AdminUserUpdate
from app.utils.dependencies import require_super_admin_dep, require_content_admin_dep
from app.utils.security import hash_password

router = APIRouter(prefix="/admin/users", tags=["admin-users"])


@router.get("/patients")
async def list_patients(
    status: str | None = Query(None, description="Filter by status: active, deactivated"),
    state_id: str | None = Query(None, description="Filter by state"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """List all patients with filters (Content Admin+)"""
    query: dict = {}
    if status:
        query["status"] = status
    if state_id:
        query["state_id"] = state_id
    
    total = await db["patients"].count_documents(query)
    cursor = db["patients"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    patients = [p async for p in cursor]
    
    return {"total": total, "patients": patients}


@router.get("/patients/{patient_id}")
async def get_patient_details(
    patient_id: str,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Get patient details (Content Admin+)"""
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient id")
    
    patient = await db["patients"].find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    # Get patient's eligibility check history
    eligibility_checks = await db["eligibility_checks"].find({"user_id": patient_id}).to_list(None)
    
    # Get patient's documents
    documents = await db["documents"].find({"user_id": patient_id, "deleted_at": None}).to_list(None)
    
    return {
        "patient": patient,
        "eligibility_checks": eligibility_checks,
        "documents": documents
    }


@router.post("/patients/{patient_id}/deactivate")
async def deactivate_patient_account(
    patient_id: str,
    reason: str = Query(..., description="Reason for deactivation"),
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Deactivate patient account (Content Admin+)"""
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient id")
    
    patient = await db["patients"].find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    await db["patients"].update_one(
        {"_id": ObjectId(patient_id)},
        {
            "$set": {
                "status": "deactivated",
                "deactivated_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Log the action
    from app.services.audit_service import audit_service
    await audit_service.log_action(
        actor_type="admin",
        actor_id=admin["id"],
        action="deactivate_patient",
        entity_type="patient",
        entity_id=patient_id,
        after_json={"reason": reason, "deactivated_by": admin["id"]}
    )
    
    return {"deactivated": True}


@router.post("/patients/{patient_id}/activate")
async def activate_patient_account(
    patient_id: str,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Reactivate patient account (Content Admin+)"""
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient id")
    
    patient = await db["patients"].find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    await db["patients"].update_one(
        {"_id": ObjectId(patient_id)},
        {
            "$set": {
                "status": "active",
                "deactivated_at": None,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Log the action
    from app.services.audit_service import audit_service
    await audit_service.log_action(
        actor_type="admin",
        actor_id=admin["id"],
        action="activate_patient",
        entity_type="patient",
        entity_id=patient_id
    )
    
    return {"activated": True}


@router.get("/admins")
async def list_admin_users(
    role: str | None = Query(None, description="Filter by role"),
    status: str | None = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db=Depends(get_db),
    admin=Depends(require_super_admin_dep),
):
    """List all admin users (Super Admin only)"""
    query: dict = {}
    if role:
        query["role"] = role
    if status:
        query["status"] = status
    
    total = await db["admin_users"].count_documents(query)
    cursor = db["admin_users"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    admins = [a async for a in cursor]
    
    return {"total": total, "admins": admins}


@router.post("/admins")
async def create_admin_user(
    request: AdminUserCreate,
    db=Depends(get_db),
    admin=Depends(require_super_admin_dep),
):
    """Create new admin user (Super Admin only)"""
    # Check if email already exists
    existing = await db["admin_users"].find_one({"email": request.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = hash_password(request.password)
    
    # Create admin user
    admin_doc = request.dict()
    admin_doc.pop("password")
    admin_doc.update({
        "hashed_password": hashed_password,
        "mfa_secret": None,
        "mfa_enabled": False,
        "status": "active",
        "force_password_change": request.force_password_change,
        "last_login": None,
        "last_password_change": None,
        "created_by": admin["id"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db["admin_users"].insert_one(admin_doc)
    
    # Log the action
    from app.services.audit_service import audit_service
    await audit_service.log_action(
        actor_type="admin",
        actor_id=admin["id"],
        action="create_admin",
        entity_type="admin_user",
        entity_id=str(result.inserted_id),
        after_json={"role": request.role, "email": request.email}
    )
    
    return {"id": str(result.inserted_id)}


@router.put("/admins/{admin_id}")
async def update_admin_user(
    admin_id: str,
    request: AdminUserUpdate,
    db=Depends(get_db),
    admin=Depends(require_super_admin_dep),
):
    """Update admin user (Super Admin only)"""
    if not ObjectId.is_valid(admin_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin id")
    
    existing = await db["admin_users"].find_one({"_id": ObjectId(admin_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")
    
    # Prevent modifying own role
    if str(existing["_id"]) == admin["id"] and "role" in request.dict(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify your own role"
        )
    
    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db["admin_users"].update_one(
        {"_id": ObjectId(admin_id)},
        {"$set": update_data}
    )
    
    # Log the action
    from app.services.audit_service import audit_service
    await audit_service.log_action(
        actor_type="admin",
        actor_id=admin["id"],
        action="update_admin",
        entity_type="admin_user",
        entity_id=admin_id,
        before_json={"previous": existing.get("role")},
        after_json=update_data
    )
    
    return {"updated": True}


@router.delete("/admins/{admin_id}")
async def delete_admin_user(
    admin_id: str,
    db=Depends(get_db),
    admin=Depends(require_super_admin_dep),
):
    """Delete admin user (Super Admin only)"""
    if not ObjectId.is_valid(admin_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin id")
    
    existing = await db["admin_users"].find_one({"_id": ObjectId(admin_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")
    
    # Prevent deleting self
    if str(existing["_id"]) == admin["id"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
    )
    
    await db["admin_users"].delete_one({"_id": ObjectId(admin_id)})
    
    # Log the action
    from app.services.audit_service import audit_service
    await audit_service.log_action(
        actor_type="admin",
        actor_id=admin["id"],
        action="delete_admin",
        entity_type="admin_user",
        entity_id=admin_id
    )
    
    return {"deleted": True}
