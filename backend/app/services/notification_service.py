"""Notification service for managing in-app, admin, and expired notification cleanup."""

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import structlog

from app.models.notification import Notification, OTP, UserBroadcast
from app.models.admin import AdminNotification
from app.models.user import User

logger = structlog.get_logger()


def process_scheduled_broadcasts(db: Session) -> int:
    """
    Find and dispatch all scheduled broadcasts whose scheduled_at timestamp has arrived.
    """
    try:
        now_utc = datetime.now(timezone.utc)
        now_naive = now_utc.replace(tzinfo=None)

        # Query pending scheduled broadcasts
        pending_broadcasts = db.query(UserBroadcast).filter(
            UserBroadcast.status == "scheduled",
            UserBroadcast.is_active == True
        ).all()

        processed_count = 0
        for broadcast in pending_broadcasts:
            if not broadcast.scheduled_at:
                continue

            # Check if scheduled time has arrived (timezone safe)
            sched_time = broadcast.scheduled_at
            if sched_time.tzinfo is not None:
                is_due = sched_time <= now_utc
            else:
                is_due = sched_time <= now_naive

            if is_due:
                # Target users
                users_query = db.query(User).filter(User.is_active == True)
                if not broadcast.target_all_users and broadcast.target_user_ids:
                    users_query = users_query.filter(User.id.in_(broadcast.target_user_ids))

                users = users_query.all()
                sent_count = 0
                failed_count = 0

                for user in users:
                    try:
                        notif = Notification(
                            user_id=user.id,
                            title=broadcast.title,
                            message=broadcast.message,
                            notification_type="admin_broadcast",
                            related_type="scheme" if broadcast.scheme_id else None,
                            related_id=broadcast.scheme_id,
                            deep_link=f"/scheme/{broadcast.scheme_id}" if broadcast.scheme_id else None
                        )
                        db.add(notif)
                        sent_count += 1
                    except Exception as err:
                        failed_count += 1
                        logger.warning("scheduled_broadcast_item_failed", user_id=user.id, error=str(err))

                broadcast.sent_count = sent_count
                broadcast.failed_count = failed_count
                broadcast.sent_at = now_utc
                broadcast.status = "sent"
                db.commit()
                processed_count += 1
                logger.info("processed_scheduled_broadcast", broadcast_id=broadcast.id, sent_count=sent_count)

        return processed_count

    except Exception as e:
        db.rollback()
        logger.error("failed_to_process_scheduled_broadcasts", error=str(e))
        return 0


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

