"""Notification system models."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.config.database import Base


class Notification(Base):
    """User notification model."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)

    # Channels
    sms_sent = Column(Boolean, default=False)
    sms_sent_at = Column(DateTime, nullable=True)
    push_sent = Column(Boolean, default=False)
    push_sent_at = Column(DateTime, nullable=True)
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime, nullable=True)

    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)

    # Related data
    related_type = Column(String(50), nullable=True)  # scheme, document, etc.
    related_id = Column(Integer, nullable=True)
    action_data = Column(JSON, default=dict)

    # Deep link
    deep_link = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="notifications")


class OTP(Base):
    """OTP storage and tracking."""
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True)

    # Target
    mobile = Column(String(10), index=True, nullable=True)
    email = Column(String(255), index=True, nullable=True)

    # OTP details
    otp_code = Column(String(6), nullable=False)
    purpose = Column(String(50), nullable=False)  # registration, login, password_reset, mobile_change

    # Expiry
    expires_at = Column(DateTime, nullable=False)

    # Usage tracking
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)

    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)

    # Metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PushToken(Base):
    """FCM/FCM push notification tokens."""
    __tablename__ = "push_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    token = Column(String(500), nullable=False, unique=True)
    platform = Column(String(20), nullable=False)  # ios, android, web

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_used_at = Column(DateTime, nullable=True)


class UserBroadcast(Base):
    """Admin broadcast notifications to users."""
    __tablename__ = "user_broadcasts"

    id = Column(Integer, primary_key=True)

    # Admin who created the notification
    admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)

    # Content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)

    # Optional scheme attachment
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=True)

    # Scheduling
    scheduled_at = Column(DateTime, nullable=True)  # Null for immediate
    sent_at = Column(DateTime, nullable=True)      # When actually sent

    # Status
    status = Column(String(20), default="draft")  # draft, scheduled, sent, cancelled
    is_active = Column(Boolean, default=True)

    # Targeting
    target_all_users = Column(Boolean, default=True)
    target_user_ids = Column(JSON, nullable=True)  # For specific users

    # Delivery tracking
    total_users = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    admin = relationship("AdminUser", back_populates="user_broadcasts")
    scheme = relationship("Scheme", back_populates="user_broadcasts")
