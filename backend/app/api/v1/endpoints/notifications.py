"""Notification endpoints."""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.notification import Notification, PushToken
from app.models.user import User
from app.api.v1.endpoints.patients import get_current_user

router = APIRouter()


# Schemas
class PushTokenRequest(BaseModel):
    token: str
    platform: str  # ios, android


class NotificationListResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: str
    deep_link: Optional[str]


# Endpoints
@router.get("")
async def get_notifications(
    unread_only: bool = False,
    page: int = 1,
    per_page: int = 20,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notifications."""
    query = db.query(Notification).filter(Notification.user_id == user.id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    total = query.count()
    notifications = query.order_by(Notification.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()
    
    return {
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "notification_type": n.notification_type,
                "is_read": n.is_read,
                "read_at": n.read_at.isoformat() if n.read_at else None,
                "created_at": n.created_at.isoformat() if n.created_at else None,
                "deep_link": n.deep_link,
                "related_type": n.related_type,
                "related_id": n.related_id,
            }
            for n in notifications
        ],
        "unread_count": db.query(Notification).filter(
            Notification.user_id == user.id,
            Notification.is_read == False
        ).count(),
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
        }
    }


@router.patch("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}


@router.post("/mark-all-read")
async def mark_all_notifications_read(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read."""
    db.query(Notification).filter(
        Notification.user_id == user.id,
        Notification.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })
    db.commit()
    
    return {"message": "All notifications marked as read"}


@router.post("/push-token")
async def register_push_token(
    request: PushTokenRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register FCM/APNs push token."""
    # Check if token already exists
    existing = db.query(PushToken).filter(PushToken.token == request.token).first()
    
    if existing:
        # Update user association
        existing.user_id = user.id
        existing.platform = request.platform
        existing.is_active = True
        existing.last_used_at = datetime.utcnow()
    else:
        token = PushToken(
            user_id=user.id,
            token=request.token,
            platform=request.platform,
        )
        db.add(token)
    
    db.commit()
    
    return {"message": "Push token registered successfully"}


@router.delete("/push-token")
async def unregister_push_token(
    token: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unregister push token."""
    push_token = db.query(PushToken).filter(
        PushToken.token == token,
        PushToken.user_id == user.id
    ).first()
    
    if push_token:
        push_token.is_active = False
        db.commit()
    
    return {"message": "Push token unregistered"}
