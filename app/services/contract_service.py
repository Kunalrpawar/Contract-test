"""
Contract Service - Business logic for contract operations
"""

import os
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Contract, ClauseExtraction, ValidationResult
from app.services.document_processor import DocumentProcessor
from app.config import settings

logger = logging.getLogger(__name__)


class ContractService:
    """Service for managing contracts"""
    
    @staticmethod
    def upload_contract(db: Session, file_name: str, file_path: str, file_type: str) -> Contract:
        """
        Upload and store contract in database
        
        Args:
            db: Database session
            file_name: Original file name
            file_path: Full path where file is stored
            file_type: File type (pdf or docx)
        
        Returns:
            Contract object
        """
        try:
            # Validate file
            is_valid, error_msg = DocumentProcessor.validate_file(file_path, file_type)
            if not is_valid:
                raise ValueError(error_msg)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create contract record
            contract = Contract(
                name=file_name,
                file_path=file_path,
                file_type=file_type.lower(),
                file_size=file_size
            )
            
            # Extract text immediately
            try:
                raw_text = DocumentProcessor.extract_text(file_path, file_type)
                contract.raw_text = raw_text
                contract.text_extracted = True
                logger.info(f"Text extracted for contract: {file_name}")
            except Exception as e:
                logger.error(f"Failed to extract text during upload: {str(e)}")
                contract.text_extracted = False
            
            db.add(contract)
            db.commit()
            db.refresh(contract)
            
            logger.info(f"Contract uploaded successfully: {contract.id}")
            return contract
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to upload contract: {str(e)}")
            raise
    
    @staticmethod
    def get_contract(db: Session, contract_id: int) -> Optional[Contract]:
        """Get contract by ID"""
        return db.query(Contract).filter(Contract.id == contract_id).first()
    
    @staticmethod
    def get_all_contracts(db: Session, skip: int = 0, limit: int = 100) -> List[Contract]:
        """Get all contracts with pagination"""
        return db.query(Contract).offset(skip).limit(limit).all()
    
    @staticmethod
    def delete_contract(db: Session, contract_id: int) -> bool:
        """
        Delete contract and its associated file
        
        Returns:
            True if deleted successfully
        """
        try:
            contract = ContractService.get_contract(db, contract_id)
            if not contract:
                return False
            
            # Delete file from storage
            if os.path.exists(contract.file_path):
                os.remove(contract.file_path)
                logger.info(f"File deleted: {contract.file_path}")
            
            # Delete from database (cascades to related records)
            db.delete(contract)
            db.commit()
            
            logger.info(f"Contract deleted: {contract_id}")
            return True
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete contract: {str(e)}")
            raise
    
    @staticmethod
    def get_contract_text(db: Session, contract_id: int) -> Optional[str]:
        """Get raw text of a contract"""
        contract = ContractService.get_contract(db, contract_id)
        if contract:
            return contract.raw_text
        return None
