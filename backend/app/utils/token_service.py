"""
Token Service
Manages JWT token operations
"""

from fastapi import HTTPException, status
from jose import JWTError
from app.config.security import TokenManager
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def get_current_user(token: str) -> dict:
    """Extract user info from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = TokenManager.verify_token(token)
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        
        if user_id is None or email is None:
            raise credentials_exception
        
        return {
            "user_id": user_id,
            "email": email,
            "role": role,
        }
    except JWTError as e:
        logger.error(f"Token verification error: {e}")
        raise credentials_exception


async def get_current_admin(token: str) -> dict:
    """Get current admin user"""
    user = await get_current_user(token)
    
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return user
