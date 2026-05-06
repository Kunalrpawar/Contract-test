"""
Unit Tests for Document Processor
"""

import pytest
import os
import tempfile
from app.services import DocumentProcessor


class TestDocumentProcessor:
    """Test document processing functionality"""
    
    def test_extract_text_from_pdf(self, sample_pdf_file):
        """Test extracting text from valid PDF"""
        text = DocumentProcessor.extract_text(sample_pdf_file, "pdf")
        assert text is not None
        assert isinstance(text, str)
        assert len(text) > 0
    
    def test_extract_text_from_docx(self, sample_docx_file):
        """Test extracting text from valid DOCX"""
        text = DocumentProcessor.extract_text(sample_docx_file, "docx")
        assert text is not None
        assert "SLA" in text or "Payment" in text or "Termination" in text
    
    def test_extract_text_invalid_file_type(self, sample_pdf_file):
        """Test error handling for unsupported file type"""
        with pytest.raises(ValueError, match="Unsupported file type"):
            DocumentProcessor.extract_text(sample_pdf_file, "txt")
    
    def test_extract_text_file_not_found(self):
        """Test error handling for non-existent file"""
        with pytest.raises(FileNotFoundError):
            DocumentProcessor.extract_text("/nonexistent/file.pdf", "pdf")
    
    def test_validate_file_success(self, sample_pdf_file):
        """Test file validation passes for valid file"""
        is_valid, error_msg = DocumentProcessor.validate_file(sample_pdf_file, "pdf")
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_file_not_exists(self):
        """Test file validation fails for non-existent file"""
        is_valid, error_msg = DocumentProcessor.validate_file("/nonexistent/file.pdf", "pdf")
        assert is_valid is False
        assert "does not exist" in error_msg
    
    def test_validate_file_empty(self, empty_pdf_file):
        """Test file validation fails for empty file"""
        is_valid, error_msg = DocumentProcessor.validate_file(empty_pdf_file, "pdf")
        assert is_valid is False
        assert "empty" in error_msg.lower()
    
    def test_validate_file_unsupported_type(self, sample_pdf_file):
        """Test file validation fails for unsupported type"""
        is_valid, error_msg = DocumentProcessor.validate_file(sample_pdf_file, "txt")
        assert is_valid is False
        assert "Unsupported" in error_msg
