"""
Document Processing Module
Handles extraction of text from PDF and DOCX files
"""

import os
import logging
from typing import Tuple
import PyPDF2
import pdfplumber
from docx import Document
from app.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process various document formats and extract text"""
    
    SUPPORTED_FORMATS = {"pdf", "docx"}
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF using pdfplumber for better accuracy
        Fallback to PyPDF2 if pdfplumber fails
        """
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            logger.info(f"Successfully extracted text from PDF: {file_path}")
            return text.strip()
        
        except Exception as e:
            logger.warning(f"pdfplumber failed, falling back to PyPDF2: {str(e)}")
            try:
                text = ""
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                
                logger.info(f"Successfully extracted text from PDF using PyPDF2: {file_path}")
                return text.strip()
            
            except Exception as e:
                logger.error(f"Failed to extract text from PDF: {str(e)}")
                raise Exception(f"PDF extraction failed: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"
            
            logger.info(f"Successfully extracted text from DOCX: {file_path}")
            return text.strip()
        
        except Exception as e:
            logger.error(f"Failed to extract text from DOCX: {str(e)}")
            raise Exception(f"DOCX extraction failed: {str(e)}")
    
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> str:
        """
        Extract text from document based on file type
        
        Args:
            file_path: Full path to the file
            file_type: File type (pdf or docx)
        
        Returns:
            Extracted text
        """
        file_type = file_type.lower()
        
        if file_type not in DocumentProcessor.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_type == "pdf":
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_type == "docx":
            return DocumentProcessor.extract_text_from_docx(file_path)
    
    @staticmethod
    def validate_file(file_path: str, file_type: str) -> Tuple[bool, str]:
        """
        Validate file before processing
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        file_type = file_type.lower()
        if file_type not in DocumentProcessor.SUPPORTED_FORMATS:
            return False, f"Unsupported file type: {file_type}"
        
        file_size = os.path.getsize(file_path)
        if file_size > settings.max_upload_size:
            return False, f"File size exceeds maximum allowed size: {settings.max_upload_size} bytes"
        
        if file_size == 0:
            return False, "File is empty"
        
        return True, ""
