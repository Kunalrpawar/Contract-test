"""
API Integration Tests
Tests for all REST API endpoints
"""

import pytest
import os
import tempfile
from io import BytesIO
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestContractUploadAPI:
    """Test contract upload endpoints"""
    
    def test_upload_pdf_success(self, client: TestClient, sample_pdf_file):
        """Test successful PDF upload"""
        with open(sample_pdf_file, "rb") as f:
            response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test_contract.pdf", f, "application/pdf")}
            )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test_contract.pdf"
        assert data["file_type"] == "pdf"
        assert data["text_extracted"] is True
        assert "id" in data
    
    def test_upload_docx_success(self, client: TestClient, sample_docx_file):
        """Test successful DOCX upload"""
        with open(sample_docx_file, "rb") as f:
            response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test_contract.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test_contract.docx"
        assert data["file_type"] == "docx"
    
    def test_upload_empty_file(self, client: TestClient, empty_pdf_file):
        """Test upload of empty file fails"""
        with open(empty_pdf_file, "rb") as f:
            response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("empty.pdf", f, "application/pdf")}
            )
        
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_upload_invalid_extension(self, client: TestClient, sample_pdf_file):
        """Test upload with invalid file extension fails"""
        with open(sample_pdf_file, "rb") as f:
            response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"].lower()
    
    def test_get_contract(self, client: TestClient, sample_pdf_file):
        """Test getting contract by ID"""
        # Upload first
        with open(sample_pdf_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.pdf", f, "application/pdf")}
            )
        
        contract_id = upload_response.json()["id"]
        
        # Get contract
        response = client.get(f"/api/v1/contracts/{contract_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == contract_id
        assert data["name"] == "test.pdf"
    
    def test_get_nonexistent_contract(self, client: TestClient):
        """Test getting non-existent contract"""
        response = client.get("/api/v1/contracts/99999")
        assert response.status_code == 404
    
    def test_list_contracts(self, client: TestClient, sample_pdf_file):
        """Test listing contracts"""
        # Upload a contract
        with open(sample_pdf_file, "rb") as f:
            client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.pdf", f, "application/pdf")}
            )
        
        # List contracts
        response = client.get("/api/v1/contracts/")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_delete_contract(self, client: TestClient, sample_pdf_file):
        """Test deleting contract"""
        # Upload
        with open(sample_pdf_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.pdf", f, "application/pdf")}
            )
        
        contract_id = upload_response.json()["id"]
        
        # Delete
        response = client.delete(f"/api/v1/contracts/{contract_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/api/v1/contracts/{contract_id}")
        assert response.status_code == 404


class TestAnalysisAPI:
    """Test contract analysis endpoints"""
    
    def test_analyze_contract(self, client: TestClient, sample_docx_file):
        """Test contract analysis"""
        # Upload contract
        with open(sample_docx_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
        
        contract_id = upload_response.json()["id"]
        
        # Analyze contract
        response = client.post(f"/api/v1/analyze/{contract_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["contract_id"] == contract_id
        assert "clauses" in data
        assert len(data["clauses"]) > 0
    
    def test_analyze_nonexistent_contract(self, client: TestClient):
        """Test analyzing non-existent contract"""
        response = client.post("/api/v1/analyze/99999")
        assert response.status_code == 404
    
    def test_get_contract_clauses(self, client: TestClient, sample_docx_file):
        """Test getting extracted clauses"""
        # Upload and analyze
        with open(sample_docx_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
        
        contract_id = upload_response.json()["id"]
        client.post(f"/api/v1/analyze/{contract_id}")
        
        # Get clauses
        response = client.get(f"/api/v1/analyze/{contract_id}/clauses")
        assert response.status_code == 200
        clauses = response.json()
        assert len(clauses) > 0


class TestValidationAPI:
    """Test contract validation endpoints"""
    
    def test_validate_contract(self, client: TestClient, sample_docx_file):
        """Test contract validation"""
        # Upload and analyze
        with open(sample_docx_file, "rb") as f:
            upload_response = client.post(
                "/api/v1/contracts/upload",
                files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            )
        
        contract_id = upload_response.json()["id"]
        client.post(f"/api/v1/analyze/{contract_id}")
        
        # Validate contract
        response = client.post(f"/api/v1/validate/{contract_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["contract_id"] == contract_id
        assert "results" in data
        assert "summary" in data
        assert "errors" in data["summary"]
        assert "warnings" in data["summary"]


class TestHealthAPI:
    """Test health check endpoint"""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data


class TestComparisonAPI:
    """Test contract comparison endpoints"""
    
    def test_compare_contracts(self, client: TestClient, sample_docx_file):
        """Test comparing two contracts"""
        # Upload and analyze two contracts
        contracts = []
        for i in range(2):
            with open(sample_docx_file, "rb") as f:
                upload_response = client.post(
                    "/api/v1/contracts/upload",
                    files={"file": (f"test{i}.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
                )
            
            contract_id = upload_response.json()["id"]
            client.post(f"/api/v1/analyze/{contract_id}")
            contracts.append(contract_id)
        
        # Compare
        response = client.post(f"/api/v1/compare/{contracts[0]}/{contracts[1]}")
        assert response.status_code == 200
        data = response.json()
        assert data["contract_1_id"] == contracts[0]
        assert data["contract_2_id"] == contracts[1]
        assert "differences" in data
        assert "similarity_score" in data
