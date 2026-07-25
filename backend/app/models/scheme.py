"""Dental scheme models."""

from datetime import datetime, date, timezone
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Boolean, ForeignKey, JSON, Numeric
from sqlalchemy.orm import relationship
from app.config.database import Base


class Scheme(Base):
    """Dental health scheme model."""
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False)
    type = Column(String(20), nullable=False)  # state, national, central, ngo, private
    status = Column(String(20), default="active")

    # Government Info
    ministry = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)  # For state schemes

    # Dates
    launch_date = Column(Date, nullable=True)
    valid_from = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)

    # Content
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)

    # Target Audience
    target_categories = Column(JSON, default=list)  # ["BPL", "Women", "Senior Citizens"]
    target_states = Column(JSON, default=list)

    # Coverage
    coverage_amount = Column(Numeric(12, 2), nullable=True)
    services_covered = Column(JSON, default=list)  # ["Extraction", "Dentures", "Cleaning"]

    # Eligibility
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    income_criteria = Column(String(200), nullable=True)

    # Required Documents
    required_documents = Column(JSON, default=list)

    # Contact
    website = Column(String(255), nullable=True)
    helpline = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    # Process Info
    application_process = Column(Text, nullable=True)
    processing_time = Column(String(50), nullable=True)

    # Original Document
    original_document_path = Column(String(500), nullable=True)
    original_document_filename = Column(String(255), nullable=True)
    full_document_text = Column(Text, nullable=True)  # Full extracted text from the PDF

    # Metadata
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)

    # Relationships
    versions = relationship("SchemeVersion", back_populates="scheme", order_by="desc(SchemeVersion.created_at)")
    bookmarks = relationship("SchemeBookmark", back_populates="scheme")
    eligibility_checks = relationship("EligibilityCheck", back_populates="scheme")
    user_broadcasts = relationship("UserBroadcast", back_populates="scheme")

    def to_dict(self):
        """Convert scheme to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type,
            "status": self.status,
            "ministry": self.ministry,
            "state": self.state,
            "launch_date": self.launch_date.isoformat() if self.launch_date else None,
            "description": self.description,
            "short_description": self.short_description,
            "target_categories": self.target_categories,
            "target_states": self.target_states,
            "coverage_amount": float(self.coverage_amount) if self.coverage_amount else None,
            "services_covered": self.services_covered,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "income_criteria": self.income_criteria,
            "required_documents": self.required_documents,
            "website": self.website,
            "helpline": self.helpline,
            "email": self.email,
            "application_process": self.application_process,
            "processing_time": self.processing_time,
            "has_original_document": bool(self.original_document_path),
            "full_document_text": self.full_document_text,
        }


class SchemeVersion(Base):
    """Scheme version history for audit."""
    __tablename__ = "scheme_versions"

    id = Column(Integer, primary_key=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    data = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)
    change_reason = Column(String(255), nullable=True)

    scheme = relationship("Scheme", back_populates="versions")


class SchemeBookmark(Base):
    """User bookmarked schemes."""
    __tablename__ = "scheme_bookmarks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)

    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="scheme_bookmarks")
    scheme = relationship("Scheme", back_populates="bookmarks")
