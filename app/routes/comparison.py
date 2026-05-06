"""
Contract Comparison Routes
Handles comparison between two contracts
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.ai_module import ClauseAnalysisService
from app.schemas import ComparisonResponse
from app.services import ContractService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/compare", tags=["comparison"])

clause_service = ClauseAnalysisService()


@router.post("/{contract_1_id}/{contract_2_id}", response_model=ComparisonResponse)
def compare_contracts(
    contract_1_id: int,
    contract_2_id: int,
    db: Session = Depends(get_db)
):
    """
    Compare two contract versions and highlight differences
    
    Args:
        contract_1_id: ID of first contract
        contract_2_id: ID of second contract
    
    Returns:
        Comparison results with differences
    """
    try:
        # Get both contracts
        contract_1 = ContractService.get_contract(db, contract_1_id)
        contract_2 = ContractService.get_contract(db, contract_2_id)
        
        if not contract_1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract not found: {contract_1_id}"
            )
        
        if not contract_2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract not found: {contract_2_id}"
            )
        
        # Get clauses for both contracts
        clauses_1 = clause_service.get_all_clauses(db, contract_1_id)
        clauses_2 = clause_service.get_all_clauses(db, contract_2_id)
        
        if not clauses_1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contract {contract_1_id} has no extracted clauses. Run analysis first."
            )
        
        if not clauses_2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Contract {contract_2_id} has no extracted clauses. Run analysis first."
            )
        
        # Compare clauses
        differences = clause_service.compare_clauses(clauses_1, clauses_2)
        
        # Calculate similarity (simple metric)
        total_unique_types = len(set([c.clause_type for c in clauses_1 + clauses_2]))
        common_types = len(set([c.clause_type for c in clauses_1]) & set([c.clause_type for c in clauses_2]))
        similarity_score = (common_types / total_unique_types * 100) if total_unique_types > 0 else 0
        
        return ComparisonResponse(
            contract_1_id=contract_1_id,
            contract_2_id=contract_2_id,
            differences=differences,
            similarity_score=round(similarity_score, 2)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error comparing contracts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare contracts: {str(e)}"
        )
