"""
Summary Service
Generate policy summaries and extract eligibility criteria
"""

import json
from typing import Dict
from app.services.ollama_service import OllamaClient
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SummaryService:
    """Generate policy summaries and extract data"""
    
    def __init__(self):
        self.ollama = OllamaClient()
    
    async def generate_summary(self, policy_text: str) -> Dict:
        """
        Generate policy summary using Gemma3
        Returns: title, short_description, summary, eligibility_criteria, covered_benefits, important_notes
        """
        try:
            prompt = f"""Analyze this healthcare policy document and provide:
1. A concise title
2. A short description (1-2 sentences)
3. A detailed summary (2-3 paragraphs)
4. Eligibility criteria in JSON format
5. List of covered benefits
6. Important notes and exclusions

Policy text:
{policy_text[:3000]}

Please respond in the following JSON format:
{{
    "title": "Policy Title",
    "short_description": "Brief description",
    "summary": "Detailed summary",
    "eligibility_criteria": {{
        "minimum_age": 0,
        "maximum_age": 150,
        "income_requirement": "text",
        "other_requirements": []
    }},
    "covered_benefits": ["benefit1", "benefit2"],
    "important_notes": ["note1", "note2"]
}}
"""
            
            result = await self.ollama.generate(
                model=self.ollama.summarization_model,
                prompt=prompt,
                temperature=0.3,  # Lower temperature for consistency
            )
            
            # Extract and parse JSON response
            response_text = result.get("response", "")
            
            try:
                # Try to find JSON in the response
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    summary_data = json.loads(json_str)
                else:
                    raise ValueError("Could not find JSON in response")
            
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                summary_data = {
                    "title": "Policy Summary",
                    "short_description": "Generated from policy document",
                    "summary": response_text,
                    "eligibility_criteria": {},
                    "covered_benefits": [],
                    "important_notes": [],
                }
            
            logger.info(f"✅ Summary generated for policy")
            return summary_data
        
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            raise
    
    async def extract_eligibility_rules(self, policy_text: str) -> Dict:
        """
        Extract detailed eligibility rules from policy
        """
        try:
            prompt = f"""Extract all eligibility rules and requirements from this healthcare policy.
Format your response as a JSON object with the following structure:
{{
    "age_requirements": {{"minimum": number, "maximum": number}},
    "income_requirements": {{"minimum": number, "maximum": number, "notes": "text"}},
    "residency_requirements": "text",
    "documentation_required": ["doc1", "doc2"],
    "excluded_conditions": ["condition1", "condition2"],
    "waiting_period": "text",
    "other_requirements": ["req1", "req2"]
}}

Policy text:
{policy_text[:2000]}
"""
            
            result = await self.ollama.generate(
                model=self.ollama.summarization_model,
                prompt=prompt,
                temperature=0.2,
            )
            
            response_text = result.get("response", "")
            
            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                eligibility_data = json.loads(json_str)
            except:
                eligibility_data = {"error": "Could not parse eligibility rules"}
            
            logger.info(f"✅ Eligibility rules extracted")
            return eligibility_data
        
        except Exception as e:
            logger.error(f"Error extracting eligibility rules: {e}")
            raise
