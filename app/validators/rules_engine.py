"""
Validation Rules Engine
Defines and executes business rules for contract validation
"""

import logging
from typing import List, Callable, Dict, Any
from dataclasses import dataclass
from sqlalchemy.orm import Session
from app.models import Contract, ClauseExtraction, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class ValidationRule:
    """Represents a validation rule"""
    name: str
    description: str
    severity: str  # ERROR, WARNING, INFO
    rule_func: Callable


class ValidationRulesEngine:
    """Engine for running validation rules against contracts"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[ValidationRule]:
        """Initialize all validation rules"""
        return [
            ValidationRule(
                name="Missing SLA",
                description="Contract must contain Service Level Agreement clause",
                severity="ERROR",
                rule_func=self._check_sla
            ),
            ValidationRule(
                name="Missing Confidentiality",
                description="Contract should contain Confidentiality clause",
                severity="WARNING",
                rule_func=self._check_confidentiality
            ),
            ValidationRule(
                name="Payment Terms Exceeds 60 Days",
                description="Payment terms exceeding 60 days may indicate cash flow risk",
                severity="WARNING",
                rule_func=self._check_payment_terms
            ),
            ValidationRule(
                name="Missing Termination Clause",
                description="Contract must include termination conditions",
                severity="ERROR",
                rule_func=self._check_termination
            ),
            ValidationRule(
                name="Missing Warranty",
                description="Contract should specify warranty terms",
                severity="WARNING",
                rule_func=self._check_warranty
            ),
            ValidationRule(
                name="Missing Liability",
                description="Contract should specify liability limits",
                severity="INFO",
                rule_func=self._check_liability
            ),
            ValidationRule(
                name="Missing Dispute Resolution",
                description="Contract should define dispute resolution mechanism",
                severity="WARNING",
                rule_func=self._check_dispute_resolution
            ),
            ValidationRule(
                name="Contract Text Empty",
                description="Contract text must be extracted",
                severity="ERROR",
                rule_func=self._check_text_extracted
            ),
        ]
    
    def validate_contract(self, db: Session, contract_id: int) -> List[ValidationResult]:
        """
        Run all validation rules against a contract
        
        Args:
            db: Database session
            contract_id: ID of contract to validate
        
        Returns:
            List of validation results
        """
        try:
            contract = db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                raise ValueError(f"Contract not found: {contract_id}")
            
            results = []
            clauses = db.query(ClauseExtraction).filter(
                ClauseExtraction.contract_id == contract_id
            ).all()
            
            # Run each rule
            for rule in self.rules:
                try:
                    is_passed, message = rule.rule_func(contract, clauses)
                    
                    validation_result = ValidationResult(
                        contract_id=contract_id,
                        rule_name=rule.name,
                        rule_description=rule.description,
                        severity=rule.severity,
                        is_passed=is_passed,
                        message=message
                    )
                    
                    db.add(validation_result)
                    results.append(validation_result)
                    
                    logger.info(f"Rule '{rule.name}' - Passed: {is_passed}")
                
                except Exception as e:
                    logger.error(f"Error executing rule '{rule.name}': {str(e)}")
            
            # Update contract status
            contract.validated = True
            
            db.commit()
            logger.info(f"Validation completed for contract {contract_id}")
            
            return results
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to validate contract: {str(e)}")
            raise
    
    # Rule implementation methods
    
    @staticmethod
    def _check_sla(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if SLA clause exists"""
        sla_exists = any(c.clause_type == "SLA" for c in clauses)
        return sla_exists, "SLA clause " + ("found" if sla_exists else "NOT found - critical")
    
    @staticmethod
    def _check_confidentiality(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if Confidentiality clause exists"""
        conf_exists = any(c.clause_type == "Confidentiality" for c in clauses)
        return conf_exists, "Confidentiality clause " + ("found" if conf_exists else "NOT found")
    
    @staticmethod
    def _check_payment_terms(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check payment terms - flag if > 60 days"""
        payment_clause = next((c for c in clauses if c.clause_type == "PaymentTerms"), None)
        
        if not payment_clause:
            return True, "No payment terms found (not flagged)"
        
        try:
            if payment_clause.extracted_data and "payment_days" in payment_clause.extracted_data:
                days = int(payment_clause.extracted_data["payment_days"])
                if days > 60:
                    return False, f"Payment terms ({days} days) exceed 60-day threshold"
            return True, "Payment terms within acceptable range"
        except Exception:
            return True, "Could not parse payment terms"
    
    @staticmethod
    def _check_termination(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if Termination clause exists"""
        term_exists = any(c.clause_type == "Termination" for c in clauses)
        return term_exists, "Termination clause " + ("found" if term_exists else "NOT found - critical")
    
    @staticmethod
    def _check_warranty(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if Warranty clause exists"""
        warranty_exists = any(c.clause_type == "Warranty" for c in clauses)
        return warranty_exists, "Warranty clause " + ("found" if warranty_exists else "NOT found")
    
    @staticmethod
    def _check_liability(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if Liability clause exists"""
        liability_exists = any(c.clause_type == "Liability" for c in clauses)
        return liability_exists, "Liability clause " + ("found" if liability_exists else "NOT found")
    
    @staticmethod
    def _check_dispute_resolution(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if Dispute Resolution clause exists"""
        dispute_exists = any(c.clause_type == "Dispute Resolution" for c in clauses)
        return dispute_exists, "Dispute Resolution clause " + ("found" if dispute_exists else "NOT found")
    
    @staticmethod
    def _check_text_extracted(contract: Contract, clauses: List[ClauseExtraction]) -> tuple:
        """Check if contract text was successfully extracted"""
        extracted = bool(contract.text_extracted and contract.raw_text)
        return extracted, "Contract text " + ("extracted" if extracted else "NOT extracted")
