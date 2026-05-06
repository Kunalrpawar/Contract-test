"""
Contract Analysis Routes
Handles clause extraction and analysis
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.ai_module import ClauseAnalysisService
from app.schemas import AnalysisResponse, ClauseExtractionResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/analyze", tags=["analysis"])

clause_service = ClauseAnalysisService()


@router.post("/{contract_id}", response_model=AnalysisResponse)
def analyze_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze contract and extract key clauses using AI
    
    Args:
        contract_id: ID of contract to analyze
    
    Returns:
        List of extracted clauses with metadata
    """
    try:
        clauses = clause_service.analyze_contract(db, contract_id)
        
        return AnalysisResponse(
            contract_id=contract_id,
            status="success",
            clauses=[ClauseExtractionResponse.model_validate(c) for c in clauses]
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Error analyzing contract: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze contract: {str(e)}"
        )


@router.get("/{contract_id}/clauses", response_model=list[ClauseExtractionResponse])
def get_contract_clauses(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Get all extracted clauses for a contract"""
    try:
        clauses = clause_service.get_all_clauses(db, contract_id)
        
        if not clauses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No clauses found for contract {contract_id}"
            )
        
        return [ClauseExtractionResponse.model_validate(c) for c in clauses]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving clauses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve clauses: {str(e)}"
        )


@router.get("/{contract_id}/clauses/{clause_type}", response_model=list[ClauseExtractionResponse])
def get_clauses_by_type(
    contract_id: int,
    clause_type: str,
    db: Session = Depends(get_db)
):
    """Get clauses of a specific type for a contract"""
    try:
        clauses = clause_service.get_clauses_by_type(db, contract_id, clause_type)
        
        if not clauses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No {clause_type} clauses found for contract {contract_id}"
            )
        
        return [ClauseExtractionResponse.model_validate(c) for c in clauses]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving {clause_type} clauses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve clauses: {str(e)}"
        )
