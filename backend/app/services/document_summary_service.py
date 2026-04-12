import asyncio
from datetime import datetime
from typing import Dict, Any
import httpx

from app.config.settings import settings
from app.models.document import SummaryStructure


class DocumentSummaryService:
    """Service for generating AI summaries of dental policy documents using Ollama"""
    
    def __init__(self):
        self.ollama_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_SUMMARY_MODEL
    
    async def generate_summary(self, document_text: str) -> SummaryStructure:
        """
        Generate structured summary from document text using Ollama
        
        Args:
            document_text: Extracted text from document
        
        Returns:
            SummaryStructure: Structured summary
        """
        prompt = f"""
You are an expert in dental insurance and government health schemes. Analyze the following document and extract key information in a structured format.

Document text:
{document_text[:8000]}  # Limit to first 8000 chars to avoid token limits

Please extract and return a JSON object with the following fields:
- coverage_scope: Summary of what the policy/scheme covers
- exclusions: List of specific exclusions (as an array)
- waiting_periods: List of waiting period information (as an array)
- premium_copay: Premium, co-pay, or cost details
- claim_process: Step-by-step claim process (as an array)
- renewal_conditions: Renewal conditions and requirements
- grievance_redressal: Grievance redressal process

Return only valid JSON without any additional text.
"""
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Ollama API error: {response.status_code}")
                
                result = response.json()
                summary_text = result.get("response", "{}")
                
                # Parse JSON response
                import json
                try:
                    summary_data = json.loads(summary_text)
                except json.JSONDecodeError:
                    # If JSON parsing fails, return default structure
                    summary_data = {
                        "coverage_scope": "Unable to extract coverage information",
                        "exclusions": [],
                        "waiting_periods": [],
                        "premium_copay": "",
                        "claim_process": [],
                        "renewal_conditions": "",
                        "grievance_redressal": ""
                    }
                
                return SummaryStructure(**summary_data)
                
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            # Return default structure on error
            return SummaryStructure(
                coverage_scope="Unable to generate summary due to processing error",
                exclusions=[],
                waiting_periods=[],
                premium_copay="",
                claim_process=[],
                renewal_conditions="",
                grievance_redressal=""
            )
    
    async def process_document_async(self, document_id: str, user_id: str, file_id: str, db):
        """
        Async task to process document and generate summary
        
        Args:
            document_id: Document ID
            user_id: User ID
            file_id: GridFS file ID
            db: Database instance
        """
        try:
            # Update status to processing
            await db["documents"].update_one(
                {"_id": document_id},
                {"$set": {"upload_status": "processing", "ai_status": "processing"}}
            )
            
            # Extract text from document
            from app.utils.gridfs_helper import gridfs_helper
            from app.services.pdf_service import pdf_service
            
            file_stream = await gridfs_helper.get_file(file_id)
            if not file_stream:
                raise Exception("File not found in GridFS")
            
            file_data = await file_stream.read()
            
            # Extract text based on file type
            if file_stream.content_type == "application/pdf":
                text = await pdf_service.extract_text_from_pdf(file_data)
            else:
                # For images, use OCR (simplified - would need Tesseract in production)
                text = "Text extraction from images not yet implemented"
            
            if not text or len(text) < 100:
                raise Exception("Unable to extract sufficient text from document")
            
            # Generate AI summary
            summary = await self.generate_summary(text)
            
            # Save summary to database
            await db["document_summaries"].insert_one({
                "document_id": document_id,
                "summary_json": summary.dict(),
                "model_version": self.model,
                "generated_at": datetime.utcnow()
            })
            
            # Update document status
            await db["documents"].update_one(
                {"_id": document_id},
                {
                    "$set": {
                        "upload_status": "completed",
                        "ai_status": "completed"
                    }
                }
            )
            
            # Send notification to user (placeholder - would integrate with notification service)
            print(f"Summary generated for document {document_id}")
            
        except Exception as e:
            print(f"Error processing document {document_id}: {str(e)}")
            # Update document status to failed
            await db["documents"].update_one(
                {"_id": document_id},
                {
                    "$set": {
                        "upload_status": "completed",
                        "ai_status": "failed"
                    }
                }
            )


document_summary_service = DocumentSummaryService()
