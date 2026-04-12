from bson import ObjectId
from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database.client import get_db
from app.models.patient import PatientInDB
from app.utils.rbac import get_current_admin_user, require_content_admin, require_super_admin, require_support_admin
from app.utils.security import decode_token

security = HTTPBearer(auto_error=False)


async def get_current_patient(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db=Depends(get_db),
) -> PatientInDB:
    """Get current authenticated patient"""
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid scheme: {credentials.scheme}")
    
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token type: {payload.get('type')}")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload: missing sub")

    patient = await db["patients"].find_one({"_id": ObjectId(user_id)})
    if not patient:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Patient not found")

    # Check account status
    if patient.get("status") == "deactivated":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")
    if patient.get("status") == "deleted":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account has been deleted")

    # Convert ObjectId to string for Pydantic model
    patient["_id"] = str(patient["_id"])
    return PatientInDB(**patient)


async def get_current_admin_user_dep(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db=Depends(get_db),
) -> dict:
    """Dependency wrapper for get_current_admin_user"""
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid scheme: {credentials.scheme}")
    
    token = credentials.credentials
    return await get_current_admin_user(token, db)


def require_super_admin_dep(admin: dict = Depends(get_current_admin_user_dep)) -> dict:
    """Dependency wrapper for require_super_admin"""
    return require_super_admin(admin)


def require_content_admin_dep(admin: dict = Depends(get_current_admin_user_dep)) -> dict:
    """Dependency wrapper for require_content_admin"""
    return require_content_admin(admin)


def require_support_admin_dep(admin: dict = Depends(get_current_admin_user_dep)) -> dict:
    """Dependency wrapper for require_support_admin"""
    return require_support_admin(admin)


# Legacy compatibility - will be removed after migration
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db=Depends(get_db),
):
    """Legacy function - use get_current_patient instead"""
    return await get_current_patient(credentials, db)


def require_admin(user = Depends(get_current_user)):
    """Legacy function - use get_current_admin_user_dep instead"""
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Use new admin authentication endpoints")
