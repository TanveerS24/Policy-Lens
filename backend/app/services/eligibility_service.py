from datetime import datetime
from typing import Dict, Any, List
from bson import ObjectId

from app.database.client import get_db
from app.models.eligibility_rule import (
    EligibilityCheckResult,
    EligibilityCheckRequest,
    RuleCondition,
    RuleFieldEnum,
    RuleOperatorEnum,
)


class EligibilityService:
    """Service for evaluating eligibility rules"""
    
    async def evaluate_condition(self, condition: RuleCondition, profile: Dict[str, Any]) -> bool:
        """
        Evaluate a single condition against profile data
        
        Args:
            condition: Rule condition to evaluate
            profile: Patient profile data
        
        Returns:
            bool: True if condition is met
        """
        field = condition.field
        operator = condition.operator
        value = condition.value
        
        # Get profile value for field
        profile_value = profile.get(field.value)
        
        if profile_value is None:
            return False
        
        # Evaluate based on operator
        if operator == RuleOperatorEnum.EQUALS:
            return profile_value == value
        
        elif operator == RuleOperatorEnum.NOT_EQUALS:
            return profile_value != value
        
        elif operator == RuleOperatorEnum.GREATER_THAN:
            try:
                return float(profile_value) > float(value)
            except (ValueError, TypeError):
                return False
        
        elif operator == RuleOperatorEnum.LESS_THAN:
            try:
                return float(profile_value) < float(value)
            except (ValueError, TypeError):
                return False
        
        elif operator == RuleOperatorEnum.GREATER_THAN_OR_EQUAL:
            try:
                return float(profile_value) >= float(value)
            except (ValueError, TypeError):
                return False
        
        elif operator == RuleOperatorEnum.LESS_THAN_OR_EQUAL:
            try:
                return float(profile_value) <= float(value)
            except (ValueError, TypeError):
                return False
        
        elif operator == RuleOperatorEnum.IN_LIST:
            if isinstance(profile_value, list):
                return any(v in value for v in profile_value)
            return profile_value in value if isinstance(value, list) else False
        
        elif operator == RuleOperatorEnum.NOT_IN_LIST:
            if isinstance(profile_value, list):
                return all(v not in value for v in profile_value)
            return profile_value not in value if isinstance(value, list) else True
        
        elif operator == RuleOperatorEnum.RANGE:
            value_end = condition.value_end
            if value_end is None:
                return False
            try:
                profile_float = float(profile_value)
                return value <= profile_float <= value_end
            except (ValueError, TypeError):
                return False
        
        elif operator == RuleOperatorEnum.CONTAINS:
            if isinstance(profile_value, str) and isinstance(value, str):
                return value.lower() in profile_value.lower()
            return False
        
        return False
    
    async def evaluate_rule(self, rule: Dict[str, Any], profile: Dict[str, Any]) -> bool:
        """
        Evaluate a complete rule (with multiple conditions)
        
        Args:
            rule: Rule data with conditions
            profile: Patient profile data
        
        Returns:
            bool: True if rule is satisfied
        """
        conditions = rule.get("conditions", [])
        logic = rule.get("logic", "AND")
        
        if not conditions:
            return True
        
        results = []
        for cond_dict in conditions:
            condition = RuleCondition(**cond_dict)
            result = await self.evaluate_condition(condition, profile)
            results.append(result)
        
        if logic == "AND":
            return all(results)
        elif logic == "OR":
            return any(results)
        
        return all(results)
    
    async def check_eligibility(self, request: EligibilityCheckRequest, user_id: str) -> EligibilityCheckResult:
        """
        Check eligibility for a scheme based on patient profile
        
        Args:
            request: Eligibility check request
            user_id: Patient user ID
        
        Returns:
            EligibilityCheckResult: Eligibility result with details
        """
        db = get_db()
        
        # Get scheme
        if not ObjectId.is_valid(request.scheme_id):
            return EligibilityCheckResult(
                eligible=False,
                eligibility_status="not_eligible",
                reason="Invalid scheme ID"
            )
        
        scheme = await db["schemes"].find_one({"_id": ObjectId(request.scheme_id)})
        if not scheme:
            return EligibilityCheckResult(
                eligible=False,
                eligibility_status="not_eligible",
                reason="Scheme not found"
            )
        
        # Get active rules for scheme
        rules = await db["eligibility_rules"].find({
            "scheme_id": request.scheme_id,
            "active": True
        }).to_list(None)
        
        if not rules:
            # No rules defined - possibly eligible
            return EligibilityCheckResult(
                eligible=True,
                eligibility_status="possibly_eligible",
                reason="No eligibility rules defined for this scheme. Please contact support for verification.",
                matched_rules=[],
                failed_rules=[]
            )
        
        # Evaluate all rules
        matched_rules = []
        failed_rules = []
        all_passed = True
        
        for rule in rules:
            rule_passed = await self.evaluate_rule(rule, request.profile)
            if rule_passed:
                matched_rules.append(rule.get("rule_name", str(rule["_id"])))
            else:
                failed_rules.append(rule.get("rule_name", str(rule["_id"])))
                all_passed = False
        
        # Determine overall eligibility
        if all_passed and matched_rules:
            result = EligibilityCheckResult(
                eligible=True,
                eligibility_status="likely_eligible",
                reason="You meet all eligibility criteria for this scheme.",
                matched_rules=matched_rules,
                failed_rules=[]
            )
        elif matched_rules and not all_passed:
            result = EligibilityCheckResult(
                eligible=False,
                eligibility_status="possibly_eligible",
                reason=f"You meet some criteria but not all. Failed rules: {', '.join(failed_rules)}",
                matched_rules=matched_rules,
                failed_rules=failed_rules
            )
        else:
            result = EligibilityCheckResult(
                eligible=False,
                eligibility_status="not_eligible",
                reason=f"You do not meet the eligibility criteria. Failed rules: {', '.join(failed_rules)}",
                matched_rules=[],
                failed_rules=failed_rules
            )
        
        # Log the eligibility check
        await db["eligibility_checks"].insert_one({
            "user_id": user_id,
            "scheme_id": request.scheme_id,
            "inputs": request.profile,
            "result": result.eligibility_status,
            "reason": result.reason,
            "checked_at": datetime.utcnow()
        })
        
        return result
    
    async def create_rule(self, db, rule_data: Dict[str, Any], admin_id: str) -> str:
        """
        Create new eligibility rule
        
        Args:
            db: Database instance
            rule_data: Rule data
            admin_id: Admin user ID
        
        Returns:
            str: Rule ID
        """
        # Validate scheme exists
        if not ObjectId.is_valid(rule_data["scheme_id"]):
            raise ValueError("Invalid scheme ID")
        
        scheme = await db["schemes"].find_one({"_id": ObjectId(rule_data["scheme_id"])})
        if not scheme:
            raise ValueError("Scheme not found")
        
        # Create rule
        rule_doc = rule_data.copy()
        rule_doc.update({
            "version": 1,
            "created_by": admin_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        result = await db["eligibility_rules"].insert_one(rule_doc)
        return str(result.inserted_id)
    
    async def update_rule(self, db, rule_id: str, rule_data: Dict[str, Any], admin_id: str) -> bool:
        """
        Update eligibility rule with versioning
        
        Args:
            db: Database instance
            rule_id: Rule ID
            rule_data: Updated rule data
            admin_id: Admin user ID
        
        Returns:
            bool: True if updated
        """
        if not ObjectId.is_valid(rule_id):
            raise ValueError("Invalid rule ID")
        
        existing = await db["eligibility_rules"].find_one({"_id": ObjectId(rule_id)})
        if not existing:
            raise ValueError("Rule not found")
        
        # Create version snapshot
        current_version = existing.get("version", 1)
        new_version = current_version + 1
        
        await db["eligibility_rule_versions"].insert_one({
            "rule_id": rule_id,
            "version_number": current_version,
            "snapshot": existing,
            "changed_by": admin_id,
            "changed_at": datetime.utcnow()
        })
        
        # Update rule
        update_data = rule_data.copy()
        update_data.update({
            "version": new_version,
            "updated_at": datetime.utcnow()
        })
        
        await db["eligibility_rules"].update_one(
            {"_id": ObjectId(rule_id)},
            {"$set": update_data}
        )
        
        return True
    
    async def get_rule_versions(self, db, rule_id: str) -> List[Dict]:
        """
        Get version history for a rule
        
        Args:
            db: Database instance
            rule_id: Rule ID
        
        Returns:
            List of version snapshots
        """
        if not ObjectId.is_valid(rule_id):
            raise ValueError("Invalid rule ID")
        
        cursor = db["eligibility_rule_versions"].find({"rule_id": rule_id}).sort([("version_number", -1)])
        return [version async for version in cursor]


eligibility_service = EligibilityService()
