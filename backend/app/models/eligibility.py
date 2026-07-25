"""Eligibility engine models."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.config.database import Base


class EligibilityRule(Base):
    """Eligibility rule configuration for schemes."""
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, unique=True)

    # Rule name and description
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    # Rule configuration (JSON format)
    rule_config = Column(JSON, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)


class EligibilityCheck(Base):
    """Record of eligibility checks performed."""
    __tablename__ = "eligibility_checks"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False)

    # Input data used for check
    check_data = Column(JSON, nullable=False)  # {age, income, state, category, etc.}

    # Result
    result = Column(String(30), nullable=False)  # likely_eligible, possibly_eligible, not_eligible
    confidence_score = Column(Integer, default=0)  # 0-100

    # Detailed breakdown
    matched_conditions = Column(JSON, default=list)
    failed_conditions = Column(JSON, default=list)
    missing_conditions = Column(JSON, default=list)

    # Explanation
    result_explanation = Column(String(1000), nullable=True)
    next_steps = Column(String(1000), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="eligibility_checks")
    scheme = relationship("Scheme", back_populates="eligibility_checks")
