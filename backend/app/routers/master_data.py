from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId

from app.database.client import get_db
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/master", tags=["master-data"])


# States endpoints
@router.get("/states")
async def list_states(
    active_only: bool = Query(True, description="Filter to only active states"),
    zone: str | None = Query(None, description="Filter by zone"),
    db=Depends(get_db),
):
    query: dict = {}
    if active_only:
        query["active"] = True
    if zone:
        query["zone"] = zone
    
    cursor = db["states"].find(query).sort("name", 1)
    return [state async for state in cursor]


@router.get("/states/{state_id}")
async def get_state(state_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(state_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state id")
    state = await db["states"].find_one({"_id": ObjectId(state_id)})
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="State not found")
    return state


@router.post("/admin/states")
async def create_state(state_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    # Check if state code already exists
    existing = await db["states"].find_one({"code": state_data["code"]})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State code already exists")
    
    result = await db["states"].insert_one({
        **state_data,
        "active": True,
        "created_at": "2026-01-01T00:00:00Z"
    })
    return {"id": str(result.inserted_id)}


@router.put("/admin/states/{state_id}")
async def update_state(state_id: str, state_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(state_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state id")
    
    # Don't allow updating code
    if "code" in state_data:
        del state_data["code"]
    
    await db["states"].update_one(
        {"_id": ObjectId(state_id)},
        {"$set": state_data}
    )
    return {"updated": True}


@router.put("/admin/states/{state_id}/deactivate")
async def deactivate_state(state_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(state_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state id")
    
    await db["states"].update_one(
        {"_id": ObjectId(state_id)},
        {"$set": {"active": False}}
    )
    return {"deactivated": True}


# Districts endpoints
@router.get("/districts")
async def list_districts(
    state_id: str | None = Query(None, description="Filter by state ID"),
    active_only: bool = Query(True, description="Filter to only active districts"),
    db=Depends(get_db),
):
    query: dict = {}
    if active_only:
        query["active"] = True
    if state_id:
        if ObjectId.is_valid(state_id):
            query["state_id"] = state_id
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state id")
    
    cursor = db["districts"].find(query).sort("name", 1)
    return [district async for district in cursor]


@router.get("/districts/{district_id}")
async def get_district(district_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(district_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid district id")
    district = await db["districts"].find_one({"_id": ObjectId(district_id)})
    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found")
    return district


@router.post("/admin/districts")
async def create_district(district_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    # Validate state_id exists
    if "state_id" in district_data and ObjectId.is_valid(district_data["state_id"]):
        state = await db["states"].find_one({"_id": ObjectId(district_data["state_id"])})
        if not state:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state_id")
    
    result = await db["districts"].insert_one({
        **district_data,
        "active": True,
        "created_at": "2026-01-01T00:00:00Z"
    })
    return {"id": str(result.inserted_id)}


@router.put("/admin/districts/{district_id}")
async def update_district(district_id: str, district_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(district_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid district id")
    
    # Don't allow updating state_id
    if "state_id" in district_data:
        del district_data["state_id"]
    
    await db["districts"].update_one(
        {"_id": ObjectId(district_id)},
        {"$set": district_data}
    )
    return {"updated": True}


@router.put("/admin/districts/{district_id}/deactivate")
async def deactivate_district(district_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(district_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid district id")
    
    await db["districts"].update_one(
        {"_id": ObjectId(district_id)},
        {"$set": {"active": False}}
    )
    return {"deactivated": True}


# Beneficiary Categories endpoints
@router.get("/beneficiary-categories")
async def list_beneficiary_categories(
    active_only: bool = Query(True, description="Filter to only active categories"),
    db=Depends(get_db),
):
    query: dict = {}
    if active_only:
        query["active"] = True
    
    cursor = db["beneficiary_categories"].find(query).sort("name", 1)
    return [category async for category in cursor]


@router.get("/beneficiary-categories/{category_id}")
async def get_beneficiary_category(category_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category id")
    category = await db["beneficiary_categories"].find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiary category not found")
    return category


@router.post("/admin/beneficiary-categories")
async def create_beneficiary_category(category_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    # Check if code already exists
    existing = await db["beneficiary_categories"].find_one({"code": category_data["code"]})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category code already exists")
    
    result = await db["beneficiary_categories"].insert_one({
        **category_data,
        "active": True,
        "created_at": "2026-01-01T00:00:00Z"
    })
    return {"id": str(result.inserted_id)}


@router.put("/admin/beneficiary-categories/{category_id}")
async def update_beneficiary_category(category_id: str, category_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category id")
    
    # Don't allow updating code
    if "code" in category_data:
        del category_data["code"]
    
    await db["beneficiary_categories"].update_one(
        {"_id": ObjectId(category_id)},
        {"$set": category_data}
    )
    return {"updated": True}


@router.put("/admin/beneficiary-categories/{category_id}/deactivate")
async def deactivate_beneficiary_category(category_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category id")
    
    await db["beneficiary_categories"].update_one(
        {"_id": ObjectId(category_id)},
        {"$set": {"active": False}}
    )
    return {"deactivated": True}


# Dental Services endpoints
@router.get("/dental-services")
async def list_dental_services(
    active_only: bool = Query(True, description="Filter to only active services"),
    category: str | None = Query(None, description="Filter by category"),
    db=Depends(get_db),
):
    query: dict = {}
    if active_only:
        query["active"] = True
    if category:
        query["category"] = category
    
    cursor = db["dental_services"].find(query).sort("name", 1)
    return [service async for service in cursor]


@router.get("/dental-services/{service_id}")
async def get_dental_service(service_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid service id")
    service = await db["dental_services"].find_one({"_id": ObjectId(service_id)})
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dental service not found")
    return service


@router.post("/admin/dental-services")
async def create_dental_service(service_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    # Check if code already exists
    existing = await db["dental_services"].find_one({"code": service_data["code"]})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service code already exists")
    
    result = await db["dental_services"].insert_one({
        **service_data,
        "active": True,
        "created_at": "2026-01-01T00:00:00Z"
    })
    return {"id": str(result.inserted_id)}


@router.put("/admin/dental-services/{service_id}")
async def update_dental_service(service_id: str, service_data: dict, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid service id")
    
    # Don't allow updating code
    if "code" in service_data:
        del service_data["code"]
    
    await db["dental_services"].update_one(
        {"_id": ObjectId(service_id)},
        {"$set": service_data}
    )
    return {"updated": True}


@router.put("/admin/dental-services/{service_id}/deactivate")
async def deactivate_dental_service(service_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid service id")
    
    await db["dental_services"].update_one(
        {"_id": ObjectId(service_id)},
        {"$set": {"active": False}}
    )
    return {"deactivated": True}
