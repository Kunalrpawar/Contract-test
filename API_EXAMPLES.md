# API Examples and Usage Guide

## Quick API Test Examples

### Using cURL

#### 1. Upload a Contract

```bash
# Upload a PDF contract
curl -X POST "http://localhost:8000/api/v1/contracts/upload" \
  -H "accept: application/json" \
  -F "file=@contract.pdf"

# Response:
# {
#   "id": 1,
#   "name": "contract.pdf",
#   "file_type": "pdf",
#   "file_size": 45678,
#   "text_extracted": true,
#   "clauses_extracted": false,
#   "validated": false,
#   "uploaded_at": "2024-01-15T10:30:00"
# }
```

#### 2. List All Contracts

```bash
curl -X GET "http://localhost:8000/api/v1/contracts/?skip=0&limit=10" \
  -H "accept: application/json"
```

#### 3. Get Specific Contract

```bash
curl -X GET "http://localhost:8000/api/v1/contracts/1" \
  -H "accept: application/json"
```

#### 4. Analyze Contract (Extract Clauses)

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/1" \
  -H "accept: application/json"

# Response:
# {
#   "contract_id": 1,
#   "status": "success",
#   "clauses": [
#     {
#       "id": 1,
#       "contract_id": 1,
#       "clause_type": "SLA",
#       "clause_text": "Service Level Agreement text...",
#       "confidence_score": 95,
#       "extracted_data": {
#         "uptime": "99.9%",
#         "response_time": "4 hours"
#       },
#       "source": "gemini_api",
#       "extracted_at": "2024-01-15T10:35:00"
#     }
#   ]
# }
```

#### 5. Validate Contract

```bash
curl -X POST "http://localhost:8000/api/v1/validate/1" \
  -H "accept: application/json"

# Response:
# {
#   "contract_id": 1,
#   "status": "success",
#   "results": [
#     {
#       "id": 1,
#       "contract_id": 1,
#       "rule_name": "Missing SLA",
#       "rule_description": "Contract must contain Service Level Agreement clause",
#       "severity": "ERROR",
#       "is_passed": true,
#       "message": "SLA clause found",
#       "validated_at": "2024-01-15T10:40:00"
#     },
#     {
#       "rule_name": "Payment Terms Exceeds 60 Days",
#       "severity": "WARNING",
#       "is_passed": false,
#       "message": "Payment terms (90 days) exceed 60-day threshold"
#     }
#   ],
#   "summary": {
#     "errors": 0,
#     "warnings": 1,
#     "info": 0,
#     "total": 8,
#     "passed": 7
#   }
# }
```

#### 6. Compare Two Contracts

```bash
curl -X POST "http://localhost:8000/api/v1/compare/1/2" \
  -H "accept: application/json"

# Response:
# {
#   "contract_1_id": 1,
#   "contract_2_id": 2,
#   "differences": {
#     "missing_in_contract2": ["SLA"],
#     "missing_in_contract1": [],
#     "different": [
#       {
#         "clause_type": "PaymentTerms",
#         "text_1": "Net 30 days",
#         "text_2": "Net 60 days"
#       }
#     ]
#   },
#   "similarity_score": 85.5
# }
```

#### 7. Get Extracted Clauses

```bash
curl -X GET "http://localhost:8000/api/v1/analyze/1/clauses" \
  -H "accept: application/json"
```

#### 8. Get Specific Clause Type

```bash
curl -X GET "http://localhost:8000/api/v1/analyze/1/clauses/SLA" \
  -H "accept: application/json"
```

#### 9. Delete Contract

```bash
curl -X DELETE "http://localhost:8000/api/v1/contracts/1"
```

#### 10. Health Check

```bash
curl -X GET "http://localhost:8000/api/v1/health"

# Response:
# {
#   "status": "healthy",
#   "service": "ContractIQ",
#   "version": "1.0.0"
# }
```

---

## Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Upload contract
def upload_contract(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/contracts/upload', files=files)
    return response.json()

# Analyze contract
def analyze_contract(contract_id):
    response = requests.post(f'{BASE_URL}/analyze/{contract_id}')
    return response.json()

# Validate contract
def validate_contract(contract_id):
    response = requests.post(f'{BASE_URL}/validate/{contract_id}')
    return response.json()

# Compare contracts
def compare_contracts(id1, id2):
    response = requests.post(f'{BASE_URL}/compare/{id1}/{id2}')
    return response.json()

# Example usage
if __name__ == "__main__":
    # Upload
    contract = upload_contract('contract.pdf')
    contract_id = contract['id']
    print(f"Uploaded: {contract_id}")
    
    # Analyze
    analysis = analyze_contract(contract_id)
    print(f"Found {len(analysis['clauses'])} clauses")
    
    # Validate
    validation = validate_contract(contract_id)
    print(f"Validation: {validation['summary']}")
```

---

## Using JavaScript/Fetch API

```javascript
const API_BASE = 'http://localhost:8000/api/v1';

// Upload contract
async function uploadContract(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE}/contracts/upload`, {
        method: 'POST',
        body: formData
    });
    return response.json();
}

// Analyze contract
async function analyzeContract(contractId) {
    const response = await fetch(`${API_BASE}/analyze/${contractId}`, {
        method: 'POST'
    });
    return response.json();
}

// Validate contract
async function validateContract(contractId) {
    const response = await fetch(`${API_BASE}/validate/${contractId}`, {
        method: 'POST'
    });
    return response.json();
}

// Example usage
document.getElementById('uploadBtn').addEventListener('click', async () => {
    const file = document.getElementById('fileInput').files[0];
    const contract = await uploadContract(file);
    console.log('Contract ID:', contract.id);
    
    // Analyze
    const analysis = await analyzeContract(contract.id);
    console.log('Clauses:', analysis.clauses);
    
    // Validate
    const validation = await validateContract(contract.id);
    console.log('Validation results:', validation.results);
});
```

---

## Batch Operations

### Process Multiple Contracts

```python
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

def process_contracts_directory(directory_path):
    """Process all PDF and DOCX files in a directory"""
    
    results = []
    pdf_files = Path(directory_path).glob('*.pdf')
    docx_files = Path(directory_path).glob('*.docx')
    
    for file_path in list(pdf_files) + list(docx_files):
        print(f"Processing: {file_path.name}")
        
        # Upload
        with open(file_path, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(f'{BASE_URL}/contracts/upload', files=files)
        
        if upload_response.status_code != 201:
            print(f"  ✗ Upload failed")
            continue
        
        contract_id = upload_response.json()['id']
        print(f"  ✓ Uploaded (ID: {contract_id})")
        
        # Analyze
        analyze_response = requests.post(f'{BASE_URL}/analyze/{contract_id}')
        clauses = analyze_response.json().get('clauses', [])
        print(f"  ✓ Analyzed ({len(clauses)} clauses extracted)")
        
        # Validate
        validate_response = requests.post(f'{BASE_URL}/validate/{contract_id}')
        validation = validate_response.json()
        summary = validation.get('summary', {})
        print(f"  ✓ Validated (Errors: {summary.get('errors', 0)}, Warnings: {summary.get('warnings', 0)})")
        
        results.append({
            'file': file_path.name,
            'contract_id': contract_id,
            'clauses': len(clauses),
            'validation_summary': summary
        })
    
    return results

# Usage
results = process_contracts_directory('./contracts')
for result in results:
    print(f"\n{result['file']}:")
    print(f"  Contract ID: {result['contract_id']}")
    print(f"  Clauses: {result['clauses']}")
    print(f"  Issues: {result['validation_summary']['errors']} errors, {result['validation_summary']['warnings']} warnings")
```

---

## Error Handling

### Common Status Codes

```
200 OK           - Successful request
201 Created      - Resource created (contract upload)
400 Bad Request  - Invalid input (unsupported file type, empty file)
404 Not Found    - Contract not found
413 Entity Too Large - File exceeds 50MB limit
500 Internal Server Error - Server error
```

### Error Response Example

```json
{
  "detail": "File type 'txt' not allowed. Allowed: ['pdf', 'docx']"
}
```

### Python Error Handling

```python
import requests

def safe_analyze(contract_id):
    try:
        response = requests.post(f'{BASE_URL}/analyze/{contract_id}')
        
        if response.status_code == 404:
            print(f"Contract {contract_id} not found")
            return None
        
        if response.status_code == 500:
            print("Server error - try again later")
            return None
        
        response.raise_for_status()  # Raise exception for other errors
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
```

---

## Performance Tips

1. **Batch Processing**: Group uploads and analyses to reduce API calls
2. **Caching**: Cache analysis results if contracts don't change frequently
3. **Pagination**: Use skip/limit parameters when listing contracts
4. **Async Operations**: For large files, consider async processing
5. **Compression**: Send large files with gzip compression

---

## Integration Examples

### Webhook Integration

```python
from fastapi import FastAPI
import requests

@app.post("/webhook/contracts")
async def webhook_handler(contract_data: dict):
    """Handle contract data from external system"""
    
    # Download contract
    response = requests.get(contract_data['file_url'])
    
    # Upload to ContractIQ
    files = {'file': ('contract.pdf', response.content)}
    upload_response = requests.post(f'{BASE_URL}/contracts/upload', files=files)
    
    # Analyze
    contract_id = upload_response.json()['id']
    analysis = requests.post(f'{BASE_URL}/analyze/{contract_id}').json()
    
    # Validate
    validation = requests.post(f'{BASE_URL}/validate/{contract_id}').json()
    
    # Send results to external system
    requests.post(contract_data['callback_url'], json={
        'contract_id': contract_id,
        'analysis': analysis,
        'validation': validation
    })
    
    return {'status': 'processed'}
```

---

## Troubleshooting

### File Upload Issues

```
# Problem: "File size exceeds maximum allowed size"
# Solution: File must be less than 50MB
# Workaround: Split large documents or increase MAX_UPLOAD_SIZE in .env

# Problem: "Unsupported file type"
# Solution: Only PDF and DOCX files are supported
# Workaround: Convert to supported format
```

### API Connection Issues

```
# Problem: Connection refused (localhost:8000)
# Solution: Ensure API is running
$ python -m uvicorn app.main:app --reload

# Or with Docker:
$ docker-compose up
```

### Analysis Not Working

```
# Problem: No clauses extracted
# Possible causes:
# 1. Document text couldn't be extracted
# 2. Gemini API key not set (using mock mode)
# 3. Document format not recognized

# Solution: Check logs
$ docker-compose logs api

# Enable debug mode in .env
LOG_LEVEL=DEBUG
```
