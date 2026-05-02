"""Audit logging models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.config.database import Base


class AuditAction(PyEnum):
    """Audit action enumeration."""
    # Auth actions
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    MFA_VERIFY = "mfa_verify"
    
    # User actions
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    PROFILE_UPDATE = "profile_update"
    
    # Scheme actions
    SCHEME_CREATE = "scheme_create"
    SCHEME_UPDATE = "scheme_update"
    SCHEME_DELETE = "scheme_delete"
    SCHEME_RESTORE = "scheme_restore"
    
    # Document actions
    DOCUMENT_UPLOAD = "document_upload"
    DOCUMENT_DELETE = "document_delete"
    AI_SUMMARY_GENERATED = "ai_summary_generated"
    
    # Admin actions
    ADMIN_CREATE = "admin_create"
    ADMIN_UPDATE = "admin_update"
    ADMIN_DELETE = "admin_delete"
    ADMIN_ROLE_CHANGE = "admin_role_change"
    
    # System actions
    SYSTEM_CONFIG_UPDATE = "system_config_update"
    BULK_IMPORT = "bulk_import"
    BULK_EXPORT = "bulk_export"
    
    # Other
    ELIGIBILITY_CHECK = "eligibility_check"
    BOOKMARK_CREATE = "bookmark_create"
    NOTIFICATION_SEND = "notification_send"


class AuditLog(Base):
    """Comprehensive audit log."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Actor (who performed the action)
    actor_type = Column(String(20), nullable=False)  # user, admin, system
    actor_id = Column(Integer, nullable=True)
    
    # Admin relationship (if action by admin)
    admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=True)
    
    # Action details
    action = Column(String(50), nullable=False)
    resource_type = Column(String(50), nullable=False)  # user, scheme, document, etc.
    resource_id = Column(Integer, nullable=True)
    
    # Request context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    request_path = Column(String(255), nullable=True)
    request_method = Column(String(10), nullable=True)
    
    # Data (before/after for changes)
    data_before = Column(JSON, nullable=True)
    data_after = Column(JSON, nullable=True)
    
    # Additional context
    description = Column(Text, nullable=True)
    meta_data = Column(JSON, default=dict)
    
    # Result
    success = Column(String(20), default="success")  # success, failed, error
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    admin = relationship("AdminUser", back_populates="audit_logs")


class SecurityEvent(Base):
    """Security-specific events."""
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True)
    
    event_type = Column(String(50), nullable=False)  # suspicious_login, brute_force, data_export
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    
    # Actor
    actor_type = Column(String(20), nullable=True)
    actor_id = Column(Integer, nullable=True)
    
    # Details
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    description = Column(Text, nullable=False)
    
    # Context
    context = Column(JSON, default=dict)
    
    # Status
    is_resolved = Column(String(20), default="open")  # open, investigating, resolved, false_positive
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class DataExportLog(Base):
    """Log of data exports (DPDP compliance)."""
    __tablename__ = "data_export_logs"
    
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Export details
    export_type = Column(String(50), nullable=False)  # full_data, partial
    request_reason = Column(String(255), nullable=True)
    
    # File info
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    
    # Timestamps
    requested_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    downloaded_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
