"""
Pydantic Schema Models for API Request/Response
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ContractBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class ContractCreate(ContractBase):
    pass


class ContractResponse(ContractBase):
    id: int
    file_type: str
    file_size: int
    text_extracted: bool
    clauses_extracted: bool
    validated: bool
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class ContractDetailResponse(ContractResponse):
    raw_text: Optional[str] = None
    clauses: List["ClauseExtractionResponse"] = []
    validations: List["ValidationResultResponse"] = []


class ClauseExtractionBase(BaseModel):
    clause_type: str
    clause_text: Optional[str] = None
    confidence_score: Optional[int] = Field(None, ge=0, le=100)


class ClauseExtractionResponse(ClauseExtractionBase):
    id: int
    contract_id: int
    extracted_data: Optional[Dict[str, Any]] = None
    extracted_at: datetime
    source: str
    
    class Config:
        from_attributes = True


class ValidationResultBase(BaseModel):
    rule_name: str
    rule_description: Optional[str] = None
    severity: str  # ERROR, WARNING, INFO
    is_passed: bool
    message: Optional[str] = None


class ValidationResultResponse(ValidationResultBase):
    id: int
    contract_id: int
    validated_at: datetime
    
    class Config:
        from_attributes = True


class AnalysisResponse(BaseModel):
    contract_id: int
    status: str  # success, error
    clauses: List[ClauseExtractionResponse] = []
    message: Optional[str] = None


class ValidationResponse(BaseModel):
    contract_id: int
    status: str  # success, error
    results: List[ValidationResultResponse] = []
    message: Optional[str] = None
    summary: Dict[str, int] = {}  # {errors: 0, warnings: 0, info: 0}


class ComparisonResponse(BaseModel):
    contract_1_id: int
    contract_2_id: int
    differences: Dict[str, Any]
    similarity_score: Optional[float] = None


class ContractDetailResponse.model_rebuild()
