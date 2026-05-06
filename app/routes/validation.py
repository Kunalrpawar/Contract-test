"""
Contract Validation Routes
Handles validation rule execution
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.validators import ValidationRulesEngine
from app.schemas import ValidationResponse, ValidationResultResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/validate", tags=["validation"])

validator = ValidationRulesEngine()


@router.post("/{contract_id}", response_model=ValidationResponse)
def validate_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """
    Validate contract against business rules
    
    Args:
        contract_id: ID of contract to validate
    
    Returns:
        Validation results with errors, warnings, and info
    """
    try:
        results = validator.validate_contract(db, contract_id)
        
        # Calculate summary
        summary = {
            "errors": sum(1 for r in results if r.severity == "ERROR" and not r.is_passed),
            "warnings": sum(1 for r in results if r.severity == "WARNING" and not r.is_passed),
            "info": sum(1 for r in results if r.severity == "INFO" and not r.is_passed),
            "total": len(results),
            "passed": sum(1 for r in results if r.is_passed)
        }
        
        return ValidationResponse(
            contract_id=contract_id,
            status="success",
            results=[ValidationResultResponse.model_validate(r) for r in results],
            summary=summary
        )
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Error validating contract: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate contract: {str(e)}"
        )
