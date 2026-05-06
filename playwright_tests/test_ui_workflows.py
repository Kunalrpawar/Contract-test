"""
Playwright UI Automation Tests for ContractIQ
Test upload, analysis, and validation workflows
"""

import pytest
import tempfile
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, expect


class TestContractUploadWorkflow:
    """UI tests for contract upload workflow"""
    
    @pytest.fixture
    def browser_context(self):
        """Create Playwright browser context"""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            yield context
            browser.close()
    
    @pytest.fixture
    def page(self, browser_context):
        """Create a page"""
        return browser_context.new_page()
    
    def test_upload_page_load(self, page: Page):
        """Test that upload page loads"""
        page.goto("http://localhost:8000/docs")
        # Check for Swagger UI
        expect(page).to_have_title(/Swagger UI|Documentation/)
        page.close()
    
    def test_api_documentation_accessible(self, page: Page):
        """Test API documentation is accessible"""
        page.goto("http://localhost:8000/docs")
        # Look for API endpoints
        content = page.content()
        assert "/api/v1/contracts/upload" in content or "upload" in content.lower()
        page.close()


class TestContractAnalysisWorkflow:
    """UI tests for contract analysis workflow"""
    
    def test_analysis_endpoint_in_docs(self):
        """Test analysis endpoint is documented"""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            page.goto("http://localhost:8000/docs")
            content = page.content()
            assert "analyze" in content.lower()
            
            browser.close()


class TestReturnsToHome:
    """Basic navigation tests"""
    
    def test_home_endpoint(self):
        """Test home endpoint returns welcome message"""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            page.goto("http://localhost:8000/")
            content = page.content()
            assert "welcome" in content.lower() or "contractiq" in content.lower()
            
            browser.close()
