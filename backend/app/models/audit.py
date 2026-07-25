"""Audit logging models."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.config.database import Base


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

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

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

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


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
    requested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    downloaded_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
