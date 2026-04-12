from fastapi import APIRouter, Depends, Query
from bson import ObjectId

from app.database.client import get_db
from app.models.notification import NotificationCreate, NotificationTypeEnum
from app.services.notification_service import notification_service
from app.utils.dependencies import get_current_patient

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("")
async def create_notification(
    request: NotificationCreate,
    db=Depends(get_db),
    patient=Depends(get_current_patient),
):
    """Create notification (patient can create for themselves)"""
    notification_id = await notification_service.create_notification(
        title=request.title,
        message=request.message,
        user_id=patient.id,
        notification_type=request.notification_type,
        link=request.link,
        data=request.data
    )
    return {"id": notification_id}


@router.get("")
async def get_notifications(
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    patient=Depends(get_current_patient),
):
    """Get user notifications"""
    return await notification_service.get_notifications(patient.id, limit, skip)


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    patient=Depends(get_current_patient),
):
    """Mark notification as read"""
    if not ObjectId.is_valid(notification_id):
        return {"error": "Invalid notification id"}
    return await notification_service.mark_as_read(notification_id, patient.id)


@router.post("/read-all")
async def mark_all_as_read(patient=Depends(get_current_patient)):
    """Mark all notifications as read"""
    return await notification_service.mark_all_as_read(patient.id)


@router.get("/unread-count")
async def get_unread_count(patient=Depends(get_current_patient)):
    """Get unread notification count"""
    return await notification_service.get_unread_count(patient.id)
