"""
Contract Upload Routes
Handles file upload and contract creation
"""

import os
import logging
from datetime import datetime
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import ContractService
from app.schemas import ContractResponse
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/contracts", tags=["contracts"])


@router.post("/upload", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a contract file (PDF or DOCX)
    
    - **file**: PDF or DOCX file to upload (max 50MB)
    
    Returns: ContractResponse with contract metadata
    """
    try:
        # Validate file type
        allowed_extensions = settings.allowed_extensions.split(",")
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type '{file_extension}' not allowed. Allowed: {allowed_extensions}"
            )
        
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.upload_directory, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(settings.upload_directory, filename)
        
        # Read and save file
        contents = await file.read()
        
        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )
        
        if len(contents) > settings.max_upload_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size: {settings.max_upload_size} bytes"
            )
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"File saved: {file_path}")
        
        # Create contract record in database
        contract = ContractService.upload_contract(
            db=db,
            file_name=file.filename,
            file_path=file_path,
            file_type=file_extension
        )
        
        logger.info(f"Contract created with ID: {contract.id}")
        
        return ContractResponse.model_validate(contract)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Get contract metadata by ID"""
    contract = ContractService.get_contract(db, contract_id)
    
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract not found: {contract_id}"
        )
    
    return ContractResponse.model_validate(contract)


@router.get("/", response_model=list[ContractResponse])
def list_contracts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all contracts with pagination"""
    contracts = ContractService.get_all_contracts(db, skip=skip, limit=limit)
    return [ContractResponse.model_validate(c) for c in contracts]


@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Delete a contract and associated file"""
    success = ContractService.delete_contract(db, contract_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract not found: {contract_id}"
        )
    
    return None
