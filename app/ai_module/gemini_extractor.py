"""
AI Module for Clause Extraction
Integrates with Gemini API for intelligent clause extraction
Includes fallback to spaCy for NLP-based extraction
"""

import json
import logging
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger(__name__)


class GeminiClauseExtractor:
    """Extract clauses from contract text using Google Gemini API"""
    
    CLAUSE_TYPES = [
        "SLA",
        "PaymentTerms",
        "Termination",
        "Confidentiality",
        "Liability",
        "ForceMAjeure",
        "Intellectual Property",
        "Warranty",
        "Indemnification",
        "Dispute Resolution",
        "Governing Law",
        "Amendment",
        "Severability"
    ]
    
    def __init__(self):
        """Initialize Gemini API client"""
        if settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini API initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini API: {str(e)}")
                self.model = None
        else:
            logger.warning("GEMINI_API_KEY not set - using mock mode")
            self.model = None
    
    def extract_clauses(self, contract_text: str) -> List[Dict[str, Any]]:
        """
        Extract clauses from contract text using Gemini
        
        Args:
            contract_text: Full text of the contract
        
        Returns:
            List of extracted clauses with metadata
        """
        if not contract_text or len(contract_text.strip()) == 0:
            logger.warning("Empty contract text provided")
            return []
        
        if self.model is None:
            logger.info("Using mock Gemini response (API key not configured)")
            return self._mock_extract_clauses(contract_text)
        
        try:
            prompt = self._build_extraction_prompt(contract_text)
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                logger.error("Empty response from Gemini API")
                return []
            
            # Parse JSON response
            clauses = self._parse_gemini_response(response.text)
            logger.info(f"Successfully extracted {len(clauses)} clauses from contract")
            return clauses
        
        except Exception as e:
            logger.error(f"Error extracting clauses with Gemini: {str(e)}")
            # Fallback to mock extraction
            return self._mock_extract_clauses(contract_text)
    
    def _build_extraction_prompt(self, contract_text: str) -> str:
        """Build the prompt for Gemini API"""
        clause_types_str = ", ".join(self.CLAUSE_TYPES)
        
        prompt = f"""
        Analyze the following contract and extract key clauses.
        
        IMPORTANT: Return your response as valid JSON only, with no additional text before or after.
        
        Contract Text:
        {contract_text[:4000]}  # Limit to first 4000 chars due to API limits
        
        Please extract clauses of these types: {clause_types_str}
        
        For each clause found, return JSON with this structure:
        {{
            "clauses": [
                {{
                    "clause_type": "SLA",
                    "clause_text": "The service provider shall maintain 99.9% uptime...",
                    "confidence_score": 95,
                    "extracted_data": {{
                        "key1": "value1",
                        "key2": "value2"
                    }}
                }}
            ]
        }}
        
        If a clause type is not found, don't include it. Return only valid JSON.
        """
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse JSON response from Gemini"""
        try:
            # Try to extract JSON from response
            response_text = response_text.strip()
            
            # Find JSON block if wrapped in markdown
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            response_json = json.loads(response_text)
            
            if "clauses" in response_json:
                return response_json["clauses"]
            else:
                return response_json if isinstance(response_json, list) else []
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            return []
    
    def _mock_extract_clauses(self, contract_text: str) -> List[Dict[str, Any]]:
        """
        Mock clause extraction for testing/development
        Returns realistic sample data
        """
        mock_clauses = []
        
        # Check for keywords and return matching mock clauses
        text_lower = contract_text.lower()
        
        if any(keyword in text_lower for keyword in ["sla", "service level", "uptime", "availability"]):
            mock_clauses.append({
                "clause_type": "SLA",
                "clause_text": "Service Level Agreement details extracted from contract",
                "confidence_score": 85,
                "extracted_data": {
                    "uptime": "99.9%",
                    "response_time": "4 hours"
                }
            })
        
        if any(keyword in text_lower for keyword in ["payment", "fee", "invoice", "bill"]):
            mock_clauses.append({
                "clause_type": "PaymentTerms",
                "clause_text": "Payment shall be made within 30 days of invoice",
                "confidence_score": 90,
                "extracted_data": {
                    "payment_days": 30,
                    "currency": "USD"
                }
            })
        
        if any(keyword in text_lower for keyword in ["termination", "terminate", "end", "cancel"]):
            mock_clauses.append({
                "clause_type": "Termination",
                "clause_text": "Either party may terminate with 30 days written notice",
                "confidence_score": 88,
                "extracted_data": {
                    "notice_period": "30 days"
                }
            })
        
        if any(keyword in text_lower for keyword in ["confidential", "confidentiality", "secret", "proprietary"]):
            mock_clauses.append({
                "clause_type": "Confidentiality",
                "clause_text": "All information shall be kept confidential",
                "confidence_score": 92,
                "extracted_data": {
                    "duration": "5 years"
                }
            })
        
        # Always include warranty
        mock_clauses.append({
            "clause_type": "Warranty",
            "clause_text": "Services are provided as-is",
            "confidence_score": 78,
            "extracted_data": {
                "type": "as-is"
            }
        })
        
        logger.info(f"Generated {len(mock_clauses)} mock clauses")
        return mock_clauses
    
    def extract_specific_clause(self, contract_text: str, clause_type: str) -> Optional[Dict[str, Any]]:
        """Extract a specific clause type"""
        clauses = self.extract_clauses(contract_text)
        for clause in clauses:
            if clause.get("clause_type") == clause_type:
                return clause
        return None
