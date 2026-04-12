from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId

from app.database.client import get_db
from app.services.audit_service import audit_service
from app.utils.dependencies import require_super_admin_dep

router = APIRouter(prefix="/admin/audit", tags=["audit"])


@router.get("/logs")
async def get_audit_logs(
    actor_type: str | None = Query(None, description="Filter by actor type"),
    entity_type: str | None = Query(None, description="Filter by entity type"),
    entity_id: str | None = Query(None, description="Filter by entity ID"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    admin=Depends(require_super_admin_dep),
):
    """Get audit logs (Super Admin only)"""
    logs = await audit_service.get_audit_logs(
        actor_type=actor_type,
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit,
        skip=skip
    )
    return {"logs": logs}


@router.get("/entity/{entity_type}/{entity_id}")
async def get_entity_history(
    entity_type: str,
    entity_id: str,
    limit: int = Query(20, ge=1, le=100),
    admin=Depends(require_super_admin_dep),
):
    """Get full history for a specific entity (Super Admin only)"""
    logs = await audit_service.get_entity_history(
        entity_type=entity_type,
        entity_id=entity_id,
        limit=limit
    )
    return {"logs": logs}
