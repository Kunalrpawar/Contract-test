"""
Advanced analysis routes using LangChain
Provides contract summarization, entity extraction, and risk analysis
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import Contract
from app.ai_module.langchain_analyzer import contract_analyzer
from app.schemas import ContractResponse
from pydantic import BaseModel
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Advanced Analysis"])


class SummaryResponse(BaseModel):
    """Response model for contract summary"""
    contract_id: int
    summary: str
    chunk_count: int
    method: str


class EntityExtractionResponse(BaseModel):
    """Response model for entity extraction"""
    contract_id: int
    entities: Dict[str, Any]
    method: str


class RiskAnalysisResponse(BaseModel):
    """Response model for risk analysis"""
    contract_id: int
    risks: Dict[str, Any]
    method: str


class ContractComparisonResponse(BaseModel):
    """Response model for contract comparison"""
    contract_1_id: int
    contract_2_id: int
    comparison: Dict[str, Any]
    method: str


@router.post("/analyze/{contract_id}/summary", response_model=SummaryResponse)
async def summarize_contract(
    contract_id: int,
    db: Session = Depends(get_db)
) -> SummaryResponse:
    """
    Generate AI-powered summary of contract using LangChain
    
    Args:
        contract_id: ID of contract to summarize
        db: Database session
    
    Returns:
        Contract summary with metadata
    """
    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        if not contract.raw_text:
            raise HTTPException(status_code=400, detail="Contract text not extracted")
        
        result = contract_analyzer.summarize_contract(contract.raw_text)
        
        return SummaryResponse(
            contract_id=contract_id,
            summary=result.get("summary", ""),
            chunk_count=result.get("chunk_count", 0),
            method=result.get("method", "unknown")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error summarizing contract {contract_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/{contract_id}/entities", response_model=EntityExtractionResponse)
async def extract_entities(
    contract_id: int,
    db: Session = Depends(get_db)
) -> EntityExtractionResponse:
    """
    Extract key entities from contract using LangChain
    (parties, dates, amounts, payment terms)
    
    Args:
        contract_id: ID of contract
        db: Database session
    
    Returns:
        Extracted entities
    """
    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        if not contract.raw_text:
            raise HTTPException(status_code=400, detail="Contract text not extracted")
        
        result = contract_analyzer.extract_entities(contract.raw_text)
        
        return EntityExtractionResponse(
            contract_id=contract_id,
            entities=result.get("entities", {}),
            method=result.get("method", "unknown")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting entities from contract {contract_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/{contract_id}/risks", response_model=RiskAnalysisResponse)
async def analyze_risks(
    contract_id: int,
    db: Session = Depends(get_db)
) -> RiskAnalysisResponse:
    """
    Analyze contract for risks and concerns using LangChain
    
    Args:
        contract_id: ID of contract
        db: Database session
    
    Returns:
        Risk analysis with recommendations
    """
    try:
        from app.models import ClauseExtraction
        
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        if not contract.raw_text:
            raise HTTPException(status_code=400, detail="Contract text not extracted")
        
        # Get clauses for context
        clauses = db.query(ClauseExtraction).filter(
            ClauseExtraction.contract_id == contract_id
        ).all()
        
        clause_dicts = [
            {
                "clause_type": c.clause_type,
                "confidence_score": c.confidence_score
            }
            for c in clauses
        ]
        
        result = contract_analyzer.analyze_risks(contract.raw_text, clause_dicts)
        
        return RiskAnalysisResponse(
            contract_id=contract_id,
            risks=result.get("risks", {}),
            method=result.get("method", "unknown")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing risks for contract {contract_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/analyze/compare/{contract_1_id}/{contract_2_id}",
    response_model=ContractComparisonResponse
)
async def compare_contracts_advanced(
    contract_1_id: int,
    contract_2_id: int,
    db: Session = Depends(get_db)
) -> ContractComparisonResponse:
    """
    Compare two contracts using LangChain for detailed analysis
    
    Args:
        contract_1_id: ID of first contract
        contract_2_id: ID of second contract
        db: Database session
    
    Returns:
        Detailed comparison with differences and risks
    """
    try:
        contract1 = db.query(Contract).filter(Contract.id == contract_1_id).first()
        contract2 = db.query(Contract).filter(Contract.id == contract_2_id).first()
        
        if not contract1:
            raise HTTPException(status_code=404, detail=f"Contract {contract_1_id} not found")
        if not contract2:
            raise HTTPException(status_code=404, detail=f"Contract {contract_2_id} not found")
        
        if not contract1.raw_text or not contract2.raw_text:
            raise HTTPException(status_code=400, detail="Both contracts must have extracted text")
        
        result = contract_analyzer.compare_contracts(contract1.raw_text, contract2.raw_text)
        
        return ContractComparisonResponse(
            contract_1_id=contract_1_id,
            contract_2_id=contract_2_id,
            comparison=result.get("comparison", {}),
            method=result.get("method", "unknown")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing contracts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{contract_id}/insights")
async def get_contract_insights(
    contract_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get comprehensive insights about a contract
    Combines summary, entities, and risk analysis
    
    Args:
        contract_id: ID of contract
        db: Database session
    
    Returns:
        Comprehensive insights dictionary
    """
    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        if not contract.raw_text:
            raise HTTPException(status_code=400, detail="Contract text not extracted")
        
        # Get summary
        summary = contract_analyzer.summarize_contract(contract.raw_text)
        
        # Get entities
        entities = contract_analyzer.extract_entities(contract.raw_text)
        
        # Get risks
        clauses = db.query(ClauseExtraction).filter(
            ClauseExtraction.contract_id == contract_id
        ).all()
        
        clause_dicts = [
            {"clause_type": c.clause_type, "confidence_score": c.confidence_score}
            for c in clauses
        ]
        
        risks = contract_analyzer.analyze_risks(contract.raw_text, clause_dicts)
        
        return {
            "contract_id": contract_id,
            "summary": summary.get("summary"),
            "entities": entities.get("entities"),
            "risks": risks.get("risks"),
            "metadata": {
                "file_size": contract.file_size,
                "uploaded_at": contract.uploaded_at.isoformat(),
                "clauses_count": len(clauses)
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting insights for contract {contract_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
