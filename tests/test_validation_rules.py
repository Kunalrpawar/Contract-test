"""
Unit Tests for Validation Rules Engine
"""

import pytest
from sqlalchemy.orm import Session
from app.models import Contract, ClauseExtraction
from app.validators import ValidationRulesEngine
from datetime import datetime


class TestValidationRulesEngine:
    """Test validation rules engine"""
    
    @pytest.fixture
    def engine(self):
        """Create validation engine"""
        return ValidationRulesEngine()
    
    def test_engine_initialization(self, engine):
        """Test engine initializes with correct rules"""
        assert engine.rules is not None
        assert len(engine.rules) > 0
        assert all(hasattr(rule, "name") for rule in engine.rules)
        assert all(hasattr(rule, "severity") for rule in engine.rules)
    
    def test_check_sla_rule_passes(self):
        """Test SLA rule passes when clause exists"""
        contract = Contract(id=1, name="Test", file_path="test.pdf", file_type="pdf", file_size=100)
        clauses = [
            ClauseExtraction(id=1, contract_id=1, clause_type="SLA", clause_text="SLA text")
        ]
        
        passed, message = ValidationRulesEngine._check_sla(contract, clauses)
        assert passed is True
        assert "found" in message.lower()
    
    def test_check_sla_rule_fails(self):
        """Test SLA rule fails when clause missing"""
        contract = Contract(id=1, name="Test", file_path="test.pdf", file_type="pdf", file_size=100)
        clauses = []
        
        passed, message = ValidationRulesEngine._check_sla(contract, clauses)
        assert passed is False
        assert "NOT found" in message
    
    def test_check_payment_terms_rule(self):
        """Test payment terms rule with various scenarios"""
        contract = Contract(id=1, name="Test", file_path="test.pdf", file_type="pdf", file_size=100)
        
        # Payment > 60 days
        clauses_over_60 = [
            ClauseExtraction(
                id=1, contract_id=1, clause_type="PaymentTerms", clause_text="Payment",
                extracted_data={"payment_days": 90}
            )
        ]
        passed, message = ValidationRulesEngine._check_payment_terms(contract, clauses_over_60)
        assert passed is False
        assert "exceed" in message.lower()
        
        # Payment <= 60 days
        clauses_within_60 = [
            ClauseExtraction(
                id=1, contract_id=1, clause_type="PaymentTerms", clause_text="Payment",
                extracted_data={"payment_days": 30}
            )
        ]
        passed, message = ValidationRulesEngine._check_payment_terms(contract, clauses_within_60)
        assert passed is True
        assert "acceptable" in message.lower()
    
    def test_check_text_extracted_rule(self):
        """Test text extraction check"""
        # Text extracted
        contract_with_text = Contract(
            id=1, name="Test", file_path="test.pdf", file_type="pdf", 
            file_size=100, text_extracted=True, raw_text="Some content"
        )
        passed, message = ValidationRulesEngine._check_text_extracted(contract_with_text, [])
        assert passed is True
        
        # Text not extracted
        contract_without_text = Contract(
            id=2, name="Test", file_path="test.pdf", file_type="pdf",
            file_size=100, text_extracted=False, raw_text=None
        )
        passed, message = ValidationRulesEngine._check_text_extracted(contract_without_text, [])
        assert passed is False
    
    def test_validate_contract_complete(self, db: Session):
        """Test complete validation process"""
        engine = ValidationRulesEngine()
        
        # Create contract
        contract = Contract(
            name="Test Contract",
            file_path="test.pdf",
            file_type="pdf",
            file_size=1000,
            text_extracted=True,
            raw_text="Sample contract text"
        )
        db.add(contract)
        db.commit()
        
        # Add some clauses
        for clause_type in ["SLA", "PaymentTerms", "Termination", "Confidentiality"]:
            clause = ClauseExtraction(
                contract_id=contract.id,
                clause_type=clause_type,
                clause_text=f"{clause_type} text",
                confidence_score=85
            )
            db.add(clause)
        db.commit()
        
        # Run validation
        results = engine.validate_contract(db, contract.id)
        
        assert len(results) > 0
        assert all(hasattr(r, "rule_name") for r in results)
        assert all(hasattr(r, "is_passed") for r in results)
        
        # Check contract marked as validated
        db.refresh(contract)
        assert contract.validated is True
