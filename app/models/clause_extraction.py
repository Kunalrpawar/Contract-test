"""
Clause Extraction Model - Database schema for extracted clauses
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ClauseExtraction(Base):
    """ClauseExtraction model for storing AI-extracted clauses"""
    __tablename__ = "clause_extractions"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    
    # Clause types
    clause_type = Column(String(100), nullable=False)  # SLA, PaymentTerms, Termination, Confidentiality, etc.
    clause_text = Column(Text, nullable=True)
    confidence_score = Column(Integer, nullable=True)  # 0-100
    
    # Extracted data (JSON for flexibility)
    extracted_data = Column(JSON, nullable=True)
    
    # Metadata
    extracted_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50), default="gemini_api")  # gemini_api, spacy, transformer
    
    # Relationship
    contract = relationship("Contract", back_populates="clauses")
    
    def __repr__(self):
        return f"<ClauseExtraction(id={self.id}, contract_id={self.contract_id}, clause_type={self.clause_type})>"
