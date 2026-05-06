"""
Tests for LangChain integration and advanced analysis
"""

import pytest
from app.ai_module.langchain_analyzer import ContractAnalyzer, contract_analyzer
from app.models import Contract


@pytest.fixture
def analyzer():
    """Fixture providing analyzer instance"""
    return ContractAnalyzer()


@pytest.fixture
def sample_contract_text():
    """Sample contract for testing"""
    return """
    SERVICE AGREEMENT
    
    This Agreement is entered into between Company A ("Client") and Company B ("Provider").
    
    TERM: This agreement shall be effective for 12 months from the date of execution.
    
    TERMINATION: Either party may terminate this agreement with 30 days written notice.
    
    PAYMENT TERMS: Invoices shall be paid within 45 days of receipt.
    
    WARRANTY: Services are provided as-is without express or implied warranties.
    
    CONFIDENTIALITY: All information shall be kept confidential for 3 years following termination.
    
    LIABILITY LIMITATION: Neither party shall be liable for consequential damages.
    
    DISPUTE RESOLUTION: Disputes shall be resolved through binding arbitration.
    """


class TestLangChainAnalyzer:
    """Test LangChain contract analyzer"""
    
    def test_analyzer_initialization(self, analyzer):
        """Test analyzer initializes properly"""
        assert analyzer is not None
        assert analyzer.text_splitter is not None
    
    def test_summarize_contract(self, analyzer, sample_contract_text):
        """Test contract summarization"""
        result = analyzer.summarize_contract(sample_contract_text)
        
        assert "status" in result
        assert result["status"] == "success"
        assert "summary" in result
        assert len(result["summary"]) > 0
        assert "method" in result
    
    def test_extract_entities(self, analyzer, sample_contract_text):
        """Test entity extraction"""
        result = analyzer.extract_entities(sample_contract_text)
        
        assert "status" in result
        assert result["status"] == "success"
        assert "entities" in result
        assert "method" in result
    
    def test_analyze_risks(self, analyzer, sample_contract_text):
        """Test risk analysis"""
        clauses = [
            {"clause_type": "Termination", "confidence_score": 0.95},
            {"clause_type": "Warranty", "confidence_score": 0.88}
        ]
        
        result = analyzer.analyze_risks(sample_contract_text, clauses)
        
        assert "status" in result
        assert result["status"] == "success"
        assert "risks" in result
        assert "method" in result
    
    def test_compare_contracts(self, analyzer, sample_contract_text):
        """Test contract comparison"""
        contract2 = """
        AGREEMENT
        
        TERM: 24 months
        PAYMENT: 30 days
        TERMINATION: 60 days notice required
        LIABILITY: Limited to contract value
        """
        
        result = analyzer.compare_contracts(sample_contract_text, contract2)
        
        assert "status" in result
        assert result["status"] == "success"
        assert "comparison" in result
        assert "method" in result
    
    def test_global_analyzer(self, sample_contract_text):
        """Test global analyzer instance"""
        result = contract_analyzer.summarize_contract(sample_contract_text)
        
        assert "status" in result
        assert "summary" in result
    
    def test_empty_contract_handling(self, analyzer):
        """Test handling of empty contract"""
        result = analyzer.summarize_contract("")
        
        assert "status" in result
        # Should handle gracefully
        assert "summary" in result or "error" in result.get("method", "").lower()
    
    def test_large_contract_handling(self, analyzer):
        """Test handling of large contracts"""
        large_contract = "Lorem ipsum " * 5000  # ~40KB of text
        
        result = analyzer.summarize_contract(large_contract)
        
        assert "status" in result
        # Should handle without errors
    
    def test_mock_fallback(self):
        """Test mock analysis fallback"""
        # Test mock summarization
        result = ContractAnalyzer._mock_summarize("test contract")
        
        assert result["status"] == "success"
        assert "summary" in result
        assert result["method"] == "mock"
    
    def test_entity_extraction_structure(self, analyzer, sample_contract_text):
        """Test entity extraction returns structured data"""
        result = analyzer.extract_entities(sample_contract_text)
        
        assert "status" in result
        assert "entities" in result
        
        entities = result["entities"]
        # Should be dict or contain structured data
        assert isinstance(entities, (dict, str, list))
    
    def test_risk_analysis_structure(self, analyzer, sample_contract_text):
        """Test risk analysis returns structured data"""
        clauses = [{"clause_type": "Termination", "confidence_score": 0.9}]
        result = analyzer.analyze_risks(sample_contract_text, clauses)
        
        assert "status" in result
        assert "risks" in result
        
        risks = result["risks"]
        # Should contain analysis
        assert isinstance(risks, (dict, str, list))


class TestContractAnalyzerEdgeCases:
    """Test edge cases and error handling"""
    
    def test_none_contract_text(self):
        """Test handling of None contract text"""
        analyzer = ContractAnalyzer()
        
        try:
            result = analyzer.summarize_contract(None)
            # Should either handle gracefully or raise
            assert result.get("status") in ["success", "error"]
        except (TypeError, AttributeError):
            # Expected behavior for None input
            pass
    
    def test_special_characters_handling(self):
        """Test handling of special characters"""
        analyzer = ContractAnalyzer()
        
        text = "Contract with special chars: © ® ™ € £ ¥ — – • … ‰"
        result = analyzer.summarize_contract(text)
        
        # Should handle without errors
        assert "status" in result
    
    def test_multiple_languages(self):
        """Test handling of multi-language contracts"""
        analyzer = ContractAnalyzer()
        
        text = "English text\n日本語テキスト\nTexto en español\nТекст на русском"
        result = analyzer.summarize_contract(text)
        
        # Should handle gracefully
        assert "status" in result
    
    def test_concurrent_analysis(self):
        """Test multiple concurrent analyses"""
        analyzer = ContractAnalyzer()
        
        contracts = [
            "Contract 1: Test content",
            "Contract 2: More test content",
            "Contract 3: Even more content"
        ]
        
        results = []
        for contract in contracts:
            result = analyzer.summarize_contract(contract)
            results.append(result)
        
        # All should succeed
        assert len(results) == 3
        assert all(r.get("status") == "success" for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
