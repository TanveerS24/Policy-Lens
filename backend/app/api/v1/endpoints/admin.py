"""Admin endpoints."""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
import bcrypt

from app.config.database import get_db
from app.config.settings import get_settings
from app.models.admin import AdminUser, AdminRole, AdminStatus
from app.models.scheme import Scheme
from app.models.user import User
from app.models.audit import AuditLog
from app.services.jwt_service import JWTService

router = APIRouter()
settings = get_settings()
jwt_service = JWTService()
security = HTTPBearer()


# Schemas
class AdminLoginRequest(BaseModel):
    email: str
    password: str
    mfa_code: Optional[str] = None


class CreateAdminRequest(BaseModel):
    name: str
    email: str
    password: str = Field(..., min_length=8)
    role: str = Field(default="support_admin")


class CreateSchemeRequest(BaseModel):
    name: str
    code: str
    type: str
    description: str
    ministry: Optional[str] = None
    state: Optional[str] = None
    target_categories: List[str] = []
    services_covered: List[str] = []
    coverage_amount: Optional[float] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    required_documents: List[str] = []
    website: Optional[str] = None
    helpline: Optional[str] = None


# Dependencies
async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AdminUser:
    """Get current authenticated admin."""
    token = credentials.credentials
    payload = jwt_service.verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    role = payload.get("role")
    if role not in ["super_admin", "content_admin", "support_admin"]:
        raise HTTPException(status_code=403, detail="Invalid admin role")
    
    admin_id = int(payload.get("sub"))
    admin = db.query(AdminUser).filter(
        AdminUser.id == admin_id,
        AdminUser.status == AdminStatus.ACTIVE.value
    ).first()
    
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found or inactive")
    
    return admin


def require_role(*allowed_roles: str):
    """Dependency to check admin role."""
    def role_checker(admin: AdminUser = Depends(get_current_admin)):
        if admin.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return admin
    return role_checker


# Endpoints
@router.post("/login")
async def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    """Admin login with MFA support."""
    admin = db.query(AdminUser).filter(AdminUser.email == request.email).first()
    
    if not admin or admin.status != AdminStatus.ACTIVE.value:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check lockout
    if admin.locked_until and admin.locked_until > datetime.utcnow():
        raise HTTPException(status_code=423, detail="Account locked. Try again later.")
    
    # Verify password
    if not bcrypt.checkpw(request.password.encode(), admin.hashed_password.encode()):
        admin.failed_login_attempts += 1
        
        if admin.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            admin.locked_until = datetime.utcnow() + timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
        
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # TODO: Verify MFA if enabled
    if admin.mfa_enabled:
        if not request.mfa_code:
            raise HTTPException(status_code=400, detail="MFA code required")
        # Verify MFA code logic here
    
    # Reset failed attempts
    admin.failed_login_attempts = 0
    admin.locked_until = None
    admin.last_login_at = datetime.utcnow()
    db.commit()
    
    # Generate tokens
    access_token, refresh_token = jwt_service.create_tokens(admin.id, admin.role)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "admin": {
            "id": admin.id,
            "name": admin.name,
            "email": admin.email,
            "role": admin.role,
        }
    }


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    # Verify refresh token
    payload = jwt_service.verify_token(request.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # Get admin from database
    admin_id = int(payload.get("sub"))
    admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    
    if not admin or admin.status != AdminStatus.ACTIVE.value:
        raise HTTPException(status_code=401, detail="Admin not found or inactive")
    
    # Generate new tokens
    access_token, new_refresh_token = jwt_service.create_tokens(admin.id, admin.role)
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@router.get("/dashboard")
async def get_dashboard(
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard analytics."""
    # User statistics
    total_users = db.query(User).filter(User.is_active == True).count()
    new_users_today = db.query(User).filter(
        User.created_at >= datetime.utcnow() - timedelta(days=1)
    ).count()
    
    # Scheme statistics
    total_schemes = db.query(Scheme).filter(Scheme.is_deleted == False).count()
    active_schemes = db.query(Scheme).filter(
        Scheme.is_deleted == False,
        Scheme.status == "active"
    ).count()
    
    # Documents
    total_documents = db.query(func.count(Scheme.id)).scalar()  # Placeholder
    
    # Recent activity
    recent_audit_logs = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).limit(10).all()
    
    return {
        "statistics": {
            "total_users": total_users,
            "new_users_today": new_users_today,
            "total_schemes": total_schemes,
            "active_schemes": active_schemes,
            "total_documents": total_documents,
        },
        "recent_activity": [
            {
                "id": log.id,
                "action": log.action,
                "actor_type": log.actor_type,
                "resource_type": log.resource_type,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in recent_audit_logs
        ]
    }


@router.get("/schemes")
async def list_all_schemes(
    status: Optional[str] = None,
    type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all schemes (admin view)."""
    query = db.query(Scheme).filter(Scheme.is_deleted == False)
    
    if status:
        query = query.filter(Scheme.status == status)
    if type:
        query = query.filter(Scheme.type == type)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(Scheme.name.ilike(search_filter))
    
    total = query.count()
    schemes = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "schemes": [s.to_dict() for s in schemes],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
        }
    }


@router.post("/schemes")
async def create_scheme(
    request: CreateSchemeRequest,
    admin: AdminUser = Depends(require_role("super_admin", "content_admin")),
    db: Session = Depends(get_db)
):
    """Create a new scheme."""
    # Check if code exists
    existing = db.query(Scheme).filter(Scheme.code == request.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Scheme code already exists")
    
    scheme = Scheme(
        name=request.name,
        code=request.code,
        type=request.type,
        description=request.description,
        ministry=request.ministry,
        state=request.state,
        target_categories=request.target_categories,
        services_covered=request.services_covered,
        coverage_amount=request.coverage_amount,
        min_age=request.min_age,
        max_age=request.max_age,
        required_documents=request.required_documents,
        website=request.website,
        helpline=request.helpline,
        created_by=admin.id,
    )
    
    db.add(scheme)
    db.commit()
    db.refresh(scheme)
    
    # Log action
    audit_log = AuditLog(
        actor_type="admin",
        actor_id=admin.id,
        admin_id=admin.id,
        action="scheme_create",
        resource_type="scheme",
        resource_id=scheme.id,
        success="success",
        description=f"Created scheme: {scheme.name}"
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Scheme created successfully", "scheme_id": scheme.id}


@router.get("/users")
async def list_users(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    per_page: int = 20,
    admin: AdminUser = Depends(require_role("super_admin", "support_admin")),
    db: Session = Depends(get_db)
):
    """List all users."""
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            User.name.ilike(search_filter) |
            User.mobile.ilike(search_filter) |
            User.email.ilike(search_filter)
        )
    
    total = query.count()
    users = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "mobile": u.mobile,
                "email": u.email,
                "is_active": u.is_active,
                "is_verified": u.is_verified,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
        }
    }


@router.post("/admins")
async def create_admin(
    request: CreateAdminRequest,
    admin: AdminUser = Depends(require_role("super_admin")),
    db: Session = Depends(get_db)
):
    """Create a new admin user (super admin only)."""
    # Check if email exists
    existing = db.query(AdminUser).filter(AdminUser.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    # Hash password
    hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    
    new_admin = AdminUser(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password,
        role=request.role,
        status=AdminStatus.ACTIVE.value,
        created_by=admin.id,
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    return {
        "message": "Admin created successfully",
        "admin_id": new_admin.id,
        "role": new_admin.role,
    }


@router.get("/admins")
async def list_admins(
    page: int = 1,
    per_page: int = 20,
    admin: AdminUser = Depends(require_role("super_admin")),
    db: Session = Depends(get_db)
):
    """List all admin users (super admin only)."""
    query = db.query(AdminUser)
    
    total = query.count()
    admins = query.order_by(AdminUser.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "admins": [
            {
                "id": a.id,
                "name": a.name,
                "email": a.email,
                "role": a.role,
                "status": a.status,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in admins
        ],
        "page": page,
        "per_page": per_page,
        "total": total,
    }


@router.delete("/admins/{admin_id}")
async def delete_admin(
    admin_id: int,
    admin: AdminUser = Depends(require_role("super_admin")),
    db: Session = Depends(get_db)
):
    """Delete an admin user (super admin only, cannot delete self unless another super admin exists)."""
    target_admin = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    if not target_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Check if deleting self
    if admin_id == admin.id:
        # Only allow if another super admin exists
        if admin.role == "super_admin":
            super_admin_count = db.query(AdminUser).filter(AdminUser.role == "super_admin").count()
            if super_admin_count <= 1:
                raise HTTPException(status_code=400, detail="Cannot delete yourself - you are the last super admin. Create another super admin first.")
    
    # Prevent deleting the last super admin
    if target_admin.role == "super_admin" and admin_id != admin.id:
        super_admin_count = db.query(AdminUser).filter(AdminUser.role == "super_admin").count()
        if super_admin_count <= 1:
            raise HTTPException(status_code=400, detail="Cannot delete the last super admin")
    
    # Set created_by to NULL for any admins created by this admin (handle FK constraint)
    db.query(AdminUser).filter(AdminUser.created_by == admin_id).update({"created_by": None})
    
    db.delete(target_admin)
    db.commit()
    
    return {"message": "Admin deleted successfully"}


@router.delete("/me")
async def delete_own_account(
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete own admin account (available to all admins)."""
    # Check if this is the last super admin
    if admin.role == "super_admin":
        super_admin_count = db.query(AdminUser).filter(AdminUser.role == "super_admin").count()
        if super_admin_count <= 1:
            raise HTTPException(
                status_code=400, 
                detail="Cannot delete your account - you are the last super admin. Create another super admin first or promote an existing admin."
            )
    
    # Set created_by to NULL for any admins created by this admin (handle FK constraint)
    db.query(AdminUser).filter(AdminUser.created_by == admin.id).update({"created_by": None})
    
    db.delete(admin)
    db.commit()
    
    return {"message": "Your account has been deleted successfully"}


@router.get("/audit-logs")
async def get_audit_logs(
    action: Optional[str] = None,
    actor_type: Optional[str] = None,
    page: int = 1,
    per_page: int = 50,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get audit logs."""
    query = db.query(AuditLog)
    
    if action:
        query = query.filter(AuditLog.action == action)
    if actor_type:
        query = query.filter(AuditLog.actor_type == actor_type)
    
    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "action": log.action,
                "actor_type": log.actor_type,
                "actor_id": log.actor_id,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "description": log.description,
                "success": log.success,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
        }
    }
