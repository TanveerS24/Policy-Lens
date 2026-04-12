from fastapi import Depends, HTTPException, status
from typing import Optional

from app.utils.security import decode_token
from app.database.client import get_db


async def get_current_admin_user(token: str, db):
    """
    Get current admin user from token
    
    Args:
        token: JWT access token
        db: Database instance
    
    Returns:
        dict: Admin user data
    
    Raises:
        HTTPException: If token invalid or user not found
    """
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Check if it's an admin user
    admin = await db["admin_users"].find_one({"_id": user_id})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found"
        )
    
    # Check if admin is active
    if admin.get("status") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is not active"
        )
    
    # Check if password change is required
    if admin.get("force_password_change"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password change required"
        )
    
    return {
        "id": str(admin["_id"]),
        "name": admin["name"],
        "email": admin["email"],
        "role": admin["role"],
        "status": admin["status"]
    }


async def require_super_admin(admin: dict):
    """
    Require Super Admin role
    
    Args:
        admin: Admin user data from get_current_admin_user
    
    Raises:
        HTTPException: If user is not Super Admin
    """
    if admin.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access required"
        )
    return admin


async def require_content_admin(admin: dict):
    """
    Require Content Admin or higher role
    
    Args:
        admin: Admin user data from get_current_admin_user
    
    Raises:
        HTTPException: If user is not Content Admin or Super Admin
    """
    if admin.get("role") not in ["content_admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Content Admin access required"
        )
    return admin


async def require_support_admin(admin: dict):
    """
    Require Support Admin or higher role
    
    Args:
        admin: Admin user data from get_current_admin_user
    
    Raises:
        HTTPException: If user is not Support Admin, Content Admin, or Super Admin
    """
    if admin.get("role") not in ["support_admin", "content_admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Support Admin access required"
        )
    return admin


def check_ip_whitelist(admin_ip: str, allowed_ips: Optional[list]) -> bool:
    """
    Check if IP is in whitelist
    
    Args:
        admin_ip: Client IP address
        allowed_ips: List of allowed IP addresses
    
    Returns:
        bool: True if IP is allowed or no whitelist configured
    """
    if not allowed_ips:
        return True
    
    return admin_ip in allowed_ips
