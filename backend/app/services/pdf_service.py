"""Enhanced PDF processing service with OCR and content validation."""

import io
import os
import re
import shutil
from typing import Dict, Any
import PyPDF2
import pdfplumber
import pytesseract
from PIL import Image
import requests
import structlog

from app.config.settings import get_settings

logger = structlog.get_logger()
settings = get_settings()


class PDFProcessingService:
    """Service for processing PDF files with text extraction and OCR."""

    def extract_text_from_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """
        Extract text from PDF using multiple methods.
        Returns dict with extracted text and method used.
        """
        result = {
            "text": "",
            "method": "none",
            "page_count": 0,
            "has_images": False,
            "is_scanned": False
        }

        try:
            # Method 1: Try PyPDF2 first
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            page_count = len(pdf_reader.pages)

            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            # Check if extracted text is meaningful
            if self._is_meaningful_text(text):
                result["text"] = text
                result["method"] = "PyPDF2"
                result["page_count"] = page_count
                return result

            # Method 2: Try pdfplumber for better extraction
            pdf_file.seek(0)
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                page_count = len(pdf.pages)

                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            if self._is_meaningful_text(text):
                result["text"] = text
                result["method"] = "pdfplumber"
                result["page_count"] = page_count
                return result

            # Method 3: Check for images and use OCR
            result["has_images"] = True
            result["is_scanned"] = True

            ocr_text = self._extract_text_with_ocr(file_content)
            if ocr_text:
                result["text"] = ocr_text
                result["method"] = "OCR"
                result["page_count"] = self._count_pages_ocr(file_content)

            return result

        except Exception as e:
            raise Exception(f"PDF processing failed: {str(e)}")

    def _is_meaningful_text(self, text: str) -> bool:
        """Check if extracted text is meaningful and not just garbage."""
        if not text or len(text.strip()) < 50:
            return False

        # Check for common PDF artifacts
        artifacts = [
            "cid:", "xref", "stream", "endstream", "obj", "endobj",
            ">>", "<<", ">>", "startxref", "trailer"
        ]

        artifact_count = sum(1 for artifact in artifacts if artifact in text.lower())
        total_chars = len(text)

        # If more than 30% are PDF artifacts, consider it not meaningful
        if artifact_count > 0 and (artifact_count * 20) > total_chars:
            return False

        # Check for actual words (not just random characters)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        if len(words) < 5:
            return False

        return True

    def _extract_text_with_ocr(self, file_content: bytes) -> str:
        """Extract text from PDF using OCR and pdf2image."""
        # Auto-detect Tesseract executable on Windows if not in PATH
        if os.name == 'nt' and not shutil.which('tesseract'):
            default_win_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(default_win_path):
                pytesseract.pytesseract.tesseract_cmd = default_win_path

        full_text = ""

        # Method A: Use pdf2image for scanned PDF page rendering
        try:
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(file_content)
            for page_num, image in enumerate(images):
                text = pytesseract.image_to_string(image)
                if text and text.strip():
                    full_text += f"Page {page_num + 1}:\n{text.strip()}\n\n"
            if full_text.strip():
                return full_text.strip()
        except Exception as e:
            logger.warning("pdf2image_ocr_fallback", error=str(e))

        # Method B: Fallback to PyPDF2 page embedded image extraction
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num, page in enumerate(pdf_reader.pages):
                page_images = page.images

                if page_images:
                    for img_index, img in enumerate(page_images):
                        image = Image.open(io.BytesIO(img.data))
                        text = pytesseract.image_to_string(image)
                        if text.strip():
                            full_text += f"Page {page_num + 1}, Image {img_index + 1}:\n{text.strip()}\n\n"
                else:
                    try:
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            full_text += f"Page {page_num + 1}:\n{page_text.strip()}\n\n"
                    except Exception:
                        continue

            return full_text.strip()

        except Exception as e:
            logger.warning("ocr_extraction_failed", error=str(e))
            return ""

    def _count_pages_ocr(self, file_content: bytes) -> int:
        """Count pages in PDF for OCR method."""
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            return len(pdf_reader.pages)
        except Exception:
            return 1

    def validate_dental_scheme_content(self, text: str) -> Dict[str, Any]:
        """
        Validate if content is related to dental schemes using RAG.
        Returns validation result with confidence score and feedback.
        """
        validation_prompt = """
        Analyze the following text and determine if it contains information about a dental scheme, dental insurance, or dental health program.

        Look for indicators such as:
        - Dental treatments, procedures, or services covered
        - Insurance coverage for dental care
        - Eligibility criteria for dental benefits
        - Dental scheme names or codes
        - Ministry/department related to health/dental
        - Benefits like check-ups, fillings, extractions, etc.

        Respond with a JSON object in this exact format:
        {{
            "is_dental_scheme": true/false,
            "confidence_score": 0.0-1.0,
            "reasoning": "brief explanation",
            "suggested_actions": ["action1", "action2"]
        }}

        Text to analyze:
        {text}
        """

        try:
            ollama_response = self._query_ollama(validation_prompt.format(text=text[:5000]))

            # Parse JSON response
            import json
            try:
                validation_result = json.loads(ollama_response)
                return validation_result
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "is_dental_scheme": True,  # Assume it's valid if we can't parse
                    "confidence_score": 0.5,
                    "reasoning": "Unable to parse validation response, proceeding with caution",
                    "suggested_actions": ["manual_review"]
                }

        except Exception as e:
            return {
                "is_dental_scheme": True,  # Default to allow when service is unavailable
                "confidence_score": 0.3,
                "reasoning": f"Validation service unavailable: {str(e)}",
                "suggested_actions": ["manual_review"]
            }

    def extract_scheme_details(self, text: str) -> Dict[str, Any]:
        """
        Extract detailed scheme information using RAG.
        """
        extraction_prompt = """
        Extract comprehensive scheme details from this dental scheme document.

        Extract the following information:
        1. Scheme name (official name)
        2. Scheme code or acronym
        3. Type (state/national/central/ngo/private)
        4. Eligibility criteria (format with bullet points for clarity)
        5. Benefits covered (dental treatments)
        6. Coverage amounts/limits
        7. Required documents
        8. Application process
        9. Contact information

        IMPORTANT: For eligibility_criteria, format as clear, focused bullet points. Each bullet should be a specific eligibility requirement. Use proper bullet point format (• or -) and organize by categories like:
        • Age requirements
        • Income criteria
        • Residential requirements
        • Category/caste requirements
        • Medical/dental condition requirements
        • Documentation requirements

        Respond with a JSON object:
        {{
            "name": "scheme name",
            "code": "scheme code",
            "type": "scheme type",
            "eligibility_criteria": "• Requirement 1\\n• Requirement 2\\n• Requirement 3",
            "benefits_covered": ["benefit1", "benefit2"],
            "coverage_amount": "amount or limits",
            "required_documents": ["doc1", "doc2"],
            "application_process": "process description",
            "contact_info": "contact details"
        }}

        Document text:
        {text}
        """

        try:
            ollama_response = self._query_ollama(extraction_prompt.format(text=text[:8000]))

            import json
            try:
                return json.loads(ollama_response)
            except json.JSONDecodeError:
                # Fallback extraction
                return self._fallback_extraction(text)

        except Exception:
            return self._fallback_extraction(text)

    def check_eligibility(self, scheme_details: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if user is eligible for the scheme based on scheme details and user profile.
        """
        eligibility_prompt = """
        Based on the scheme details and user profile, determine eligibility.

        Scheme Details:
        {scheme_details}

        User Profile:
        {user_profile}

        Analyze and respond with JSON:
        {{
            "is_eligible": true/false,
            "eligibility_score": 0.0-1.0,
            "matching_criteria": ["criteria1", "criteria2"],
            "missing_criteria": ["criteria1", "criteria2"],
            "recommendations": ["recommendation1", "recommendation2"]
        }}
        """

        try:
            ollama_response = self._query_ollama(
                eligibility_prompt.format(
                    scheme_details=str(scheme_details),
                    user_profile=str(user_profile)
                )
            )

            import json
            try:
                return json.loads(ollama_response)
            except json.JSONDecodeError:
                return {
                    "is_eligible": False,
                    "eligibility_score": 0.0,
                    "matching_criteria": [],
                    "missing_criteria": ["Unable to determine"],
                    "recommendations": ["Manual review required"]
                }

        except Exception:
            return {
                "is_eligible": False,
                "eligibility_score": 0.0,
                "matching_criteria": [],
                "missing_criteria": ["Service unavailable"],
                "recommendations": ["Please try again later"]
            }

    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama for RAG processing."""
        try:
            ollama_host = self._get_ollama_host()
            ollama_url = f"http://{ollama_host}:11434/api/generate"

            response = requests.post(
                ollama_url,
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")

        except Exception as e:
            logger.warning("ollama_query_failed", error=str(e))
            raise Exception(f"RAG processing failed: {str(e)}")

    def _get_ollama_host(self) -> str:
        """Get Ollama host, trying multiple options."""
        env_host = os.environ.get('OLLAMA_HOST')
        if env_host:
            return env_host

        hosts_to_try = ['localhost', '127.0.0.1', 'host.docker.internal']
        for host in hosts_to_try:
            try:
                response = requests.get(f"http://{host}:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    return host
            except Exception:
                continue

        return 'localhost'

    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback extraction using regex patterns."""
        return {
            "name": "Unknown Scheme",
            "code": "UNKNOWN",
            "type": "unknown",
            "eligibility_criteria": text[:500] + "..." if len(text) > 500 else text,
            "benefits_covered": [],
            "coverage_amount": "Not specified",
            "required_documents": [],
            "application_process": "Not specified",
            "contact_info": "Not specified"
        }
