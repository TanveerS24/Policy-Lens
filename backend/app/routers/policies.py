from fastapi import APIRouter, Depends, HTTPException, Query, status
from bson import ObjectId

from app.database.client import get_db
from app.schemas.policy import AskRequest, AskResponse, EligibilityCheckRequest, EligibilityResponse, PolicyListResponse, PolicySummaryResponse
from app.services.rag_service import rag_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("", response_model=PolicyListResponse)
async def list_policies(
    q: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db=Depends(get_db),
):
    query = {"approved": True}
    if q:
        query["$text"] = {"$search": q}
    total = await db["policies"].count_documents(query)
    cursor = db["policies"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
    items = [policy async for policy in cursor]
    return {"total": total, "items": items}


@router.get("/{policy_id}", response_model=PolicySummaryResponse)
async def get_policy(policy_id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(policy_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid policy id")
    policy = await db["policies"].find_one({"_id": ObjectId(policy_id), "approved": True})
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")
    return policy


@router.post("/check-eligibility", response_model=EligibilityResponse)
async def check_eligibility(request: EligibilityCheckRequest, user=Depends(get_current_user), db=Depends(get_db)):
    policy = await db["policies"].find_one({"_id": ObjectId(request.policy_id), "approved": True})
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    result = await rag_service.check_eligibility(request.policy_id, request.profile)
    return result


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, user=Depends(get_current_user), db=Depends(get_db)):
    policy = await db["policies"].find_one({"_id": ObjectId(request.policy_id), "approved": True})
    if not policy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Policy not found")

    answer = await rag_service.ask_question(request.policy_id, request.question)
    return {"answer": answer}
