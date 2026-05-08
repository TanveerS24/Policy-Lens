"""Admin user models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.config.database import Base


class AdminRole(PyEnum):
    """Admin role enumeration."""
    SUPER_ADMIN = "super_admin"
    CONTENT_ADMIN = "content_admin"
    SUPPORT_ADMIN = "support_admin"


class AdminStatus(PyEnum):
    """Admin account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class AdminUser(Base):
    """Admin user model."""
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Info
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Auth
    hashed_password = Column(String(255), nullable=False)
    
    # Role & Status
    role = Column(String(20), nullable=False, default="support_admin")
    status = Column(String(20), default="active")
    
    # MFA
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255), nullable=True)
    mfa_backup_codes = Column(JSON, default=list)
    
    # Security
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="admin")
    notifications = relationship("AdminNotification", back_populates="admin")
    user_broadcasts = relationship("UserBroadcast", back_populates="admin")


class AdminSession(Base):
    """Admin session tracking."""
    __tablename__ = "admin_sessions"
    
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)
    
    session_token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)


class AdminNotification(Base):
    """Notifications for admin users."""
    __tablename__ = "admin_notifications"
    
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)
    
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # system, alert, info
    
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    action_url = Column(String(255), nullable=True)
    action_data = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    admin = relationship("AdminUser", back_populates="notifications")
