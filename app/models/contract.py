"""
Contract Model - Database schema for contracts
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Contract(Base):
    """Contract model for storing uploaded contract metadata and content"""
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(10), nullable=False)  # pdf, docx
    raw_text = Column(Text, nullable=True)
    file_size = Column(Integer, nullable=False)  # in bytes
    
    # Metadata
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status tracking
    text_extracted = Column(Boolean, default=False)
    clauses_extracted = Column(Boolean, default=False)
    validated = Column(Boolean, default=False)
    
    # Relationships
    clauses = relationship("ClauseExtraction", back_populates="contract", cascade="all, delete-orphan")
    validations = relationship("ValidationResult", back_populates="contract", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Contract(id={self.id}, name={self.name}, file_type={self.file_type})>"
