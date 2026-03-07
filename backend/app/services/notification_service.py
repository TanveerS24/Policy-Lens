"""
Notification Service
Send notifications to users
"""

from typing import Optional, List
from datetime import datetime
from app.database.mongodb import get_db
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotificationService:
    """Manage user notifications"""
    
    @staticmethod
    async def create_notification(
        user_id: Optional[str],
        title: str,
        message: str,
        notification_type: str,
    ) -> bool:
        """Create a notification"""
        try:
            db = get_db()
            
            notification_doc = {
                "user_id": user_id,
                "title": title,
                "message": message,
                "type": notification_type,
                "is_read": False,
                "created_at": datetime.utcnow(),
            }
            
            result = await db["notifications"].insert_one(notification_doc)
            logger.info(f"✅ Notification created: {title}")
            return True
        
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return False
    
    @staticmethod
    async def broadcast_notification(
        title: str,
        message: str,
        notification_type: str,
    ) -> bool:
        """Send notification to all users"""
        try:
            db = get_db()
            
            notification_doc = {
                "user_id": None,
                "title": title,
                "message": message,
                "type": notification_type,
                "is_read": False,
                "created_at": datetime.utcnow(),
            }
            
            result = await db["notifications"].insert_one(notification_doc)
            logger.info(f"✅ Broadcast notification sent: {title}")
            return True
        
        except Exception as e:
            logger.error(f"Error broadcasting notification: {e}")
            return False
    
    @staticmethod
    async def get_user_notifications(user_id: str, limit: int = 10) -> List[dict]:
        """Get notifications for user"""
        try:
            db = get_db()
            
            notifications = await db["notifications"].find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit).to_list(limit)
            
            return notifications
        
        except Exception as e:
            logger.error(f"Error fetching notifications: {e}")
            return []
    
    @staticmethod
    async def mark_as_read(notification_id: str) -> bool:
        """Mark notification as read"""
        try:
            from bson import ObjectId
            
            db = get_db()
            
            await db["notifications"].update_one(
                {"_id": ObjectId(notification_id)},
                {"$set": {"is_read": True}}
            )
            
            return True
        
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False
