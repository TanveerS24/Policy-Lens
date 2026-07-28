"""Eligibility engine endpoints."""

from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, String

from app.config.database import get_db
from app.models.eligibility import EligibilityRule, EligibilityCheck
from app.models.scheme import Scheme
from app.models.user import User
from app.api.v1.endpoints.patients import get_current_user

router = APIRouter()


# Schemas
class EligibilityCheckRequest(BaseModel):
    scheme_id: int
    age: Optional[int] = None
    income: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    has_dental_conditions: Optional[bool] = None


class BulkEligibilityRequest(BaseModel):
    age: Optional[int] = None
    income: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


# Endpoints
@router.post("/check")
async def check_eligibility(
    request: EligibilityCheckRequest,
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check eligibility for a specific scheme."""
    scheme = db.query(Scheme).filter(
        Scheme.id == request.scheme_id,
        Scheme.is_deleted == False
    ).first()
    
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    # Get eligibility rules
    rule = db.query(EligibilityRule).filter(
        EligibilityRule.scheme_id == request.scheme_id,
        EligibilityRule.is_active == True
    ).first()
    
    # Prepare check data
    check_data = {
        "age": request.age,
        "income": request.income,
        "state": request.state,
        "category": request.category,
        "gender": request.gender,
        "occupation": request.occupation,
        "has_dental_conditions": request.has_dental_conditions,
    }
    
    # Remove None values
    check_data = {k: v for k, v in check_data.items() if v is not None}
    
    # Evaluate rules if they exist
    result = "more_info_needed"
    confidence_score = 0
    matched_conditions = []
    failed_conditions = []
    missing_conditions = []
    explanation = ""
    
    if rule and rule.rule_config:
        conditions = rule.rule_config.get("conditions", {})
        
        for condition, requirement in conditions.items():
            user_value = check_data.get(condition)
            
            if user_value is None:
                missing_conditions.append(condition)
                continue
            
            # Evaluate condition
            if isinstance(requirement, dict):
                if "min" in requirement and user_value < requirement["min"]:
                    failed_conditions.append(f"{condition}: min {requirement['min']}")
                elif "max" in requirement and user_value > requirement["max"]:
                    failed_conditions.append(f"{condition}: max {requirement['max']}")
                elif "in" in requirement and user_value not in requirement["in"]:
                    failed_conditions.append(f"{condition}: must be in {requirement['in']}")
                else:
                    matched_conditions.append(condition)
            elif isinstance(requirement, list):
                if user_value in requirement:
                    matched_conditions.append(condition)
                else:
                    failed_conditions.append(f"{condition}: must be in {requirement}")
            else:
                if user_value == requirement:
                    matched_conditions.append(condition)
                else:
                    failed_conditions.append(f"{condition}: must be {requirement}")
        
        # Determine result
        total_conditions = len(conditions)
        matched_count = len(matched_conditions)
        failed_count = len(failed_conditions)
        
        confidence_score = int((matched_count / total_conditions) * 100) if total_conditions > 0 else 0
        
        if failed_count == 0 and matched_count == total_conditions:
            result = "likely_eligible"
            explanation = "You meet all the eligibility criteria for this scheme."
        elif failed_count > 0 and matched_count > 0:
            result = "possibly_eligible"
            explanation = f"You meet some criteria but not all. Consider the failed conditions."
        elif failed_count > 0:
            result = "not_eligible"
            explanation = "You do not meet the eligibility criteria for this scheme."
        else:
            result = "more_info_needed"
            explanation = "More information is needed to determine eligibility."
    else:
        # Basic check without rules
        if request.age is not None and scheme.min_age and request.age < scheme.min_age:
            result = "not_eligible"
            failed_conditions.append(f"Minimum age: {scheme.min_age}")
        elif request.age is not None and scheme.max_age and request.age > scheme.max_age:
            result = "not_eligible"
            failed_conditions.append(f"Maximum age: {scheme.max_age}")
        else:
            result = "likely_eligible" if check_data else "more_info_needed"
            explanation = "Basic eligibility criteria met. Please verify with official sources."
    
    # Save check if user is authenticated
    if user:
        check_record = EligibilityCheck(
            user_id=user.id,
            scheme_id=request.scheme_id,
            check_data=check_data,
            result=result,
            confidence_score=confidence_score,
            matched_conditions=matched_conditions,
            failed_conditions=failed_conditions,
            missing_conditions=missing_conditions,
            result_explanation=explanation,
        )
        db.add(check_record)
        db.commit()
    
    return {
        "scheme_id": request.scheme_id,
        "scheme_name": scheme.name,
        "result": result,
        "confidence_score": confidence_score,
        "matched_conditions": matched_conditions,
        "failed_conditions": failed_conditions,
        "missing_conditions": missing_conditions,
        "explanation": explanation,
        "required_documents": scheme.required_documents,
        "coverage_amount": float(scheme.coverage_amount) if scheme.coverage_amount else None,
        "services_covered": scheme.services_covered,
        "application_process": scheme.application_process,
        "helpline": scheme.helpline,
        "website": scheme.website,
    }


@router.post("/check-all")
async def check_all_schemes(
    request: BulkEligibilityRequest,
    user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check eligibility across all schemes."""
    # Get all active schemes
    query = db.query(Scheme).filter(Scheme.is_deleted == False, Scheme.status == "active")
    
    if request.filters:
        if "type" in request.filters:
            query = query.filter(Scheme.type == request.filters["type"])
        if "state" in request.filters:
            st_filter = f"%{request.filters['state']}%"
            query = query.filter(func.cast(Scheme.target_states, String).ilike(st_filter))
    
    schemes = query.order_by(Scheme.created_at.desc(), Scheme.id.desc()).all()
    
    results = []
    for scheme in schemes:
        # Quick eligibility check
        is_eligible = True
        reasons = []
        
        if request.age is not None and scheme.min_age and request.age < scheme.min_age:
            is_eligible = False
            reasons.append(f"Age below minimum {scheme.min_age}")
        if request.age is not None and scheme.max_age and request.age > scheme.max_age:
            is_eligible = False
            reasons.append(f"Age above maximum {scheme.max_age}")
        if request.state and scheme.target_states and request.state not in scheme.target_states:
            is_eligible = False
            reasons.append(f"Not available in {request.state}")
        
        if is_eligible or not reasons:  # Include if eligible or no specific failures
            results.append({
                "scheme_id": scheme.id,
                "scheme_name": scheme.name,
                "type": scheme.type,
                "likely_eligible": is_eligible and not reasons,
                "coverage_amount": float(scheme.coverage_amount) if scheme.coverage_amount else None,
                "services_covered": scheme.services_covered,
                "website": scheme.website,
                "helpline": scheme.helpline,
            })
    
    return {
        "total_schemes": len(schemes),
        "matching_schemes": len(results),
        "results": results,
    }
