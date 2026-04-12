from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.database.client import get_db
from app.models.eligibility_rule import (
    EligibilityCheckRequest,
    EligibilityCheckResult,
    EligibilityRuleCreate,
    EligibilityRuleInDB,
    EligibilityRulePublic,
    EligibilityRuleUpdate,
)
from app.services.eligibility_service import eligibility_service
from app.utils.dependencies import get_current_patient, get_current_admin_user_dep, require_content_admin_dep

router = APIRouter(prefix="/eligibility", tags=["eligibility"])


@router.post("/check", response_model=EligibilityCheckResult)
async def check_eligibility(
    request: EligibilityCheckRequest,
    patient=Depends(get_current_patient),
    db=Depends(get_db),
):
    """Check eligibility for a scheme (Patient only)"""
    result = await eligibility_service.check_eligibility(request, str(patient.id))
    return result


@router.get("/schemes/{scheme_id}/rules")
async def get_scheme_rules(scheme_id: str, db=Depends(get_db)):
    """Get all rules for a scheme (public endpoint)"""
    if not ObjectId.is_valid(scheme_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheme id")
    
    cursor = db["eligibility_rules"].find({"scheme_id": scheme_id, "active": True}).sort("rule_name", 1)
    rules = [rule async for rule in cursor]
    
    return {"rules": rules}


# Admin endpoints
@router.post("/admin/rules")
async def create_rule(
    request: EligibilityRuleCreate,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Create new eligibility rule (Admin - Content Admin+)"""
    try:
        rule_id = await eligibility_service.create_rule(db, request.dict(), admin["id"])
        return {"id": rule_id}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/admin/rules/{rule_id}")
async def update_rule(
    rule_id: str,
    request: EligibilityRuleUpdate,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Update eligibility rule (Admin - Content Admin+)"""
    try:
        await eligibility_service.update_rule(db, rule_id, request.dict(exclude_unset=True), admin["id"])
        return {"updated": True}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/admin/rules/{rule_id}")
async def delete_rule(
    rule_id: str,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Delete eligibility rule (Admin - Content Admin+)"""
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid rule id")
    
    await db["eligibility_rules"].delete_one({"_id": ObjectId(rule_id)})
    return {"deleted": True}


@router.get("/admin/rules/{rule_id}/versions")
async def get_rule_versions(
    rule_id: str,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Get rule version history (Admin - Content Admin+)"""
    try:
        versions = await eligibility_service.get_rule_versions(db, rule_id)
        return {"versions": versions}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/admin/rules/{rule_id}/rollback/{version}")
async def rollback_rule(
    rule_id: str,
    version: int,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Rollback rule to specific version (Admin - Content Admin+)"""
    if not ObjectId.is_valid(rule_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid rule id")
    
    # Get version snapshot
    version_snapshot = await db["eligibility_rule_versions"].find_one({
        "rule_id": rule_id,
        "version_number": version
    })
    
    if not version_snapshot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")
    
    snapshot = version_snapshot["snapshot"]
    current_rule = await db["eligibility_rules"].find_one({"_id": ObjectId(rule_id)})
    
    if not current_rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    
    # Create new version with rollback data
    new_version = current_rule.get("version", 1) + 1
    
    await db["eligibility_rule_versions"].insert_one({
        "rule_id": rule_id,
        "version_number": current_rule.get("version", 1),
        "snapshot": current_rule,
        "changed_by": admin["id"],
        "changed_at": "rollback"
    })
    
    # Update rule with rollback data
    snapshot["version"] = new_version
    snapshot["updated_at"] = "rollback"
    await db["eligibility_rules"].update_one(
        {"_id": ObjectId(rule_id)},
        {"$set": snapshot}
    )
    
    return {"rolled_back": True, "new_version": new_version}
