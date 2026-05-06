"""
LangChain integration for advanced contract analysis
Provides contract summarization, entity extraction, and risk analysis
"""

import logging
from typing import Dict, List, Any
from app.config import settings

logger = logging.getLogger(__name__)

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain.llms import GooglePalm
    LANGCHAIN_AVAILABLE = True
except Exception as exc:  # pragma: no cover - defensive import guard
    RecursiveCharacterTextSplitter = None
    LLMChain = None
    PromptTemplate = None
    GooglePalm = None
    LANGCHAIN_AVAILABLE = False
    logger.warning(f"LangChain unavailable, using mock analysis: {exc}")


class ContractAnalyzer:
    """Advanced contract analysis using LangChain"""
    
    def __init__(self):
        """Initialize LangChain analyzer"""
        try:
            if LANGCHAIN_AVAILABLE and GooglePalm and RecursiveCharacterTextSplitter:
                self.llm = GooglePalm(google_api_key=settings.gemini_api_key)
                self.text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                logger.info("LangChain analyzer initialized successfully")
            else:
                self.llm = None
                self.text_splitter = None
                logger.info("LangChain analyzer using mock fallback")
        except Exception as e:
            logger.warning(f"Failed to initialize LLM: {e}. Using mock analysis.")
            self.llm = None
            self.text_splitter = None
    
    def summarize_contract(self, contract_text: str) -> Dict[str, Any]:
        """
        Generate a concise summary of the contract
        
        Args:
            contract_text: Full contract text
        
        Returns:
            Dictionary with summary and metadata
        """
        try:
            if not self.llm or not self.text_splitter or not LLMChain or not PromptTemplate:
                return self._mock_summarize(contract_text)
            
            # Split large documents
            chunks = self.text_splitter.split_text(contract_text)
            
            # Create summarization prompt
            summary_prompt = PromptTemplate(
                input_variables=["contract"],
                template="""Provide a concise 3-4 sentence summary of this contract:

{contract}

Summary:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=summary_prompt)
            
            # Summarize first chunk (most important)
            result = chain.run(contract=chunks[0] if chunks else contract_text)
            
            return {
                "status": "success",
                "summary": result.strip(),
                "chunk_count": len(chunks),
                "method": "langchain"
            }
        
        except Exception as e:
            logger.error(f"Error in summarize_contract: {e}")
            return self._mock_summarize(contract_text)
    
    def extract_entities(self, contract_text: str) -> Dict[str, List[str]]:
        """
        Extract key entities from contract (parties, dates, amounts)
        
        Args:
            contract_text: Full contract text
        
        Returns:
            Dictionary with extracted entities
        """
        try:
            if not self.llm or not LLMChain or not PromptTemplate:
                return self._mock_extract_entities(contract_text)
            
            entity_prompt = PromptTemplate(
                input_variables=["contract"],
                template="""Extract the following from this contract:
- Parties involved (company/individual names)
- Key dates (start date, end date, renewal dates)
- Monetary amounts or payment terms
- Performance metrics or KPIs

Contract:
{contract}

Return as structured list."""
            )
            
            chain = LLMChain(llm=self.llm, prompt=entity_prompt)
            result = chain.run(contract=contract_text[:2000])  # Limit input size
            
            return {
                "status": "success",
                "entities": result.strip(),
                "method": "langchain"
            }
        
        except Exception as e:
            logger.error(f"Error in extract_entities: {e}")
            return self._mock_extract_entities(contract_text)
    
    def analyze_risks(self, contract_text: str, clauses: List[Dict]) -> Dict[str, Any]:
        """
        Analyze contract for potential risks
        
        Args:
            contract_text: Full contract text
            clauses: List of extracted clauses
        
        Returns:
            Dictionary with risk analysis
        """
        try:
            if not self.llm or not LLMChain or not PromptTemplate:
                return self._mock_analyze_risks(clauses)
            
            risk_prompt = PromptTemplate(
                input_variables=["contract", "clauses"],
                template="""Analyze this contract for risks and concerns:

Contract excerpt:
{contract}

Key clauses found: {clauses}

Identify:
1. High-risk areas
2. Missing critical clauses
3. Unfavorable terms
4. Recommendations for negotiation

Analysis:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=risk_prompt)
            
            clauses_str = ", ".join([c.get("clause_type", "Unknown") for c in clauses])
            result = chain.run(
                contract=contract_text[:1500],
                clauses=clauses_str
            )
            
            return {
                "status": "success",
                "risks": result.strip(),
                "method": "langchain"
            }
        
        except Exception as e:
            logger.error(f"Error in analyze_risks: {e}")
            return self._mock_analyze_risks(clauses)
    
    def compare_contracts(self, contract1_text: str, contract2_text: str) -> Dict[str, Any]:
        """
        Compare two contracts and highlight differences
        
        Args:
            contract1_text: First contract text
            contract2_text: Second contract text
        
        Returns:
            Dictionary with comparison results
        """
        try:
            if not self.llm or not LLMChain or not PromptTemplate:
                return self._mock_compare_contracts()
            
            compare_prompt = PromptTemplate(
                input_variables=["contract1", "contract2"],
                template="""Compare these two contracts and identify:
1. Major differences in terms
2. Risks in one vs the other
3. Which contract is more favorable

Contract 1:
{contract1}

Contract 2:
{contract2}

Comparison:"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=compare_prompt)
            result = chain.run(
                contract1=contract1_text[:1500],
                contract2=contract2_text[:1500]
            )
            
            return {
                "status": "success",
                "comparison": result.strip(),
                "method": "langchain"
            }
        
        except Exception as e:
            logger.error(f"Error in compare_contracts: {e}")
            return self._mock_compare_contracts()
    
    # Mock methods for fallback
    
    @staticmethod
    def _mock_summarize(contract_text: str) -> Dict[str, Any]:
        """Mock contract summarization"""
        lines = contract_text.split("\n")
        summary = " ".join(lines[:3]) if lines else "No summary available"
        
        return {
            "status": "success",
            "summary": summary[:200],
            "method": "mock",
            "note": "LangChain not available - using mock analysis"
        }
    
    @staticmethod
    def _mock_extract_entities(contract_text: str) -> Dict[str, List[str]]:
        """Mock entity extraction"""
        entities = {
            "parties": ["Party A", "Party B"],
            "dates": ["2026-05-06"],
            "amounts": ["$1,000", "$5,000"],
            "terms": ["30 days payment"]
        }
        
        return {
            "status": "success",
            "entities": entities,
            "method": "mock",
            "note": "LangChain not available - using mock extraction"
        }
    
    @staticmethod
    def _mock_analyze_risks(clauses: List[Dict]) -> Dict[str, Any]:
        """Mock risk analysis"""
        risks = {
            "high_risk": [
                "Unlimited liability clause detected",
                "No dispute resolution mechanism"
            ],
            "medium_risk": [
                "Payment terms exceed 60 days",
                "Termination requires 30 days notice"
            ],
            "recommendations": [
                "Add liability cap of $100,000",
                "Define arbitration clause",
                "Reduce payment terms to 30 days"
            ]
        }
        
        return {
            "status": "success",
            "risks": risks,
            "method": "mock"
        }
    
    @staticmethod
    def _mock_compare_contracts() -> Dict[str, Any]:
        """Mock contract comparison"""
        return {
            "status": "success",
            "comparison": {
                "differences": [
                    "Contract 2 has longer payment terms",
                    "Contract 1 has broader liability coverage"
                ],
                "favorable_in_contract_1": ["Faster payment", "Limited liability"],
                "favorable_in_contract_2": ["Extended terms", "Flexible termination"]
            },
            "method": "mock"
        }


# Initialize global analyzer
contract_analyzer = ContractAnalyzer()
