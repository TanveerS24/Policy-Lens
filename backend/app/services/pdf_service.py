"""
PDF Service
Extract text from PDF files
"""

import fitz  # PyMuPDF
from typing import List, Dict
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class PDFExtractor:
    """Extract text and metadata from PDF files"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract all text from PDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += f"\n\n--- Page {page_num + 1} ---\n\n"
                text += page.get_text()
            
            doc.close()
            logger.info(f"✅ Text extracted from {pdf_path}")
            return text
        
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise


    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks for embedding
        """
        chunks = []
        words = text.split()
        
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_chunk.append(word)
            current_length += len(word) + 1
            
            if current_length >= chunk_size:
                chunks.append(" ".join(current_chunk))
                # Overlap: keep last words
                current_chunk = current_chunk[-(overlap // 5):]
                current_length = sum(len(w) for w in current_chunk) + len(current_chunk)
        
        # Add remaining text
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        logger.info(f"✅ Text split into {len(chunks)} chunks")
        return chunks


    @staticmethod
    def get_metadata(pdf_path: str) -> Dict:
        """Extract metadata from PDF"""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            page_count = len(doc)
            
            doc.close()
            
            return {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "pages": page_count,
            }
        
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {}
