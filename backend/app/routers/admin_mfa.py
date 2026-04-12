from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.database.client import get_db
from app.utils.dependencies import require_super_admin_dep, get_current_admin_user_dep
from app.services.totp_service import totp_service
from app.utils.security import hash_password

router = APIRouter(prefix="/admin/mfa", tags=["admin-mfa"])


@router.post("/setup")
async def setup_mfa(
    db=Depends(get_db),
    admin=Depends(get_current_admin_user_dep),
):
    """Setup TOTP MFA for admin account"""
    # Check if MFA already enabled
    admin_user = await db["admin_users"].find_one({"_id": ObjectId(admin["id"])})
    if admin_user.get("mfa_enabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    
    # Generate secret
    secret = totp_service.generate_secret()
    qr_code_url = totp_service.generate_qr_code_url(secret, admin["email"])
    
    # Generate backup codes
    backup_codes = totp_service.generate_backup_codes()
    
    # Store hashed backup codes
    hashed_backup_codes = [hash_password(code) for code in backup_codes]
    
    # Update admin user with secret (not yet enabled)
    await db["admin_users"].update_one(
        {"_id": ObjectId(admin["id"])},
        {
            "$set": {
                "mfa_secret": secret,
                "mfa_backup_codes": hashed_backup_codes,
                "mfa_enabled": False  # Will be enabled after verification
            }
        }
    )
    
    return {
        "qr_code_url": qr_code_url,
        "secret": secret,
        "backup_codes": backup_codes  # Return only once for user to save
    }


@router.post("/verify")
async def verify_mfa_setup(
    token: str,
    db=Depends(get_db),
    admin=Depends(get_current_admin_user_dep),
):
    """Verify TOTP token and enable MFA"""
    admin_user = await db["admin_users"].find_one({"_id": ObjectId(admin["id"])})
    
    if not admin_user.get("mfa_secret"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA setup not initiated. Call /setup first."
        )
    
    if admin_user.get("mfa_enabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    
    # Verify token
    if not totp_service.verify_totp(admin_user["mfa_secret"], token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid TOTP token"
        )
    
    # Enable MFA
    await db["admin_users"].update_one(
        {"_id": ObjectId(admin["id"])},
        {"$set": {"mfa_enabled": True}}
    )
    
    return {"enabled": True}


@router.post("/disable")
async def disable_mfa(
    password: str,
    db=Depends(get_db),
    admin=Depends(get_current_admin_user_dep),
):
    """Disable MFA (requires password confirmation)"""
    admin_user = await db["admin_users"].find_one({"_id": ObjectId(admin["id"])})
    
    if not admin_user.get("mfa_enabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    
    # Verify password
    from app.utils.security import verify_password
    if not verify_password(password, admin_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    # Disable MFA
    await db["admin_users"].update_one(
        {"_id": ObjectId(admin["id"])},
        {
            "$set": {
                "mfa_enabled": False,
                "mfa_secret": None,
                "mfa_backup_codes": []
            }
        }
    )
    
    return {"disabled": True}


@router.post("/verify-token")
async def verify_mfa_token(
    token: str,
    db=Depends(get_db),
    admin=Depends(get_current_admin_user_dep),
):
    """Verify TOTP token for login"""
    admin_user = await db["admin_users"].find_one({"_id": ObjectId(admin["id"])})
    
    if not admin_user.get("mfa_enabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled for this account"
        )
    
    # Verify TOTP token
    if totp_service.verify_totp(admin_user["mfa_secret"], token):
        return {"valid": True}
    
    # Check backup codes
    from app.utils.security import verify_password
    for hashed_code in admin_user.get("mfa_backup_codes", []):
        if verify_password(token, hashed_code):
            # Remove used backup code
            await db["admin_users"].update_one(
                {"_id": ObjectId(admin["id"])},
                {"$pull": {"mfa_backup_codes": hashed_code}}
            )
            return {"valid": True, "backup_code_used": True}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid MFA token"
    )


@router.post("/regenerate-backup-codes")
async def regenerate_backup_codes(
    password: str,
    db=Depends(get_db),
    admin=Depends(get_current_admin_user_dep),
):
    """Regenerate backup codes (requires password confirmation)"""
    admin_user = await db["admin_users"].find_one({"_id": ObjectId(admin["id"])})
    
    if not admin_user.get("mfa_enabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    
    # Verify password
    from app.utils.security import verify_password
    if not verify_password(password, admin_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    # Generate new backup codes
    backup_codes = totp_service.generate_backup_codes()
    hashed_backup_codes = [hash_password(code) for code in backup_codes]
    
    # Update admin user
    await db["admin_users"].update_one(
        {"_id": ObjectId(admin["id"])},
        {"$set": {"mfa_backup_codes": hashed_backup_codes}}
    )
    
    return {"backup_codes": backup_codes}
