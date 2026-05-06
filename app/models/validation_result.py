"""
Validation Result Model - Database schema for validation results
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ValidationResult(Base):
    """ValidationResult model for storing validation rules results"""
    __tablename__ = "validation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    
    # Validation details
    rule_name = Column(String(255), nullable=False)
    rule_description = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False)  # ERROR, WARNING, INFO
    is_passed = Column(Boolean, nullable=False)
    message = Column(Text, nullable=True)
    
    # Metadata
    validated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    contract = relationship("Contract", back_populates="validations")
    
    def __repr__(self):
        return f"<ValidationResult(id={self.id}, contract_id={self.contract_id}, rule_name={self.rule_name}, severity={self.severity})>"
