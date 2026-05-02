"""Document upload and AI summary models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.config.database import Base


class DocumentStatus(PyEnum):
    """Document processing status."""
    PENDING = "pending"
    SCANNING = "scanning"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    QUARANTINED = "quarantined"


class Document(Base):
    """User uploaded policy documents."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # File info
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False, unique=True)
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(50), nullable=False)
    
    # Storage
    storage_path = Column(String(500), nullable=False)
    storage_url = Column(String(500), nullable=True)
    
    # Status
    status = Column(String(20), default="pending")
    virus_scan_result = Column(String(20), nullable=True)  # clean, infected, error
    
    # Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # AI Summary (populated after processing)
    summary_generated = Column(Boolean, default=False)
    summary_generated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    ai_summary = relationship("AISummary", back_populates="document", uselist=False)


class AISummary(Base):
    """AI-generated document summary."""
    __tablename__ = "ai_summaries"
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), unique=True)
    
    # Summary sections
    coverage_summary = Column(Text, nullable=True)
    exclusions = Column(Text, nullable=True)
    waiting_period = Column(Text, nullable=True)
    claims_process = Column(Text, nullable=True)
    renewal_conditions = Column(Text, nullable=True)
    
    # Raw structured data
    coverage_details = Column(JSON, default=dict)  # {amount, services, frequency}
    exclusions_list = Column(JSON, default=list)
    
    # Metadata
    processing_time_seconds = Column(Integer, nullable=True)
    model_used = Column(String(50), nullable=True)
    confidence_score = Column(Integer, nullable=True)  # 0-100
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="ai_summary")


class DocumentChunk(Base):
    """Document chunks for vector search (future RAG)."""
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True)
    
    embedding = Column(JSON, nullable=True)  # Vector embedding for similarity search
    
    created_at = Column(DateTime, default=datetime.utcnow)
