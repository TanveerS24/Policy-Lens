"""
Eligibility Service
Check user eligibility against policy criteria
"""

import json
from typing import Dict
from app.services.ollama_service import OllamaClient
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class EligibilityService:
    """Check eligibility using Llama3.2 reasoning"""
    
    def __init__(self):
        self.ollama = OllamaClient()
    
    async def check_eligibility(
        self,
        user_profile: Dict,
        eligibility_criteria: Dict,
        policy_summary: str,
    ) -> Dict:
        """
        Check if user is eligible for policy
        Uses Llama3.2 for reasoning
        
        Returns:
        {
            "eligible": bool,
            "reason": str,
            "missing_requirements": [],
            "confidence_score": float
        }
        """
        try:
            prompt = f"""You are a healthcare policy eligibility expert. Carefully analyze the following:

USER PROFILE:
- Age: {user_profile.get('age', 'Not provided')}
- Gender: {user_profile.get('gender', 'Not provided')}
- State: {user_profile.get('state', 'Not provided')}
- Income: {user_profile.get('income', 'Not provided')}

ELIGIBILITY CRITERIA:
{json.dumps(eligibility_criteria, indent=2)}

POLICY SUMMARY:
{policy_summary[:1500]}

Based on this information, determine if the user is eligible for this policy. Consider:
1. Age requirements
2. Income requirements
3. Geographic/state requirements
4. Any exclusions or special conditions

Respond in JSON format:
{{
    "eligible": true/false,
    "reason": "Clear explanation of eligibility determination",
    "missing_requirements": ["requirement1", "requirement2"],
    "confidence_score": 0.0-1.0,
    "details": "Additional context"
}}
"""
            
            result = await self.ollama.generate(
                model=self.ollama.reasoning_model,
                prompt=prompt,
                temperature=0.5,
            )
            
            response_text = result.get("response", "")
            
            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                eligibility_result = json.loads(json_str)
            except:
                eligibility_result = {
                    "eligible": False,
                    "reason": "Could not determine eligibility",
                    "missing_requirements": [],
                    "confidence_score": 0.0,
                }
            
            logger.info(f"✅ Eligibility checked - Result: {eligibility_result['eligible']}")
            return eligibility_result
        
        except Exception as e:
            logger.error(f"Error checking eligibility: {e}")
            raise
    
    async def explain_ineligibility(
        self,
        user_profile: Dict,
        eligibility_criteria: Dict,
    ) -> str:
        """Generate detailed explanation of why user is ineligible"""
        try:
            prompt = f"""Explain in simple terms why this user does not meet the eligibility criteria:

USER: {json.dumps(user_profile, indent=2)}
REQUIREMENTS: {json.dumps(eligibility_criteria, indent=2)}

Provide a clear, empathetic explanation that:
1. Identifies specific missing criteria
2. Suggests possible solutions if any
3. Is easy to understand for a non-technical user
"""
            
            result = await self.ollama.generate(
                model=self.ollama.reasoning_model,
                prompt=prompt,
                temperature=0.6,
            )
            
            logger.info(f"✅ Ineligibility explanation generated")
            return result.get("response", "")
        
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            raise
