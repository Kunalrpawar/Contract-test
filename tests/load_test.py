"""
Performance and Load Testing Script
Uses Locust for load testing
"""

from locust import HttpUser, task, between
import random
import json


class ContractIQUser(HttpUser):
    """Simulates a user interacting with ContractIQ API"""
    
    wait_time = between(1, 5)
    
    def on_start(self):
        """Initialize user session"""
        # Check health on startup
        self.client.get("/api/v1/health")
        self.contract_ids = []
    
    @task(3)
    def upload_contract(self):
        """Task: Upload a contract"""
        # Create a dummy PDF content
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< >>
stream
BT
/F1 12 Tf
100 700 Td
(SLA 99.9% uptime) Tj
100 650 Td
(Payment Net 30) Tj
100 600 Td
(Termination 30 days notice) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000273 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
353
%%EOF
"""
        files = {"file": ("test_contract.pdf", pdf_content, "application/pdf")}
        response = self.client.post("/api/v1/contracts/upload", files=files)
        
        if response.status_code == 201:
            contract_id = response.json().get("id")
            if contract_id:
                self.contract_ids.append(contract_id)
    
    @task(2)
    def list_contracts(self):
        """Task: List contracts"""
        self.client.get("/api/v1/contracts/")
    
    @task(2)
    def get_contract(self):
        """Task: Get specific contract"""
        if self.contract_ids:
            contract_id = random.choice(self.contract_ids)
            self.client.get(f"/api/v1/contracts/{contract_id}")
    
    @task(1)
    def analyze_contract(self):
        """Task: Analyze a contract"""
        if self.contract_ids:
            contract_id = random.choice(self.contract_ids)
            self.client.post(f"/api/v1/analyze/{contract_id}")
    
    @task(1)
    def validate_contract(self):
        """Task: Validate a contract"""
        if self.contract_ids:
            contract_id = random.choice(self.contract_ids)
            self.client.post(f"/api/v1/validate/{contract_id}")
    
    @task(1)
    def health_check(self):
        """Task: Health check"""
        self.client.get("/api/v1/health")


# Run with: locust -f load_test.py --host=http://localhost:8000 -u 10 -r 2 -t 5m
