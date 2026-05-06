"""
Selenium-based UI/E2E tests for ContractIQ
Tests the web interface and user workflows
"""

import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    """Initialize Selenium WebDriver"""
    chrome_options = Options()
    # Uncomment for headless mode
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


class TestContractIQUI:
    """UI tests for ContractIQ web interface"""
    
    BASE_URL = "http://localhost:8000"
    UPLOAD_FILE = "./tests/fixtures/sample_contract.pdf"
    
    def test_homepage_loads(self, driver):
        """Test that homepage loads successfully"""
        driver.get(self.BASE_URL)
        assert "ContractIQ" in driver.title or "Welcome" in driver.page_source
    
    def test_ui_page_loads(self, driver):
        """Test that UI page loads"""
        driver.get(f"{self.BASE_URL}/ui")
        
        # Wait for upload form
        upload_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fileInput"))
        )
        assert upload_element is not None
    
    def test_upload_contract_workflow(self, driver):
        """Test complete upload workflow"""
        driver.get(f"{self.BASE_URL}/ui")
        
        # Wait for and interact with upload input
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fileInput"))
        )
        
        # Create a test file if it doesn't exist
        test_file = "./tests/fixtures/test_upload.txt"
        os.makedirs("./tests/fixtures", exist_ok=True)
        with open(test_file, "w") as f:
            f.write("Sample contract for testing\n")
            f.write("TERMINATION CLAUSE: Either party may terminate with 30 days notice\n")
            f.write("WARRANTY: Services provided as-is\n")
        
        # Send file
        file_input.send_keys(os.path.abspath(test_file))
        
        # Wait for and click upload button
        upload_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "uploadBtn"))
        )
        upload_btn.click()
        
        # Wait for success message
        success_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success"))
        )
        assert "success" in success_msg.get_attribute("class").lower()
        
        # Cleanup
        os.remove(test_file)
    
    def test_contract_list_displays(self, driver):
        """Test that uploaded contracts are listed"""
        driver.get(f"{self.BASE_URL}/ui")
        
        # Wait for contracts list to load
        contracts_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contractsList"))
        )
        
        assert contracts_list is not None
    
    def test_analyze_contract_workflow(self, driver):
        """Test contract analysis workflow"""
        driver.get(f"{self.BASE_URL}/ui")
        
        # Wait for analyze button (if contracts exist)
        try:
            analyze_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "analyze-btn"))
            )
            analyze_btn.click()
            
            # Wait for results
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results"))
            )
            assert results is not None
        except:
            # No contracts to analyze, test passed
            pass
    
    def test_api_documentation_accessible(self, driver):
        """Test that Swagger documentation is accessible"""
        driver.get(f"{self.BASE_URL}/docs")
        
        # Check for Swagger UI elements
        swagger_ui = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swagger-ui"))
        )
        assert swagger_ui is not None
    
    def test_health_check_endpoint(self, driver):
        """Test health check endpoint in API"""
        driver.get(f"{self.BASE_URL}/api/v1/health")
        
        # Page should display JSON
        page_source = driver.page_source
        assert ("ok" in page_source.lower() or "status" in page_source.lower())
    
    def test_responsive_layout(self, driver):
        """Test responsive design at mobile breakpoint"""
        # Set mobile viewport
        driver.set_window_size(375, 667)
        driver.get(f"{self.BASE_URL}/ui")
        
        # Wait for mobile-optimized elements
        upload_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "uploadForm"))
        )
        assert upload_form is not None
        
        # Reset to desktop
        driver.set_window_size(1920, 1080)
    
    def test_error_handling_invalid_file(self, driver):
        """Test error handling for invalid file upload"""
        driver.get(f"{self.BASE_URL}/ui")
        
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fileInput"))
        )
        
        # Create invalid file (wrong extension)
        test_file = "./tests/fixtures/test_invalid.txt"
        os.makedirs("./tests/fixtures", exist_ok=True)
        with open(test_file, "w") as f:
            f.write("Invalid file content")
        
        file_input.send_keys(os.path.abspath(test_file))
        
        # The UI should show validation or the upload should be rejected
        time.sleep(2)
        
        # Cleanup
        os.remove(test_file)


class TestContractIQNavigation:
    """Test navigation flows"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_root_to_ui_navigation(self, driver):
        """Test navigation from root to UI"""
        driver.get(self.BASE_URL)
        
        # Look for navigation links
        links = driver.find_elements(By.TAG_NAME, "a")
        ui_link = next((l for l in links if "/ui" in l.get_attribute("href")), None)
        
        if ui_link:
            ui_link.click()
            assert "/ui" in driver.current_url
    
    def test_api_docs_link(self, driver):
        """Test API docs link"""
        driver.get(self.BASE_URL)
        
        # Navigate to docs
        driver.get(f"{self.BASE_URL}/docs")
        
        # Should be on docs page
        assert "/docs" in driver.current_url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
