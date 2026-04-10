from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId

from app.database.client import get_db
from app.schemas.policy import PolicyCreateRequest
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def get_dashboard(db=Depends(get_db), admin=Depends(require_admin)):
    total_policies = await db["policies"].count_documents({})
    pending = await db["policies"].count_documents({"approved": False})
    total_users = await db["users"].count_documents({})
    recent_policies = [p async for p in db["policies"].find({}).sort([("created_at", -1)]).limit(5)]
    return {
        "total_policies": total_policies,
        "pending_approvals": pending,
        "total_users": total_users,
        "recent_policies": recent_policies,
    }


@router.get("/policies")
async def list_policies(
    q: str | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db=Depends(get_db),
    admin=Depends(require_admin),
):
    query: dict = {}
    if status is not None:
        query["approved"] = status.lower() in ("true", "1", "yes")
    if q:
        query["$text"] = {"$search": q}
    cursor = db["policies"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    return [p async for p in cursor]


@router.post("/policy")
async def create_policy(request: PolicyCreateRequest, db=Depends(get_db), admin=Depends(require_admin)):
    doc = request.dict()
    doc.update({"approved": True, "created_by": None, "created_at": datetime.utcnow()})
    result = await db["policies"].insert_one(doc)
    return {"id": str(result.inserted_id)}


@router.put("/policy/{policy_id}")
async def update_policy(policy_id: str, request: PolicyCreateRequest, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].update_one({"_id": ObjectId(policy_id)}, {"$set": request.dict()})
    return {"updated": True}


@router.delete("/policy/{policy_id}")
async def delete_policy(policy_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].delete_one({"_id": ObjectId(policy_id)})
    return {"deleted": True}


@router.get("/pending")
async def pending_requests(db=Depends(get_db), admin=Depends(require_admin)):
    cursor = db["policies"].find({"approved": False}).sort([("created_at", -1)])
    return [p async for p in cursor]


@router.post("/approve/{policy_id}")
async def approve_policy(policy_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].update_one(
        {"_id": ObjectId(policy_id)},
        {"$set": {"approved": True, "published_at": datetime.utcnow()}},
    )
    return {"approved": True}


@router.post("/reject/{policy_id}")
async def reject_policy(policy_id: str, db=Depends(get_db), admin=Depends(require_admin)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].delete_one({"_id": ObjectId(policy_id)})
    return {"rejected": True}
