"""
Clause Analysis Service
Manages extraction and storage of clauses
"""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models import Contract, ClauseExtraction
from app.ai_module.gemini_extractor import GeminiClauseExtractor

logger = logging.getLogger(__name__)


class ClauseAnalysisService:
    """Service for analyzing and managing contract clauses"""
    
    def __init__(self):
        self.extractor = GeminiClauseExtractor()
    
    def analyze_contract(self, db: Session, contract_id: int) -> List[ClauseExtraction]:
        """
        Analyze contract and extract clauses
        
        Args:
            db: Database session
            contract_id: ID of contract to analyze
        
        Returns:
            List of extracted clauses
        """
        try:
            contract = db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                raise ValueError(f"Contract not found: {contract_id}")
            
            if not contract.raw_text:
                raise ValueError(f"Contract has no text extracted: {contract_id}")
            
            # Extract clauses using Gemini
            extracted_clauses = self.extractor.extract_clauses(contract.raw_text)
            
            # Store in database
            clause_records = []
            for clause_data in extracted_clauses:
                clause = ClauseExtraction(
                    contract_id=contract_id,
                    clause_type=clause_data.get("clause_type"),
                    clause_text=clause_data.get("clause_text"),
                    confidence_score=clause_data.get("confidence_score"),
                    extracted_data=clause_data.get("extracted_data"),
                    source="gemini_api"
                )
                db.add(clause)
                clause_records.append(clause)
            
            # Update contract status
            contract.clauses_extracted = True
            
            db.commit()
            logger.info(f"Extracted {len(clause_records)} clauses for contract {contract_id}")
            
            return clause_records
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to analyze contract: {str(e)}")
            raise
    
    def get_clauses_by_type(self, db: Session, contract_id: int, clause_type: str) -> List[ClauseExtraction]:
        """Get all clauses of a specific type for a contract"""
        return db.query(ClauseExtraction).filter(
            ClauseExtraction.contract_id == contract_id,
            ClauseExtraction.clause_type == clause_type
        ).all()
    
    def get_all_clauses(self, db: Session, contract_id: int) -> List[ClauseExtraction]:
        """Get all extracted clauses for a contract"""
        return db.query(ClauseExtraction).filter(
            ClauseExtraction.contract_id == contract_id
        ).all()
    
    def compare_clauses(self, contract_1_clauses: List[ClauseExtraction], 
                       contract_2_clauses: List[ClauseExtraction]) -> Dict[str, Any]:
        """
        Compare clauses between two contracts
        
        Returns:
            Dictionary with comparison results
        """
        differences = {
            "missing_in_contract2": [],
            "missing_in_contract1": [],
            "different": []
        }
        
        # Get clause types
        types_1 = {c.clause_type: c for c in contract_1_clauses}
        types_2 = {c.clause_type: c for c in contract_2_clauses}
        
        # Find missing clauses
        for clause_type in types_1:
            if clause_type not in types_2:
                differences["missing_in_contract2"].append(clause_type)
        
        for clause_type in types_2:
            if clause_type not in types_1:
                differences["missing_in_contract1"].append(clause_type)
        
        # Compare matching clauses
        for clause_type in types_1:
            if clause_type in types_2:
                if types_1[clause_type].clause_text != types_2[clause_type].clause_text:
                    differences["different"].append({
                        "clause_type": clause_type,
                        "text_1": types_1[clause_type].clause_text[:100] + "...",
                        "text_2": types_2[clause_type].clause_text[:100] + "..."
                    })
        
        return differences
