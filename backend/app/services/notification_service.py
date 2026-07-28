"""Notification service for managing in-app, admin, and expired notification cleanup."""

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import structlog

from app.models.notification import Notification, OTP
from app.models.admin import AdminNotification

logger = structlog.get_logger()


def purge_old_notifications(db: Session, days: int = 30) -> int:
    """
    Automatically delete all notifications (user and admin notifications) 
    and expired OTP logs that are older than `days` (default 30 days / 1 month).
    """
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # 1. Delete user notifications older than 30 days
        deleted_user_notes = db.query(Notification).filter(
            Notification.created_at < cutoff_date
        ).delete(synchronize_session=False)

        # 2. Delete admin notifications older than 30 days
        deleted_admin_notes = db.query(AdminNotification).filter(
            AdminNotification.created_at < cutoff_date
        ).delete(synchronize_session=False)

        # 3. Delete OTPs older than 30 days
        deleted_otps = db.query(OTP).filter(
            OTP.created_at < cutoff_date
        ).delete(synchronize_session=False)

        total_deleted = deleted_user_notes + deleted_admin_notes
        
        if total_deleted > 0 or deleted_otps > 0:
            db.commit()
            logger.info(
                "purged_old_notifications",
                deleted_user_notifications=deleted_user_notes,
                deleted_admin_notifications=deleted_admin_notes,
                deleted_otps=deleted_otps,
                cutoff_date=cutoff_date.isoformat()
            )
            
        return total_deleted

    except Exception as e:
        db.rollback()
        logger.error("failed_to_purge_old_notifications", error=str(e))
        return 0
