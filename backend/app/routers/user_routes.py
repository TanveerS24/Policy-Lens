"""
User Routes
User profile management
"""

from fastapi import APIRouter, HTTPException, status, Header
from bson import ObjectId

from app.database.mongodb import get_db
from app.schemas.schemas import (
    UserResponse,
    UserProfileUpdate,
)
from app.utils.token_service import get_current_user
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.get("/me", response_model=dict)
async def get_current_user_profile(authorization: str = Header(None)):
    """
    Get current user profile
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
        user = await db["users"].find_one({"_id": ObjectId(current_user["user_id"])})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Convert ObjectId to string
        user["_id"] = str(user["_id"])
        
        return user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch profile",
        )


@router.put("/me", response_model=dict)
async def update_user_profile(
    request: UserProfileUpdate,
    authorization: str = Header(None),
):
    """
    Update user profile
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
        
        # Prepare update data
        update_data = {}
        if request.name:
            update_data["name"] = request.name
        if request.age:
            update_data["age"] = request.age
        if request.gender:
            update_data["gender"] = request.gender
        if request.state:
            update_data["state"] = request.state
        if request.income:
            update_data["income"] = request.income
        
        # Update user
        await db["users"].update_one(
            {"_id": ObjectId(current_user["user_id"])},
            {"$set": update_data}
        )
        
        logger.info(f"✅ User profile updated: {current_user['email']}")
        
        return {"message": "Profile updated successfully"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile",
        )


@router.get("/notifications")
async def get_notifications(authorization: str = Header(None)):
    """
    Get user notifications
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
        
        # Get notifications
        notifications = await db["notifications"].find(
            {"user_id": current_user["user_id"]}
        ).sort("created_at", -1).to_list(10)
        
        return {
            "notifications": notifications,
            "total": len(notifications),
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch notifications",
        )
