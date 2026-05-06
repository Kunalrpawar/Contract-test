# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Using Docker (Recommended)

```bash
# 1. Clone and navigate
git clone <repo-url>
cd contract-test

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
docker-compose up

# 4. In another terminal, initialize database
docker exec contractiq-api python init_db.py

# 5. Access the platform
# API:     http://localhost:8000
# Docs:    http://localhost:8000/docs
# UI:      http://localhost:8000/ui
# pgAdmin: http://localhost:5050
```

### Option 2: Local Development

```bash
# 1. Prerequisites
# - Python 3.11+
# - PostgreSQL 15+

# 2. Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database
createdb contractiq_db -U contractiq

# 5. Initialize database
python init_db.py

# 6. Run application
python -m uvicorn app.main:app --reload

# 7. Access
# API:  http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 📝 First Steps

### 1. Upload a Contract

**Using Web UI:**
1. Open http://localhost:8000/ui
2. Click "Upload Contract"
3. Select a PDF or DOCX file
4. Click "Upload Contract"

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/upload" \
  -F "file=@contract.pdf"
```

**Using Python:**
```python
import requests

with open('contract.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/v1/contracts/upload',
        files=files
    )
contract_id = response.json()['id']
print(f"Contract ID: {contract_id}")
```

### 2. Analyze Contract

**Using Web UI:**
1. Enter the Contract ID from step 1
2. Click "Analyze"
3. View extracted clauses

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze/{contract_id}"
```

**Using Python:**
```python
response = requests.post(
    f'http://localhost:8000/api/v1/analyze/{contract_id}'
)
clauses = response.json()['clauses']
for clause in clauses:
    print(f"{clause['clause_type']}: {clause['confidence_score']}%")
```

### 3. Validate Contract

**Using Web UI:**
1. Enter the Contract ID
2. Click "Validate"
3. Review validation results

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/validate/{contract_id}"
```

**Using Python:**
```python
response = requests.post(
    f'http://localhost:8000/api/v1/validate/{contract_id}'
)
results = response.json()
print(f"Errors: {results['summary']['errors']}")
print(f"Warnings: {results['summary']['warnings']}")
```

---

## 🧪 Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run load test
locust -f tests/load_test.py --host=http://localhost:8000 -u 10

# Run UI tests
pytest playwright_tests/ -v
```

---

## 📊 Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Web UI | http://localhost:8000/ui | - |
| Database | localhost:5432 | contractiq/contractiq |
| pgAdmin | http://localhost:5050 | admin@contractiq.local/admin |

---

## 🔧 Common Commands

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f api

# Access database
docker exec -it contractiq-db psql -U contractiq -d contractiq_db

# Rebuild containers
docker-compose build --no-cache

# Delete all data
docker-compose down -v

# Run migrations
docker exec contractiq-api python init_db.py

# Check health
curl http://localhost:8000/api/v1/health
```

---

## 📚 Documentation

- **README.md** - Project overview and features
- **API_EXAMPLES.md** - API usage examples
- **TESTING_GUIDE.md** - Comprehensive testing guide
- **docker/README.md** - Docker deployment info
- **API Docs** - http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change port in docker-compose.yml
# Or kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose logs db

# Recreate database
docker-compose down -v
docker-compose up
docker exec contractiq-api python init_db.py
```

### Tests Failing

```bash
# Run with verbose output
pytest tests/ -v -s

# Check logs
docker-compose logs api

# Ensure database is initialized
docker exec contractiq-api python init_db.py
```

### API Not Responding

```bash
# Check if service is running
docker-compose ps

# View logs
docker-compose logs api

# Restart service
docker-compose restart api
```

---

## 🎯 Next Steps

1. **Explore API Documentation** - Visit http://localhost:8000/docs
2. **Run Sample Tests** - `pytest tests/test_api.py -v`
3. **Upload Sample Contract** - Use the web UI at http://localhost:8000/ui
4. **Review Code** - Check `app/` directory for implementation
5. **Customize Validation Rules** - Edit `app/validators/rules_engine.py`
6. **Add Gemini API Key** - Set `GEMINI_API_KEY` in `.env`

---

## 💡 Quick Tips

- **Web UI**: Simple interface for testing without API knowledge
- **API Docs**: Interactive documentation with try-it-out feature
- **pgAdmin**: Visual database management tool
- **Logs**: Check container logs for debugging (`docker-compose logs`)
- **Test Coverage**: Run `pytest tests/ --cov=app` for coverage report

---

## 📞 Support

For detailed information, refer to:
- README.md - Full documentation
- TESTING_GUIDE.md - Testing strategies
- API_EXAMPLES.md - API usage patterns

---

**Happy Contract Analysis! 🎉**
