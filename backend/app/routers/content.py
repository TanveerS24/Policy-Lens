from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from datetime import datetime

from app.database.client import get_db
from app.models.content import FAQCreate, FAQUpdate, BannerCreate, BannerUpdate
from app.utils.dependencies import require_content_admin_dep, require_super_admin_dep

router = APIRouter(prefix="/content", tags=["content"])


# Public endpoints
@router.get("/faqs")
async def list_faqs(
    category: str | None = Query(None, description="Filter by category"),
    active_only: bool = Query(True, description="Filter to only active FAQs"),
    db=Depends(get_db),
):
    """List FAQs (public endpoint)"""
    query: dict = {}
    if category:
        query["category"] = category
    if active_only:
        query["active"] = True
    
    cursor = db["faqs"].find(query).sort([("display_order", 1), ("category", 1)])
    faqs = [faq async for faq in cursor]
    
    return {"faqs": faqs}


@router.get("/banners")
async def list_banners(
    active_only: bool = Query(True, description="Filter to only active banners"),
    db=Depends(get_db),
):
    """List banners (public endpoint)"""
    query: dict = {}
    if active_only:
        query["active"] = True
        query["start_date"] = {"$lte": datetime.utcnow()}
        query["end_date"] = {"$gte": datetime.utcnow()}
    
    cursor = db["banners"].find(query).sort([("display_order", 1)])
    banners = [banner async for banner in cursor]
    
    return {"banners": banners}


# Admin endpoints
@router.post("/admin/faqs")
async def create_faq(
    request: FAQCreate,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Create new FAQ (Content Admin+)"""
    faq_doc = request.dict()
    faq_doc.update({
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db["faqs"].insert_one(faq_doc)
    return {"id": str(result.inserted_id)}


@router.put("/admin/faqs/{faq_id}")
async def update_faq(
    faq_id: str,
    request: FAQUpdate,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Update FAQ (Content Admin+)"""
    if not ObjectId.is_valid(faq_id):
        raise HTTPException(status_code=400, detail="Invalid FAQ id")
    
    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db["faqs"].update_one(
        {"_id": ObjectId(faq_id)},
        {"$set": update_data}
    )
    
    return {"updated": True}


@router.delete("/admin/faqs/{faq_id}")
async def delete_faq(
    faq_id: str,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Delete FAQ (Content Admin+)"""
    if not ObjectId.is_valid(faq_id):
        raise HTTPException(status_code=400, detail="Invalid FAQ id")
    
    await db["faqs"].delete_one({"_id": ObjectId(faq_id)})
    return {"deleted": True}


@router.post("/admin/banners")
async def create_banner(
    request: BannerCreate,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Create new banner (Content Admin+)"""
    banner_doc = request.dict()
    banner_doc.update({
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db["banners"].insert_one(banner_doc)
    return {"id": str(result.inserted_id)}


@router.put("/admin/banners/{banner_id}")
async def update_banner(
    banner_id: str,
    request: BannerUpdate,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Update banner (Content Admin+)"""
    if not ObjectId.is_valid(banner_id):
        raise HTTPException(status_code=400, detail="Invalid banner id")
    
    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db["banners"].update_one(
        {"_id": ObjectId(banner_id)},
        {"$set": update_data}
    )
    
    return {"updated": True}


@router.delete("/admin/banners/{banner_id}")
async def delete_banner(
    banner_id: str,
    db=Depends(get_db),
    admin=Depends(require_content_admin_dep),
):
    """Delete banner (Content Admin+)"""
    if not ObjectId.is_valid(banner_id):
        raise HTTPException(status_code=400, detail="Invalid banner id")
    
    await db["banners"].delete_one({"_id": ObjectId(banner_id)})
    return {"deleted": True}
