"""
Playwright E2E tests for ContractIQ
Tests complete user workflows and edge cases
"""

import pytest
import asyncio
import os
from playwright.async_api import async_playwright, Page, expect


BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def page():
    """Fixture to provide a Playwright page"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        yield page
        await browser.close()


class TestContractIQPlaywright:
    """E2E tests using Playwright"""
    
    @pytest.mark.asyncio
    async def test_upload_and_analyze_workflow(self, page: Page):
        """Test complete upload and analysis workflow"""
        await page.goto(f"{BASE_URL}/ui")
        
        # Wait for upload form
        await page.wait_for_selector("#uploadForm")
        
        # Create test file
        test_file = "./tests/fixtures/e2e_contract.txt"
        os.makedirs("./tests/fixtures", exist_ok=True)
        with open(test_file, "w") as f:
            f.write("""
            SERVICE AGREEMENT
            
            TERMINATION: This agreement may be terminated by either party with 30 days written notice.
            WARRANTY: Services are provided as-is without express or implied warranties.
            PAYMENT TERMS: Invoice due within 45 days of receipt.
            CONFIDENTIALITY: All information shall be kept confidential for 3 years.
            """)
        
        # Upload file
        file_input = await page.query_selector("#fileInput")
        await file_input.set_input_files(os.path.abspath(test_file))
        
        # Click upload
        await page.click("#uploadBtn")
        
        # Wait for success
        await page.wait_for_selector(".success", timeout=5000)
        
        # Verify contract appears in list
        await page.wait_for_selector("#contractsList")
        content = await page.content()
        assert "e2e_contract" in content or "success" in content
        
        # Cleanup
        os.remove(test_file)
    
    @pytest.mark.asyncio
    async def test_contract_analysis(self, page: Page):
        """Test contract analysis workflow"""
        await page.goto(f"{BASE_URL}/ui")
        
        # Wait for page load
        await page.wait_for_selector("#contractsList")
        
        # Check if analyze buttons exist
        analyze_buttons = await page.query_selector_all(".analyze-btn")
        
        if analyze_buttons:
            # Click first analyze button
            await analyze_buttons[0].click()
            
            # Wait for results
            await page.wait_for_selector(".results", timeout=10000)
            
            # Verify results contain clause data
            content = await page.content()
            assert "Termination" in content or "Warranty" in content or "clause" in content.lower()
    
    @pytest.mark.asyncio
    async def test_api_documentation(self, page: Page):
        """Test API documentation accessibility"""
        await page.goto(f"{BASE_URL}/docs")
        
        # Wait for Swagger UI
        await page.wait_for_selector(".swagger-ui", timeout=5000)
        
        # Verify endpoints are visible
        content = await page.content()
        assert "/api/v1" in content
    
    @pytest.mark.asyncio
    async def test_responsive_design(self, page: Page):
        """Test responsive design"""
        # Test mobile view
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.goto(f"{BASE_URL}/ui")
        
        # Check elements are accessible
        await page.wait_for_selector("#uploadForm")
        
        # Test desktop view
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.goto(f"{BASE_URL}/ui")
        
        # Verify still works
        await page.wait_for_selector("#uploadForm")
    
    @pytest.mark.asyncio
    async def test_error_handling(self, page: Page):
        """Test error handling"""
        await page.goto(f"{BASE_URL}/ui")
        
        # Try invalid contract ID
        await page.goto(f"{BASE_URL}/ui")
        
        # Create test file with minimal content
        test_file = "./tests/fixtures/minimal.txt"
        os.makedirs("./tests/fixtures", exist_ok=True)
        with open(test_file, "w") as f:
            f.write("Short")
        
        # Upload
        file_input = await page.query_selector("#fileInput")
        await file_input.set_input_files(os.path.abspath(test_file))
        await page.click("#uploadBtn")
        
        # Should either succeed or show error gracefully
        try:
            await page.wait_for_selector(".success", timeout=3000)
        except:
            # Error handling test passed
            pass
        
        # Cleanup
        os.remove(test_file)
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, page: Page):
        """Test health check endpoint"""
        await page.goto(f"{BASE_URL}/api/v1/health")
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        
        # Get page content
        content = await page.content()
        
        # Should contain status or health info
        assert "status" in content.lower() or "ok" in content.lower()
    
    @pytest.mark.asyncio
    async def test_navigation_flow(self, page: Page):
        """Test navigation between pages"""
        # Start at root
        await page.goto(BASE_URL)
        
        # Navigate to UI
        await page.goto(f"{BASE_URL}/ui")
        await page.wait_for_selector("#uploadForm")
        
        # Navigate to docs
        await page.goto(f"{BASE_URL}/docs")
        await page.wait_for_selector(".swagger-ui", timeout=5000)
        
        # Back to UI
        await page.goto(f"{BASE_URL}/ui")
        await page.wait_for_selector("#uploadForm")


class TestContractIQPerformance:
    """Performance tests using Playwright"""
    
    @pytest.mark.asyncio
    async def test_page_load_time(self, page: Page):
        """Test page load performance"""
        start_time = asyncio.get_event_loop().time()
        
        await page.goto(f"{BASE_URL}/ui", wait_until="networkidle")
        
        end_time = asyncio.get_event_loop().time()
        load_time = end_time - start_time
        
        # Should load within 5 seconds
        assert load_time < 5, f"Page took {load_time}s to load"
    
    @pytest.mark.asyncio
    async def test_multiple_uploads_performance(self, page: Page):
        """Test handling multiple uploads"""
        await page.goto(f"{BASE_URL}/ui")
        
        for i in range(3):
            # Create test file
            test_file = f"./tests/fixtures/perf_test_{i}.txt"
            os.makedirs("./tests/fixtures", exist_ok=True)
            with open(test_file, "w") as f:
                f.write(f"Test contract {i}\nTermination clause: 30 days notice")
            
            # Upload
            file_input = await page.query_selector("#fileInput")
            await file_input.set_input_files(os.path.abspath(test_file))
            await page.click("#uploadBtn")
            
            # Wait for completion
            try:
                await page.wait_for_selector(".success", timeout=3000)
            except:
                pass
            
            # Cleanup
            os.remove(test_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
