from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId

from app.database.client import get_db
from app.schemas.policy import PolicyCreateRequest
from app.utils.dependencies import require_content_admin_dep, require_super_admin_dep

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
async def get_dashboard(db=Depends(get_db), admin=Depends(require_super_admin_dep)):
    """Enhanced admin dashboard with all PRD metrics"""
    
    # Scheme metrics
    total_schemes = await db["schemes"].count_documents({})
    national_schemes = await db["schemes"].count_documents({"scheme_type": "national"})
    state_schemes = await db["schemes"].count_documents({"scheme_type": "state"})
    active_schemes = await db["schemes"].count_documents({"active_status": "active"})
    inactive_schemes = await db["schemes"].count_documents({"active_status": "inactive"})
    discontinued_schemes = await db["schemes"].count_documents({"active_status": "discontinued"})
    
    # Patient metrics
    total_patients = await db["patients"].count_documents({})
    active_patients = await db["patients"].count_documents({"status": "active"})
    deactivated_patients = await db["patients"].count_documents({"status": "deactivated"})
    
    # Patient registration trend (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_registrations = await db["patients"].count_documents({
        "created_at": {"$gte": thirty_days_ago}
    })
    
    # Daily registration counts for last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    registration_trend = []
    for i in range(7):
        day_start = datetime.utcnow() - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        count = await db["patients"].count_documents({
            "created_at": {"$gte": day_start, "$lt": day_end}
        })
        registration_trend.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count
        })
    registration_trend.reverse()
    
    # Document metrics
    total_documents = await db["documents"].count_documents({"deleted_at": None})
    documents_pending_ai = await db["documents"].count_documents({"ai_status": "pending"})
    documents_processing_ai = await db["documents"].count_documents({"ai_status": "processing"})
    documents_ai_completed = await db["documents"].count_documents({"ai_status": "completed"})
    documents_ai_failed = await db["documents"].count_documents({"ai_status": "failed"})
    
    # Eligibility check metrics (last 30 days)
    total_eligibility_checks = await db["eligibility_checks"].count_documents({
        "checked_at": {"$gte": thirty_days_ago}
    })
    likely_eligible = await db["eligibility_checks"].count_documents({
        "checked_at": {"$gte": thirty_days_ago},
        "result": "likely_eligible"
    })
    possibly_eligible = await db["eligibility_checks"].count_documents({
        "checked_at": {"$gte": thirty_days_ago},
        "result": "possibly_eligible"
    })
    not_eligible = await db["eligibility_checks"].count_documents({
        "checked_at": {"$gte": thirty_days_ago},
        "result": "not_eligible"
    })
    
    # Master data metrics
    total_states = await db["states"].count_documents({"active": True})
    total_districts = await db["districts"].count_documents({"active": True})
    total_beneficiary_categories = await db["beneficiary_categories"].count_documents({"active": True})
    total_dental_services = await db["dental_services"].count_documents({"active": True})
    
    # System health indicators
    try:
        from app.utils.redis_client import redis_client
        redis = await redis_client.get_client()
        await redis.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    # Recent activity
    recent_patients = [p async for p in db["patients"].find({}).sort([("created_at", -1)]).limit(5)]
    recent_schemes = [s async for s in db["schemes"].find({}).sort([("created_at", -1)]).limit(5)]
    
    return {
        "schemes": {
            "total": total_schemes,
            "national": national_schemes,
            "state": state_schemes,
            "active": active_schemes,
            "inactive": inactive_schemes,
            "discontinued": discontinued_schemes,
            "recent": recent_schemes
        },
        "patients": {
            "total": total_patients,
            "active": active_patients,
            "deactivated": deactivated_patients,
            "recent_registrations_30d": recent_registrations,
            "registration_trend_7d": registration_trend,
            "recent": recent_patients
        },
        "documents": {
            "total": total_documents,
            "pending_ai": documents_pending_ai,
            "processing_ai": documents_processing_ai,
            "ai_completed": documents_ai_completed,
            "ai_failed": documents_ai_failed
        },
        "eligibility": {
            "total_checks_30d": total_eligibility_checks,
            "likely_eligible": likely_eligible,
            "possibly_eligible": possibly_eligible,
            "not_eligible": not_eligible
        },
        "master_data": {
            "states": total_states,
            "districts": total_districts,
            "beneficiary_categories": total_beneficiary_categories,
            "dental_services": total_dental_services
        },
        "system_health": {
            "redis": redis_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    }


@router.get("/policies")
async def list_policies(
    q: str | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    query: dict = {}
    if status is not None:
        query["approved"] = status.lower() in ("true", "1", "yes")
    if q:
        query["$text"] = {"$search": q}
    cursor = db["policies"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    return [p async for p in cursor]


@router.post("/policy")
async def create_policy(request: PolicyCreateRequest, db=Depends(get_db), admin=Depends(require_content_admin_dep)):
    doc = request.dict()
    doc.update({"approved": True, "created_by": None, "created_at": datetime.utcnow()})
    result = await db["policies"].insert_one(doc)
    return {"id": str(result.inserted_id)}


@router.put("/policy/{policy_id}")
async def update_policy(policy_id: str, request: PolicyCreateRequest, db=Depends(get_db), admin=Depends(require_content_admin_dep)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].update_one({"_id": ObjectId(policy_id)}, {"$set": request.dict()})
    return {"updated": True}


@router.delete("/policy/{policy_id}")
async def delete_policy(policy_id: str, db=Depends(get_db), admin=Depends(require_content_admin_dep)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].delete_one({"_id": ObjectId(policy_id)})
    return {"deleted": True}


@router.get("/pending")
async def pending_requests(db=Depends(get_db), admin=Depends(require_content_admin_dep)):
    cursor = db["policies"].find({"approved": False}).sort([("created_at", -1)])
    return [p async for p in cursor]


@router.post("/approve/{policy_id}")
async def approve_policy(policy_id: str, db=Depends(get_db), admin=Depends(require_content_admin_dep)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].update_one(
        {"_id": ObjectId(policy_id)},
        {"$set": {"approved": True, "published_at": datetime.utcnow()}},
    )
    return {"approved": True}


@router.post("/reject/{policy_id}")
async def reject_policy(policy_id: str, db=Depends(get_db), admin=Depends(require_content_admin_dep)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    await db["policies"].delete_one({"_id": ObjectId(policy_id)})
    return {"rejected": True}
