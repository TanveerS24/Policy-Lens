"""
Policy Routes
Retrieve policies, check eligibility, ask questions
"""

from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional

from app.database.mongodb import get_db
from app.schemas.schemas import (
    PolicyListResponse,
    PolicyResponse,
    PolicyFilterRequest,
    EligibilityCheckForMe,
    EligibilityCheckForOther,
    EligibilityResponse,
    PolicyQuestionRequest,
    PolicyQuestionResponse,
)
from app.utils.token_service import get_current_user
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.get("/", response_model=dict)
async def list_policies(
    skip: int = 0,
    limit: int = 10,
    state: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
):
    """
    Get list of policies with optional filtering
    """
    try:
        db = get_db()
        
        # Build query
        query = {"is_active": True}
        
        if state:
            query["state"] = state
        if category:
            query["category"] = category
        if search:
            query["$text"] = {"$search": search}
        
        # Get policies
        policies = await db["policies"].find(query).skip(skip).limit(limit).to_list(limit)
        total = await db["policies"].count_documents(query)
        
        return {
            "policies": policies,
            "total": total,
            "skip": skip,
            "limit": limit,
        }
    
    except Exception as e:
        logger.error(f"Error fetching policies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch policies",
        )


@router.get("/{policy_id}", response_model=dict)
async def get_policy_detail(policy_id: str):
    """
    Get policy details
    """
    try:
        from bson import ObjectId
        
        db = get_db()
        
        # Fetch policy
        policy = await db["policies"].find_one({"_id": ObjectId(policy_id)})
        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found",
            )
        
        return policy
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching policy: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch policy",
        )


@router.post("/check-eligibility/me", response_model=EligibilityResponse)
async def check_eligibility_for_me(
    request: EligibilityCheckForMe,
    authorization: str = Header(None),
):
    """
    Check eligibility for current user
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
        
        # Get user profile
        from bson import ObjectId
        user = await db["users"].find_one({"_id": ObjectId(current_user["user_id"])})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Get policy
        policy = await db["policies"].find_one({"_id": ObjectId(request.policy_id)})
        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found",
            )
        
        # TODO: Call eligibility service to check eligibility
        # For now, return placeholder response
        
        return EligibilityResponse(
            eligible=True,
            reason="User meets all eligibility criteria",
            missing_requirements=[],
            confidence_score=0.95,
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error checking eligibility: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check eligibility",
        )


@router.post("/check-eligibility/other", response_model=EligibilityResponse)
async def check_eligibility_for_other(request: EligibilityCheckForOther):
    """
    Check eligibility for another person
    """
    try:
        db = get_db()
        
        # Get policy
        from bson import ObjectId
        policy = await db["policies"].find_one({"_id": ObjectId(request.policy_id)})
        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found",
            )
        
        # TODO: Call eligibility service to check eligibility
        # For now, return placeholder response
        
        return EligibilityResponse(
            eligible=False,
            reason="User age is below minimum requirement",
            missing_requirements=["Minimum age 60", "Government health ID"],
            confidence_score=0.90,
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error checking eligibility: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check eligibility",
        )


@router.post("/ask", response_model=PolicyQuestionResponse)
async def ask_policy_question(request: PolicyQuestionRequest):
    """
    Ask a question about a specific policy
    Uses RAG with Llama3.2
    """
    try:
        from bson import ObjectId
        
        db = get_db()
        
        # Get policy
        policy = await db["policies"].find_one({"_id": ObjectId(request.policy_id)})
        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found",
            )
        
        # TODO: Call RAG service to answer question
        # For now, return placeholder response
        
        return PolicyQuestionResponse(
            question=request.question,
            answer="This policy is available in Tamil Nadu. The details are provided in Section 3.2.",
            confidence_score=0.88,
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to answer question",
        )
