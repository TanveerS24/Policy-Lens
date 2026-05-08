"""Notification endpoints."""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.notification import Notification, PushToken, UserBroadcast
from app.models.user import User
from app.models.scheme import Scheme
from app.models.admin import AdminUser
from app.api.v1.endpoints.patients import get_current_user
from app.api.v1.endpoints.admin import get_current_admin

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


# Admin Broadcast Schemas
class BroadcastCreateRequest(BaseModel):
    title: str
    message: str
    scheme_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None  # None for immediate
    target_all_users: bool = True
    target_user_ids: Optional[List[int]] = None


class BroadcastResponse(BaseModel):
    id: int
    title: str
    message: str
    scheme_id: Optional[int]
    scheme_name: Optional[str]
    scheduled_at: Optional[str]
    sent_at: Optional[str]
    status: str
    target_all_users: bool
    total_users: int
    sent_count: int
    failed_count: int
    created_at: str
    admin_name: str


class BroadcastListResponse(BaseModel):
    broadcasts: List[BroadcastResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


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


# Admin Broadcast Endpoints
@router.post("/broadcast", response_model=BroadcastResponse)
async def create_broadcast(
    request: BroadcastCreateRequest,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new broadcast notification."""
    
    # Validate scheme if provided
    scheme_name = None
    if request.scheme_id:
        scheme = db.query(Scheme).filter(Scheme.id == request.scheme_id).first()
        if not scheme:
            raise HTTPException(status_code=404, detail="Scheme not found")
        scheme_name = scheme.name
    
    # Get total user count for targeting
    user_count = db.query(User).filter(User.is_active == True).count()
    
    broadcast = UserBroadcast(
        admin_id=admin.id,
        title=request.title,
        message=request.message,
        scheme_id=request.scheme_id,
        scheduled_at=request.scheduled_at,
        target_all_users=request.target_all_users,
        target_user_ids=request.target_user_ids,
        total_users=user_count,
        status="scheduled" if request.scheduled_at else "sent"
    )
    
    db.add(broadcast)
    db.commit()
    db.refresh(broadcast)
    
    # If immediate, create notifications for all users
    if not request.scheduled_at:
        await send_broadcast_notifications(broadcast, db)
    
    return {
        "id": broadcast.id,
        "title": broadcast.title,
        "message": broadcast.message,
        "scheme_id": broadcast.scheme_id,
        "scheme_name": scheme_name,
        "scheduled_at": broadcast.scheduled_at.isoformat() if broadcast.scheduled_at else None,
        "sent_at": broadcast.sent_at.isoformat() if broadcast.sent_at else None,
        "status": broadcast.status,
        "target_all_users": broadcast.target_all_users,
        "total_users": broadcast.total_users,
        "sent_count": broadcast.sent_count,
        "failed_count": broadcast.failed_count,
        "created_at": broadcast.created_at.isoformat(),
        "admin_name": admin.name
    }


@router.get("/broadcast", response_model=BroadcastListResponse)
async def get_broadcasts(
    page: int = 1,
    per_page: int = 20,
    status: Optional[str] = None,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all broadcast notifications."""
    query = db.query(UserBroadcast).filter(UserBroadcast.admin_id == admin.id)
    
    if status:
        query = query.filter(UserBroadcast.status == status)
    
    total = query.count()
    broadcasts = query.order_by(UserBroadcast.created_at.desc()).offset(
        (page - 1) * per_page
    ).limit(per_page).all()
    
    return {
        "broadcasts": [
            {
                "id": b.id,
                "title": b.title,
                "message": b.message,
                "scheme_id": b.scheme_id,
                "scheme_name": b.scheme.name if b.scheme else None,
                "scheduled_at": b.scheduled_at.isoformat() if b.scheduled_at else None,
                "sent_at": b.sent_at.isoformat() if b.sent_at else None,
                "status": b.status,
                "target_all_users": b.target_all_users,
                "total_users": b.total_users,
                "sent_count": b.sent_count,
                "failed_count": b.failed_count,
                "created_at": b.created_at.isoformat(),
                "admin_name": b.admin.name
            }
            for b in broadcasts
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }


@router.get("/broadcast/{broadcast_id}", response_model=BroadcastResponse)
async def get_broadcast(
    broadcast_id: int,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get a specific broadcast notification."""
    broadcast = db.query(UserBroadcast).filter(
        UserBroadcast.id == broadcast_id,
        UserBroadcast.admin_id == admin.id
    ).first()
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    return {
        "id": broadcast.id,
        "title": broadcast.title,
        "message": broadcast.message,
        "scheme_id": broadcast.scheme_id,
        "scheme_name": broadcast.scheme.name if broadcast.scheme else None,
        "scheduled_at": broadcast.scheduled_at.isoformat() if broadcast.scheduled_at else None,
        "sent_at": broadcast.sent_at.isoformat() if broadcast.sent_at else None,
        "status": broadcast.status,
        "target_all_users": broadcast.target_all_users,
        "total_users": broadcast.total_users,
        "sent_count": broadcast.sent_count,
        "failed_count": broadcast.failed_count,
        "created_at": broadcast.created_at.isoformat(),
        "admin_name": broadcast.admin.name
    }


@router.patch("/broadcast/{broadcast_id}/cancel")
async def cancel_broadcast(
    broadcast_id: int,
    admin: AdminUser = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Cancel a scheduled broadcast."""
    broadcast = db.query(UserBroadcast).filter(
        UserBroadcast.id == broadcast_id,
        UserBroadcast.admin_id == admin.id
    ).first()
    
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    if broadcast.status == "sent":
        raise HTTPException(status_code=400, detail="Cannot cancel sent broadcast")
    
    broadcast.status = "cancelled"
    db.commit()
    
    return {"message": "Broadcast cancelled successfully"}


async def send_broadcast_notifications(broadcast: UserBroadcast, db: Session):
    """Send broadcast notifications to all target users."""
    users_query = db.query(User).filter(User.is_active == True)
    
    if not broadcast.target_all_users and broadcast.target_user_ids:
        users_query = users_query.filter(User.id.in_(broadcast.target_user_ids))
    
    users = users_query.all()
    
    sent_count = 0
    failed_count = 0
    
    for user in users:
        try:
            notification = Notification(
                user_id=user.id,
                title=broadcast.title,
                message=broadcast.message,
                notification_type="admin_broadcast",
                related_type="scheme" if broadcast.scheme_id else None,
                related_id=broadcast.scheme_id,
                deep_link=f"/scheme/{broadcast.scheme_id}" if broadcast.scheme_id else None
            )
            db.add(notification)
            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to send notification to user {user.id}: {e}")
    
    db.commit()
    
    # Update broadcast stats
    broadcast.sent_count = sent_count
    broadcast.failed_count = failed_count
    broadcast.sent_at = datetime.utcnow()
    broadcast.status = "sent"
    db.commit()
