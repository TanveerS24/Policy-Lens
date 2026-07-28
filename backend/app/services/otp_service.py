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

    def count_recent_requests(self, db: Session, target: str, hours: int = 1) -> int:
        """Count recent OTP requests for rate limiting (by email or mobile)."""
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        count = db.query(OTP).filter(
            ((OTP.email == target) | (OTP.mobile == target)),
            OTP.created_at >= since
        ).count()
        return count

    def verify_otp(self, db: Session, target: str, otp_code: str) -> bool:
        """Verify an OTP code by email or mobile."""
        if not target or not otp_code:
            return False

        otp_record = db.query(OTP).filter(
            ((OTP.email == target) | (OTP.mobile == target)),
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
        import structlog
        logger = structlog.get_logger()
        logger.info("sms_placeholder", mobile=mobile, message_length=len(message))
        return True

    def send_email_otp(self, email: str, otp_code: str) -> bool:
        """
        Send OTP code via SMTP email if configured, or log for development simulation.
        """
        import structlog
        logger = structlog.get_logger()

        if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart

                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"Your Verification Code - {settings.APP_NAME}"
                msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
                msg["To"] = email

                html_body = f"""
                <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
                  <h2>Verification Code</h2>
                  <p>Use the following 6-digit OTP code to complete your verification:</p>
                  <div style="font-size: 28px; font-weight: bold; letter-spacing: 4px; color: #2563EB; margin: 20px 0;">
                    {otp_code}
                  </div>
                  <p>This code will expire in {settings.OTP_EXPIRE_MINUTES} minutes.</p>
                </div>
                """
                msg.attach(MIMEText(html_body, "html"))

                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.sendmail(settings.EMAILS_FROM_EMAIL, [email], msg.as_string())

                logger.info("otp_email_sent_smtp", email=email)
                return True
            except Exception as e:
                logger.error("otp_email_smtp_failed", error=str(e), email=email)
                return False
        else:
            logger.info("otp_email_simulated", email=email, otp_code=otp_code)
            return True
