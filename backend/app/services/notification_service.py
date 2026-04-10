from typing import Optional

from app.database.client import get_db


class NotificationService:
    async def create_notification(self, title: str, message: str, user_id: Optional[str] = None, link: Optional[str] = None):
        db = get_db()
        return await db["notifications"].insert_one({
            "title": title,
            "message": message,
            "user_id": user_id,
            "link": link,
            "is_read": False,
        })

    async def get_notifications(self, user_id: str):
        db = get_db()
        cursor = db["notifications"].find({"user_id": user_id}).sort([("_id", -1)])
        return [doc async for doc in cursor]


notification_service = NotificationService()
