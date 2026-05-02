"""Eligibility engine models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.config.database import Base


class EligibilityResult(PyEnum):
    """Eligibility check result."""
    LIKELY_ELIGIBLE = "likely_eligible"
    POSSIBLY_ELIGIBLE = "possibly_eligible"
    NOT_ELIGIBLE = "not_eligible"
    MORE_INFO_NEEDED = "more_info_needed"


class EligibilityRule(Base):
    """Eligibility rule configuration for schemes."""
    __tablename__ = "eligibility_rules"
    
    id = Column(Integer, primary_key=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id"), nullable=False, unique=True)
    
    # Rule name and description
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Rule configuration (JSON format)
    # {
    #   "conditions": {
    #     "age": {"min": 18, "max": 65},
    #     "income": {"max": "300000"},
    #     "state": ["Karnataka", "Maharashtra"],
    #     "category": ["BPL", "SC", "ST"],
    #     "gender": ["female"]
    #   },
    #   "priority": 1
    # }
    rule_config = Column(JSON, nullable=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="eligibility_checks")
    scheme = relationship("Scheme", back_populates="eligibility_checks")
