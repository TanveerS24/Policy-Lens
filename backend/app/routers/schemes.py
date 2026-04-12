from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId
from datetime import datetime

from app.database.client import get_db
from app.models.scheme import SchemeCreate, SchemeInDB, SchemePublic, SchemeUpdate
from app.utils.dependencies import get_current_admin_user

router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.get("")
async def list_schemes(
    scheme_type: str | None = Query(None, description="Filter by scheme type: national/state"),
    state_id: str | None = Query(None, description="Filter by state ID"),
    beneficiary_category: str | None = Query(None, description="Filter by beneficiary category"),
    service: str | None = Query(None, description="Filter by service covered"),
    active_status: str | None = Query(None, description="Filter by status: active/inactive/discontinued"),
    search: str | None = Query(None, description="Search in scheme name and description"),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db=Depends(get_db),
):
    """List all schemes with filters (public endpoint)"""
    query: dict = {}
    
    if scheme_type:
        query["scheme_type"] = scheme_type
    if state_id:
        query["state_id"] = state_id
    if active_status:
        query["active_status"] = active_status
    if beneficiary_category:
        query["beneficiary_categories"] = beneficiary_category
    if service:
        query["services_covered"] = service
    if search:
        query["$or"] = [
            {"scheme_name": {"$regex": search, "$options": "i"}},
            {"short_description": {"$regex": search, "$options": "i"}},
            {"detailed_description": {"$regex": search, "$options": "i"}}
        ]
    
    total = await db["schemes"].count_documents(query)
    cursor = db["schemes"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    items = [scheme async for scheme in cursor]
    
    return {"total": total, "items": items}


@router.get("/{scheme_id}", response_model=SchemePublic)
async def get_scheme(scheme_id: str, db=Depends(get_db)):
    """Get scheme details by ID (public endpoint)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    scheme = await db["schemes"].find_one({"_id": ObjectId(scheme_id)})
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    
    return scheme


# Admin endpoints
@router.post("/admin/schemes")
async def create_scheme(request: SchemeCreate, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    """Create new scheme (Admin only - Content Admin+)"""
    # Validate state exists if state scheme
    if request.scheme_type == "state" and request.state_id:
        if not ObjectId.is_valid(request.state_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state id")
        state = await db["states"].find_one({"_id": ObjectId(request.state_id)})
        if not state:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State not found")
    
    # Check for duplicate scheme name + state combination
    duplicate_query = {"scheme_name": request.scheme_name}
    if request.state_id:
        duplicate_query["state_id"] = request.state_id
    else:
        duplicate_query["state_id"] = None
    
    existing = await db["schemes"].find_one(duplicate_query)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheme with this name already exists for this state"
        )
    
    # Validate beneficiary categories exist
    for cat_id in request.beneficiary_categories:
        if ObjectId.is_valid(cat_id):
            cat = await db["beneficiary_categories"].find_one({"_id": ObjectId(cat_id)})
            if not cat:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid beneficiary category: {cat_id}")
    
    # Validate services exist
    for service_id in request.services_covered:
        if ObjectId.is_valid(service_id):
            service = await db["dental_services"].find_one({"_id": ObjectId(service_id)})
            if not service:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid dental service: {service_id}")
    
    # Create scheme
    scheme_doc = request.dict()
    scheme_doc.update({
        "version": 1,
        "last_updated_by": admin["id"],
        "last_updated_at": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "published_at": None  # Draft by default
    })
    
    result = await db["schemes"].insert_one(scheme_doc)
    
    # Create initial version snapshot
    await db["scheme_versions"].insert_one({
        "scheme_id": str(result.inserted_id),
        "version_number": 1,
        "snapshot": scheme_doc,
        "changed_by": admin["id"],
        "changed_at": datetime.utcnow(),
        "change_reason": "Initial creation"
    })
    
    return {"id": str(result.inserted_id), "version": 1}


@router.put("/admin/schemes/{scheme_id}")
async def update_scheme(scheme_id: str, request: SchemeUpdate, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    """Update scheme (Admin only - Content Admin+)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    existing = await db["schemes"].find_one({"_id": ObjectId(scheme_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    
    # Create version snapshot before update
    current_version = existing.get("version", 1)
    new_version = current_version + 1
    
    await db["scheme_versions"].insert_one({
        "scheme_id": scheme_id,
        "version_number": new_version,
        "snapshot": existing,
        "changed_by": admin["id"],
        "changed_at": datetime.utcnow(),
        "change_reason": "Scheme update"
    })
    
    # Update scheme
    update_data = request.dict(exclude_unset=True)
    update_data.update({
        "version": new_version,
        "last_updated_by": admin["id"],
        "last_updated_at": datetime.utcnow()
    })
    
    await db["schemes"].update_one(
        {"_id": ObjectId(scheme_id)},
        {"$set": update_data}
    )
    
    return {"updated": True, "new_version": new_version}


@router.delete("/admin/schemes/{scheme_id}")
async def delete_scheme(scheme_id: str, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    """Soft delete scheme (Admin only - Super Admin)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    # Check admin role - only Super Admin can delete
    if admin.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admin can delete schemes"
        )
    
    existing = await db["schemes"].find_one({"_id": ObjectId(scheme_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    
    # Soft delete by setting status to discontinued
    await db["schemes"].update_one(
        {"_id": ObjectId(scheme_id)},
        {
            "$set": {
                "active_status": "discontinued",
                "last_updated_by": admin["id"],
                "last_updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"deleted": True}


@router.post("/admin/schemes/{scheme_id}/publish")
async def publish_scheme(scheme_id: str, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    """Publish draft scheme (Admin only - Content Admin+)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    existing = await db["schemes"].find_one({"_id": ObjectId(scheme_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    
    if existing.get("published_at"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheme is already published"
        )
    
    await db["schemes"].update_one(
        {"_id": ObjectId(scheme_id)},
        {
            "$set": {
                "published_at": datetime.utcnow(),
                "active_status": "active",
                "last_updated_by": admin["id"],
                "last_updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"published": True}


@router.get("/admin/schemes/{scheme_id}/versions")
async def get_scheme_versions(scheme_id: str, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    """Get scheme version history (Admin only)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    cursor = db["scheme_versions"].find({"scheme_id": scheme_id}).sort([("version_number", -1)]).limit(10)
    versions = [version async for version in cursor]
    
    return {"versions": versions}


@router.post("/admin/schemes/{scheme_id}/clone")
async def clone_scheme(scheme_id: str, db=Depends(get_db), admin=Depends(get_current_admin_user)):
    """Clone scheme (useful for creating state variants) (Admin only)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    existing = await db["schemes"].find_one({"_id": ObjectId(scheme_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    
    # Create clone
    clone_doc = existing.copy()
    clone_doc.pop("_id")
    clone_doc.pop("created_at")
    clone_doc.pop("published_at")
    clone_doc["scheme_name"] = f"{existing['scheme_name']} (Copy)"
    clone_doc["version"] = 1
    clone_doc["last_updated_by"] = admin["id"]
    clone_doc["last_updated_at"] = datetime.utcnow()
    clone_doc["created_at"] = datetime.utcnow()
    
    result = await db["schemes"].insert_one(clone_doc)
    
    # Create initial version for clone
    await db["scheme_versions"].insert_one({
        "scheme_id": str(result.inserted_id),
        "version_number": 1,
        "snapshot": clone_doc,
        "changed_by": admin["id"],
        "changed_at": datetime.utcnow(),
        "change_reason": f"Cloned from scheme {scheme_id}"
    })
    
    return {"id": str(result.inserted_id), "cloned_from": scheme_id}
