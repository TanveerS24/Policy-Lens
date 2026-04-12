from typing import Optional, List
from datetime import datetime

from app.database.client import get_db
from app.models.notification import NotificationTypeEnum, NotificationStatusEnum
from app.services.sms_service import sms_service


class NotificationService:
    async def create_notification(
        self,
        title: str,
        message: str,
        user_id: Optional[str] = None,
        notification_type: NotificationTypeEnum = NotificationTypeEnum.IN_APP,
        link: Optional[str] = None,
        data: Optional[dict] = None
    ):
        db = get_db()
        notification_doc = {
            "title": title,
            "message": message,
            "user_id": user_id,
            "notification_type": notification_type.value,
            "link": link,
            "data": data or {},
            "is_read": False,
            "status": NotificationStatusEnum.PENDING.value,
            "created_at": datetime.utcnow(),
            "delivery_attempts": 0
        }
        result = await db["notifications"].insert_one(notification_doc)
        
        # Trigger sending based on type
        if notification_type == NotificationTypeEnum.SMS and user_id:
            await self._send_sms_notification(str(result.inserted_id), user_id, message)
        elif notification_type == NotificationTypeEnum.PUSH and user_id:
            await self._send_push_notification(str(result.inserted_id), user_id, title, message, data)
        
        return str(result.inserted_id)
    
    async def _send_sms_notification(self, notification_id: str, user_id: str, message: str):
        """Send SMS notification via MSG91"""
        db = get_db()
        
        # Get user mobile
        user = await db["patients"].find_one({"_id": user_id})
        if not user:
            await self._mark_failed(notification_id, "User not found")
            return
        
        try:
            await sms_service.send_sms(user["mobile"], message)
            await self._mark_sent(notification_id)
        except Exception as e:
            await self._mark_failed(notification_id, str(e))
    
    async def _send_push_notification(self, notification_id: str, user_id: str, title: str, message: str, data: Optional[dict]):
        """Send push notification (placeholder - would integrate with FCM/APNs)"""
        db = get_db()
        
        # Placeholder for push notification integration
        # In production, this would integrate with Firebase Cloud Messaging or Apple Push Notification Service
        await self._mark_sent(notification_id)
    
    async def _mark_sent(self, notification_id: str):
        db = get_db()
        await db["notifications"].update_one(
            {"_id": notification_id},
            {
                "$set": {
                    "status": NotificationStatusEnum.SENT.value,
                    "sent_at": datetime.utcnow()
                }
            }
        )
    
    async def _mark_failed(self, notification_id: str, error_message: str):
        db = get_db()
        await db["notifications"].update_one(
            {"_id": notification_id},
            {
                "$set": {
                    "status": NotificationStatusEnum.FAILED.value,
                    "error_message": error_message,
                    "delivery_attempts": 1
                }
            }
        )
    
    async def get_notifications(self, user_id: str, limit: int = 50, skip: int = 0):
        db = get_db()
        query = {"user_id": user_id}
        total = await db["notifications"].count_documents(query)
        cursor = db["notifications"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
        notifications = [doc async for doc in cursor]
        return {"total": total, "notifications": notifications}
    
    async def mark_as_read(self, notification_id: str, user_id: str):
        db = get_db()
        await db["notifications"].update_one(
            {"_id": notification_id, "user_id": user_id},
            {
                "$set": {
                    "is_read": True,
                    "read_at": datetime.utcnow()
                }
            }
        )
        return {"read": True}
    
    async def mark_all_as_read(self, user_id: str):
        db = get_db()
        await db["notifications"].update_many(
            {"user_id": user_id, "is_read": False},
            {
                "$set": {
                    "is_read": True,
                    "read_at": datetime.utcnow()
                }
            }
        )
        return {"read": True}
    
    async def get_unread_count(self, user_id: str):
        db = get_db()
        count = await db["notifications"].count_documents({
            "user_id": user_id,
            "is_read": False
        })
        return {"unread_count": count}


notification_service = NotificationService()
