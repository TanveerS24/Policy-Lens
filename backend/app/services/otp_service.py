"""OTP service."""

import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.models.notification import OTP

settings = get_settings()


class OTPService:
    """Service for OTP generation and verification."""

    def generate_otp(self, length: int = 6) -> str:
        """Generate a cryptographically secure random OTP."""
        digits = "0123456789"
        return ''.join(secrets.choice(digits) for _ in range(length))

    def count_recent_requests(self, db: Session, mobile: str, hours: int = 1) -> int:
        """Count recent OTP requests for rate limiting."""
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        count = db.query(OTP).filter(
            OTP.mobile == mobile,
            OTP.created_at >= since
        ).count()
        return count

    def verify_otp(self, db: Session, mobile: str, otp_code: str) -> bool:
        """Verify an OTP code."""
        otp_record = db.query(OTP).filter(
            OTP.mobile == mobile,
            OTP.otp_code == otp_code,
            OTP.is_used == False,
            OTP.expires_at > datetime.now(timezone.utc)
        ).first()

        if not otp_record:
            return False

        # Check attempts
        if otp_record.attempts >= otp_record.max_attempts:
            return False

        # Increment attempts
        otp_record.attempts += 1

        # Mark as used if valid
        if otp_record.otp_code == otp_code:
            otp_record.is_used = True
            otp_record.used_at = datetime.now(timezone.utc)
            db.commit()
            return True

        db.commit()
        return False

    def send_sms(self, mobile: str, message: str) -> bool:
        """Send SMS (placeholder — integrate with actual SMS provider)."""
        # TODO: Integrate with SMS provider (Twilio, Msg91, etc.)
        import structlog
        logger = structlog.get_logger()
        logger.info("sms_placeholder", mobile=mobile, message_length=len(message))
        return True
