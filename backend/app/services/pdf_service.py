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
        Validate if content is related to dental/oral healthcare using Keyword Heuristics + AI.
        Allows ALL documents related to dental/oral health (programs, guidelines, treatments, schemes).
        Rejects ONLY non-dental documents (e.g. vehicle insurance, real estate, bank loans).
        """
        if not text or len(text.strip()) < 20:
            return {
                "is_dental_scheme": False,
                "confidence_score": 1.0,
                "reasoning": "Document contains insufficient or unreadable text content.",
                "suggested_actions": ["Upload a valid PDF document containing text or clear scan."]
            }

        # Step 1: Fast Keyword Heuristic Check
        dental_keywords = [
            "dental", "dentist", "dentistry", "teeth", "tooth", "denture", "dentures",
            "oral", "orthodontic", "orthodontics", "periodontal", "endodontic",
            "molar", "caries", "gum", "gums", "extraction", "extractions", "scaling",
            "filling", "fillings", "crown", "crowns", "bridge", "bridges", "root canal",
            "stomatology", "dental health", "dental care", "dental benefit", "dental scheme",
            "oral health", "oral healthcare", "nohp", "oral disease", "oral diseases"
        ]

        text_lower = text.lower()
        keyword_hits = [kw for kw in dental_keywords if kw in text_lower]

        if not keyword_hits:
            logger.warning("dental_validation_failed_no_keywords")
            return {
                "is_dental_scheme": False,
                "confidence_score": 0.95,
                "reasoning": "The document does not mention any dental care terms, oral health topics, or dental treatments.",
                "suggested_actions": ["Upload a PDF document specifically related to dental/oral health."]
            }

        # Step 2: Query Ollama AI for validation
        validation_prompt = """
        Analyze the following document text and determine if it is related to dental care, oral health, dental health programs, dental guidelines, dental treatments, or dental policy documents.

        CRITICAL VALIDATION RULE:
        - ALLOW (is_dental_scheme: true) for ALL documents related to dental or oral health (including government oral health programs, dental guidelines, dental treatment plans, and dental insurance).
        - REJECT (is_dental_scheme: false) ONLY if the document has NOTHING to do with dental or oral health (e.g. motor vehicle insurance, real estate agreements, bank loans, resumes, IT manuals).

        Document Text:
        {text}

        Respond with a JSON object ONLY in this exact format:
        {{
            "is_dental_scheme": true/false,
            "confidence_score": 0.9,
            "reasoning": "Clear explanation of why this document is or is not related to dental or oral healthcare."
        }}
        """

        try:
            ollama_response = self._query_ollama(
                validation_prompt.format(text=text[:5000]),
                json_format=True
            )

            import json
            cleaned_resp = ollama_response.strip()
            if cleaned_resp.startswith("```"):
                lines = cleaned_resp.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                cleaned_resp = "\n".join(lines).strip()

            result = json.loads(cleaned_resp)
            if isinstance(result, dict) and "is_dental_scheme" in result:
                return result

        except Exception as e:
            logger.warning("ollama_validation_query_failed", error=str(e))

        # If keyword hits exist and AI is unreachable, pass with keyword evidence
        return {
            "is_dental_scheme": True,
            "confidence_score": 0.85,
            "reasoning": f"Document contains dental/oral health keywords ({', '.join(keyword_hits[:5])}).",
            "suggested_actions": []
        }

    def extract_scheme_details(self, text: str) -> Dict[str, Any]:
        """
        Extract detailed scheme information using RAG/Ollama.
        If AI queueing or extraction fails, raises an exception without returning fake/fallback content.
        """
        extraction_prompt = """
        You are an expert dental healthcare analyst. Analyze the document text below and extract comprehensive scheme details.

        CRITICAL INSTRUCTIONS FOR 'about_scheme':
        - Write a high-quality, comprehensive paragraph summary (4 to 5 lines) detailing the scheme's overarching mission, target demographic emphasis (e.g. children, adults, elderly, pregnant women, rural populations, low-income groups), core services/treatments provided (prevention, diagnosis, extractions, dentures, root canals, cleanings, awareness), and overall objective across India.

        CRITICAL INSTRUCTIONS FOR 'eligibility_criteria':
        - Format strictly as clear structured lines in this exact layout:
          - Age requirement: <Age range or "None / All age groups">
          - Income criteria: <Income cap or "No income restriction">
          - Target category: <Target categories, e.g. Low-income families, Senior Citizens, Children>
          - Required documents: <Required documents, e.g. Aadhaar Card, Income Certificate>

        - If the document contains NO specific eligibility restrictions (e.g. open to all citizens, or universal policy), clearly state "None / Open to all citizens" for age and income, and set "has_eligibility_restrictions": false.

        Document Text:
        {text}

        Extract and return a valid JSON object ONLY with the exact following schema:
        {{
            "name": "Official Scheme Name (from document header/title)",
            "code": "Scheme Code / Policy ID (e.g., DPM-2026-001)",
            "type": "One of: national, state, central, ngo, private",
            "about_scheme": "Comprehensive 4-5 line paragraph summary explaining scheme mission, target emphasis, core oral health services/treatments, and overall objective...",
            "eligibility_criteria": "- Age requirement: 18 to 65 years\\n- Income criteria: Below INR 3,00,000 per annum\\n- Target category: Low-income families, Senior Citizens, Children\\n- Required documents: Aadhaar Card, Income Certificate",
            "has_eligibility_restrictions": true,
            "ministry": "Issuing Ministry, Department, or Organization",
            "state": "State name if state-specific, or null",
            "coverage_amount": 50000,
            "min_age": 18,
            "max_age": 65,
            "target_categories": ["Low-income families", "Senior Citizens", "Children"],
            "services_covered": ["Cleanings", "Dentures", "Extractions", "Root Canals"],
            "required_documents": ["Aadhaar Card", "Income Certificate"],
            "website": "Official website URL or empty string",
            "helpline": "Helpline number or empty string"
        }}
        """

        try:
            ollama_response = self._query_ollama(
                extraction_prompt.format(text=text[:8000]),
                json_format=True
            )

            import json
            # Clean markdown codeblocks if present
            cleaned_resp = ollama_response.strip()
            if cleaned_resp.startswith("```"):
                lines = cleaned_resp.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                cleaned_resp = "\n".join(lines).strip()

            data = json.loads(cleaned_resp)
            if not isinstance(data, dict):
                raise Exception("Extracted data is not a valid JSON object")
            return data

        except Exception as e:
            logger.error("ollama_scheme_extraction_failed", error=str(e))
            raise Exception(f"AI scheme extraction failed: {str(e)}")

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
                ),
                json_format=True
            )

            import json
            cleaned_resp = ollama_response.strip()
            if cleaned_resp.startswith("```"):
                lines = cleaned_resp.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                cleaned_resp = "\n".join(lines).strip()

            return json.loads(cleaned_resp)

        except Exception:
            return {
                "is_eligible": False,
                "eligibility_score": 0.0,
                "matching_criteria": [],
                "missing_criteria": ["Service unavailable"],
                "recommendations": ["Please try again later"]
            }

    def _query_ollama(self, prompt: str, json_format: bool = False) -> str:
        """Query Ollama for RAG processing."""
        try:
            ollama_host = self._get_ollama_host()
            ollama_url = f"http://{ollama_host}:11434/api/generate"

            payload = {
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            }
            if json_format:
                payload["format"] = "json"

            response = requests.post(
                ollama_url,
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")

        except Exception as e:
            logger.warning("ollama_query_failed", error=str(e))
            raise Exception(f"Ollama AI query failed: {str(e)}")

    def _get_ollama_host(self) -> str:
        """Get working Ollama host, avoiding invalid hosts like 0.0.0.0."""
        env_host = os.environ.get('OLLAMA_HOST', '').strip()

        # Sanitize env_host if present and not 0.0.0.0
        if env_host and env_host != '0.0.0.0':
            env_host_clean = env_host.replace('http://', '').replace('https://', '').split(':')[0].strip('/')
            if env_host_clean and env_host_clean != '0.0.0.0':
                try:
                    response = requests.get(f"http://{env_host_clean}:11434/api/tags", timeout=2)
                    if response.status_code == 200:
                        return env_host_clean
                except Exception:
                    pass

        # Try default host candidates
        hosts_to_try = ['host.docker.internal', '127.0.0.1', 'localhost', '172.17.0.1']
        for host in hosts_to_try:
            try:
                response = requests.get(f"http://{host}:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    return host
            except Exception:
                continue

        return 'host.docker.internal'

