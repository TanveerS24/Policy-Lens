"""User model for patients and guests."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.config.database import Base


class User(Base):
    """Patient/Guest user model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    mobile = Column(String(10), unique=True, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)

    # Address
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    pin_code = Column(String(6), nullable=False)

    # Auth
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Security
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deactivated_at = Column(DateTime, nullable=True)

    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user")
    scheme_bookmarks = relationship("SchemeBookmark", back_populates="user")
    eligibility_checks = relationship("EligibilityCheck", back_populates="user")


class UserProfile(Base):
    """Extended user profile information."""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Demographics
    occupation = Column(String(50), nullable=True)
    income_bracket = Column(String(20), nullable=True)  # BPL, Low, Medium, High
    category = Column(String(20), nullable=True)  # General, SC, ST, OBC

    # Health
    has_dental_conditions = Column(Boolean, default=False)
    dental_conditions = Column(JSON, default=list)

    # Emergency Contact
    emergency_name = Column(String(100), nullable=True)
    emergency_mobile = Column(String(10), nullable=True)

    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="profile")


# Add relationship to User
User.profile = relationship("UserProfile", back_populates="user", uselist=False)
