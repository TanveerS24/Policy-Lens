"""Scheme endpoints."""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.config.database import get_db
from app.models.scheme import Scheme, SchemeBookmark
from app.models.user import User
from app.api.v1.endpoints.patients import get_current_user

router = APIRouter()
security = HTTPBearer()


# Schemas
class SchemeFilter(BaseModel):
    type: Optional[str] = None  # state, national, central
    state: Optional[str] = None
    category: Optional[str] = None  # BPL, Women, etc.
    service: Optional[str] = None  # Extraction, Dentures
    search: Optional[str] = None
    page: int = 1
    per_page: int = 20


class BookmarkRequest(BaseModel):
    scheme_id: int
    enable_notifications: bool = True


# Endpoints
@router.get("")
async def list_schemes(
    type: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    service: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List schemes with filters and pagination."""
    query = db.query(Scheme).filter(Scheme.is_deleted == False, Scheme.status == "active")
    
    # Apply filters
    if type:
        query = query.filter(Scheme.type == type)
    if state:
        query = query.filter(
            (Scheme.state == state) | (Scheme.target_states.contains([state]))
        )
    if category:
        query = query.filter(Scheme.target_categories.contains([category]))
    if service:
        query = query.filter(Scheme.services_covered.contains([service]))
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            Scheme.name.ilike(search_filter) |
            Scheme.description.ilike(search_filter) |
            Scheme.ministry.ilike(search_filter)
        )
    
    # Get total count
    total = query.count()
    
    # Pagination
    schemes = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # Get bookmarked scheme IDs for user
    bookmarked_ids = set()
    if user:
        bookmarks = db.query(SchemeBookmark).filter(SchemeBookmark.user_id == user.id).all()
        bookmarked_ids = {b.scheme_id for b in bookmarks}
    
    return {
        "schemes": [
            {
                **scheme.to_dict(),
                "is_bookmarked": scheme.id in bookmarked_ids
            }
            for scheme in schemes
        ],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
        }
    }


@router.get("/{scheme_id}")
async def get_scheme(
    scheme_id: int,
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed scheme information."""
    scheme = db.query(Scheme).filter(
        Scheme.id == scheme_id,
        Scheme.is_deleted == False
    ).first()
    
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Check if bookmarked
    is_bookmarked = False
    if user:
        bookmark = db.query(SchemeBookmark).filter(
            SchemeBookmark.user_id == user.id,
            SchemeBookmark.scheme_id == scheme_id
        ).first()
        is_bookmarked = bookmark is not None
    
    result = scheme.to_dict()
    result["is_bookmarked"] = is_bookmarked
    
    return result


@router.get("/{scheme_id}/eligibility")
async def get_scheme_eligibility(
    scheme_id: int,
    age: Optional[int] = Query(None),
    income: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Check eligibility for a specific scheme."""
    scheme = db.query(Scheme).filter(
        Scheme.id == scheme_id,
        Scheme.is_deleted == False
    ).first()
    
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Simple eligibility check based on provided criteria
    checks = {
        "age": True,
        "income": True,
        "state": True,
        "category": True,
        "gender": True,
    }
    
    failed_conditions = []
    
    if age is not None and scheme.min_age is not None and age < scheme.min_age:
        checks["age"] = False
        failed_conditions.append(f"Minimum age is {scheme.min_age}")
    
    if age is not None and scheme.max_age is not None and age > scheme.max_age:
        checks["age"] = False
        failed_conditions.append(f"Maximum age is {scheme.max_age}")
    
    if state and scheme.target_states and state not in scheme.target_states:
        checks["state"] = False
        failed_conditions.append(f"Only available in: {', '.join(scheme.target_states)}")
    
    # Determine result
    if all(checks.values()):
        result = "likely_eligible"
    elif failed_conditions:
        result = "not_eligible" if len(failed_conditions) > 2 else "possibly_eligible"
    else:
        result = "more_info_needed"
    
    return {
        "scheme_id": scheme_id,
        "result": result,
        "checks": checks,
        "failed_conditions": failed_conditions,
        "required_documents": scheme.required_documents,
        "next_steps": [
            "Visit the official website for application",
            "Gather required documents",
            "Contact helpline for assistance"
        ] if result != "not_eligible" else None
    }


@router.post("/bookmark")
async def bookmark_scheme(
    request: BookmarkRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Bookmark a scheme."""
    # Check if scheme exists
    scheme = db.query(Scheme).filter(Scheme.id == request.scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Check if already bookmarked
    existing = db.query(SchemeBookmark).filter(
        SchemeBookmark.user_id == user.id,
        SchemeBookmark.scheme_id == request.scheme_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Scheme already bookmarked")
    
    bookmark = SchemeBookmark(
        user_id=user.id,
        scheme_id=request.scheme_id,
        notifications_enabled=request.enable_notifications
    )
    db.add(bookmark)
    db.commit()
    
    return {"message": "Scheme bookmarked successfully"}


@router.delete("/{scheme_id}/bookmark")
async def remove_bookmark(
    scheme_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a scheme bookmark."""
    bookmark = db.query(SchemeBookmark).filter(
        SchemeBookmark.user_id == user.id,
        SchemeBookmark.scheme_id == scheme_id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    
    return {"message": "Bookmark removed successfully"}


@router.get("/my/bookmarks")
async def get_my_bookmarks(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's bookmarked schemes."""
    bookmarks = db.query(SchemeBookmark).filter(
        SchemeBookmark.user_id == user.id
    ).all()
    
    scheme_ids = [b.scheme_id for b in bookmarks]
    schemes = db.query(Scheme).filter(Scheme.id.in_(scheme_ids)).all()
    
    scheme_map = {s.id: s for s in schemes}
    
    return {
        "bookmarks": [
            {
                "id": b.id,
                "scheme": scheme_map.get(b.scheme_id).to_dict() if b.scheme_id in scheme_map else None,
                "notifications_enabled": b.notifications_enabled,
                "created_at": b.created_at.isoformat() if b.created_at else None,
            }
            for b in bookmarks
        ]
    }
