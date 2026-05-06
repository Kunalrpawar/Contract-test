# ContractIQ Testing Guide - SDET Focus

## Overview

This guide covers comprehensive testing strategies for the ContractIQ platform, with emphasis on test automation (SDET) best practices.

---

## Test Pyramid

```
          /\
         /  \
        /E2E \          (3-5% - End-to-end tests)
       /______\
         /  \
        /  UI \        (10-15% - UI automation tests)
       /______\
         /  \
        / API  \       (20-30% - API integration tests)
       /______\
         /  \
        / Unit \       (50-70% - Unit tests)
       /______\
```

---

## 1. Unit Tests

### Location
`tests/test_document_processor.py`, `tests/test_validation_rules.py`

### Coverage
- Document processor functions
- Validation rules logic
- Service layer business logic

### Running Unit Tests

```bash
# Run all unit tests
pytest tests/test_document_processor.py tests/test_validation_rules.py -v

# Run with coverage
pytest tests/test_document_processor.py --cov=app.services --cov-report=html

# Run specific test
pytest tests/test_document_processor.py::TestDocumentProcessor::test_extract_text_from_pdf -v

# Run with markers
pytest -m "not load_test" -v
```

### Example Unit Test

```python
def test_validate_file_success(self, sample_pdf_file):
    """Test file validation passes for valid file"""
    is_valid, error_msg = DocumentProcessor.validate_file(sample_pdf_file, "pdf")
    assert is_valid is True
    assert error_msg == ""
```

### SDET Checklist for Unit Tests

- [ ] Test happy path scenarios
- [ ] Test error conditions
- [ ] Test boundary conditions
- [ ] Mock external dependencies
- [ ] Use fixtures for test data
- [ ] Verify state changes
- [ ] Clean up after tests
- [ ] Assert specific error messages

---

## 2. Integration Tests (API Tests)

### Location
`tests/test_api.py`

### Coverage
- Upload endpoint
- Analysis endpoint
- Validation endpoint
- Comparison endpoint
- Database interactions
- Full workflows

### Running Integration Tests

```bash
# Run all API tests
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_api.py::TestContractUploadAPI -v

# Run with detailed output
pytest tests/test_api.py -vv -s

# Run and show failed test info
pytest tests/test_api.py --tb=short
```

### Example Integration Test

```python
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
    assert data["text_extracted"] is True
```

### SDET Checklist for Integration Tests

- [ ] Test complete workflows
- [ ] Verify database state
- [ ] Test error scenarios
- [ ] Validate response structure
- [ ] Check status codes
- [ ] Test pagination
- [ ] Verify data persistence
- [ ] Test with various data types
- [ ] Check concurrent requests

---

## 3. End-to-End Tests (Playwright)

### Location
`playwright_tests/test_ui_workflows.py`

### Coverage
- User workflows
- UI interactions
- Navigation
- Form submissions

### Running Playwright Tests

```bash
# Install browsers
playwright install

# Run all Playwright tests
pytest playwright_tests/ -v

# Run specific test
pytest playwright_tests/test_ui_workflows.py::TestContractUploadWorkflow::test_upload_page_load -v

# Run in headed mode (see browser)
pytest playwright_tests/ -v --headed

# Generate report
pytest playwright_tests/ --html=report.html --self-contained-html
```

### Example Playwright Test

```python
def test_upload_page_load(self, page: Page):
    """Test that upload page loads"""
    page.goto("http://localhost:8000/docs")
    expect(page).to_have_title(/Swagger UI|Documentation/)
    page.close()
```

### SDET Checklist for E2E Tests

- [ ] Test critical user paths
- [ ] Wait for dynamic content
- [ ] Use explicit waits, not implicit
- [ ] Verify multiple elements
- [ ] Test error scenarios
- [ ] Test on different browsers
- [ ] Take screenshots on failure
- [ ] Use Page Object Model for maintenance
- [ ] Test accessibility

---

## 4. Performance Tests

### Location
`tests/load_test.py`

### Coverage
- API throughput
- Response times
- Concurrent users
- Resource usage

### Running Performance Tests

```bash
# Install Locust
pip install locust

# Run with CLI
locust -f tests/load_test.py --host=http://localhost:8000 -u 50 -r 10 -t 5m

# Run headless
python -m locust -f tests/load_test.py --headless --users 100 --spawn-rate 10 --run-time 10m --host=http://localhost:8000

# Generate CSV reports
locust -f tests/load_test.py --headless -u 50 -r 5 -t 5m --csv=results --host=http://localhost:8000
```

### Performance Metrics to Monitor

```
- Response Time (< 500ms target)
- Throughput (requests/sec)
- Error Rate (target: 0%)
- 95th percentile response time
- CPU usage
- Memory usage
- Database connections
```

### SDET Checklist for Performance Tests

- [ ] Define performance baselines
- [ ] Test with realistic data volume
- [ ] Monitor resource usage
- [ ] Test error handling under load
- [ ] Verify no memory leaks
- [ ] Test database performance
- [ ] Generate reports
- [ ] Document results

---

## 5. Test Data Management

### Fixtures for Test Data

```python
@pytest.fixture(scope="function")
def sample_pdf_file():
    """Create a temporary PDF file for testing"""
    # ... create test file
    yield file_path
    # ... cleanup
```

### Database Fixtures

```python
@pytest.fixture
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
```

### Test Data Strategy

```
1. Use minimal data needed for test
2. Randomize data to prevent test interdependencies
3. Use factories for complex objects
4. Clean up after each test
5. Use in-memory database for speed
```

---

## 6. Test Coverage Analysis

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html --cov-report=term

# View report
open htmlcov/index.html

# Check specific module coverage
pytest tests/ --cov=app.services --cov-report=term-missing

# Fail if coverage below threshold
pytest tests/ --cov=app --cov-fail-under=80
```

### Current Coverage Target

```
- Overall: > 80%
- app/services: > 90%
- app/validators: > 90%
- app/ai_module: > 85%
- app/models: > 70%
```

---

## 7. CI/CD Integration

### GitHub Actions Workflow

The CI/CD pipeline automatically:

```yaml
1. Runs linting (flake8)
2. Runs unit tests
3. Runs integration tests
4. Generates coverage reports
5. Runs security scans
6. Builds Docker image
7. Generates documentation
```

### Local Testing Before Push

```bash
# Run full test suite
python run_tests.py

# Run specific test level
pytest tests/ -m "not load_test" -v

# Check coverage
pytest tests/ --cov=app --cov-report=term-missing

# Lint code
flake8 app/
```

---

## 8. Regression Testing

### Regression Test Suite

Test critical functionality after each change:

```bash
# Upload contracts
POST /api/v1/contracts/upload

# Analyze contracts
POST /api/v1/analyze/{id}

# Validate contracts
POST /api/v1/validate/{id}

# Compare contracts
POST /api/v1/compare/{id1}/{id2}

# Get contract details
GET /api/v1/contracts/{id}
```

### Automated Regression Tests

```python
class TestRegressionSuite:
    """Critical functionality regression tests"""
    
    def test_complete_workflow(self, client, sample_pdf_file):
        """Test complete contract processing workflow"""
        # Upload
        upload_response = client.post("/api/v1/contracts/upload", files=files)
        assert upload_response.status_code == 201
        contract_id = upload_response.json()['id']
        
        # Analyze
        analyze_response = client.post(f"/api/v1/analyze/{contract_id}")
        assert analyze_response.status_code == 200
        
        # Validate
        validate_response = client.post(f"/api/v1/validate/{contract_id}")
        assert validate_response.status_code == 200
```

---

## 9. Edge Cases and Error Testing

### Categories to Test

1. **File Upload Edge Cases**
   - Empty files
   - Corrupted files
   - Oversized files (> 50MB)
   - Invalid formats
   - Special characters in filenames

2. **Data Validation**
   - Missing required fields
   - Invalid data types
   - Null/empty values
   - Boundary values

3. **API Error Cases**
   - Non-existent resource (404)
   - Invalid request (400)
   - Server errors (500)
   - Timeout scenarios
   - Concurrent requests

### Example Edge Case Test

```python
def test_upload_oversized_file(self, client: TestClient):
    """Test upload of file exceeding size limit"""
    # Create a file > 50MB
    large_file = create_large_file(51_000_000)
    
    response = client.post(
        "/api/v1/contracts/upload",
        files={"file": large_file}
    )
    
    assert response.status_code == 413
    assert "exceeds maximum" in response.json()["detail"].lower()
```

---

## 10. Test Reporting

### Generate Reports

```bash
# HTML Report
pytest tests/ --html=report.html --self-contained-html

# JUnit XML (for CI/CD)
pytest tests/ --junit-xml=junit.xml

# Coverage Report
pytest tests/ --cov=app --cov-report=html

# Allure Report
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Report Location

```
- HTML Report: report.html
- Coverage: htmlcov/index.html
- JUnit XML: junit.xml
```

---

## 11. Best Practices

### ✅ DO

- Write tests before code (TDD)
- Keep tests isolated and independent
- Use meaningful test names
- Mock external dependencies
- Test one thing per test
- Use fixtures for setup/teardown
- Run tests frequently
- Keep tests fast (< 10ms for unit tests)
- Document complex test scenarios
- Review test coverage regularly

### ❌ DON'T

- Create test interdependencies
- Use hardcoded values
- Ignore test failures
- Test implementation details
- Create slow tests
- Skip error scenarios
- Use GUI testing for API testing
- Test third-party libraries
- Copy-paste test code
- Commit with failing tests

---

## 12. Debugging Tests

### Run with Debug Output

```bash
# Verbose output
pytest tests/ -vv -s

# Show print statements
pytest tests/ -s

# Stop on first failure
pytest tests/ -x

# Show last N lines of output
pytest tests/ --tb=line

# Full traceback
pytest tests/ --tb=long

# Post-mortem debugger
pytest tests/ --pdb
```

### Common Issues

```
Problem: "Database locked"
Solution: Clear database fixtures, check for missing rollbacks

Problem: "Fixture not found"
Solution: Check conftest.py is in correct directory

Problem: "Test times out"
Solution: Check for missing mocks, infinite loops, or blocking calls

Problem: "Random failures"
Solution: Check for test order dependencies, use --randomly-dont-shuffle
```

---

## 13. Test Execution Time

### Current Benchmarks

```
Unit Tests:          < 30 seconds
Integration Tests:   < 1 minute
API Tests:          < 2 minutes
Performance Tests:   5-10 minutes
Full Suite:          ~5-15 minutes
```

### Optimize Test Speed

```bash
# Run tests in parallel
pytest tests/ -n auto

# Run only failed tests
pytest tests/ --lf

# Run failed tests first, then others
pytest tests/ --ff

# Skip slowest tests
pytest tests/ -m "not slow"
```

---

## 14. Continuous Testing

### Pre-commit Testing

```bash
#!/bin/bash
# In .git/hooks/pre-commit

pytest tests/ -x || exit 1
flake8 app/ || exit 1
```

### Watch Mode

```bash
# Run tests on file changes
ptw -- -x

# Or use pytest-watch
pip install pytest-watch
```

---

## Resources

- [PyTest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [Locust Documentation](https://locust.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-events/)
- [SDET Best Practices](https://sdet.me/)

---

## Summary

| Test Type | Count | Coverage | Speed | Maintenance |
|-----------|-------|----------|-------|-------------|
| Unit | ~30 | High | Fast | Easy |
| Integration | ~15 | Medium | Medium | Medium |
| E2E | ~5 | Low | Slow | Hard |
| Performance | ~3 | - | Long | Medium |

**Total Tests: 50+** | **Total Coverage: >80%** | **Execution Time: ~5-15 min**
