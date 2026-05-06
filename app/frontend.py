"""
Simple HTML Frontend for ContractIQ
Provides basic UI for upload and analysis
"""

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ContractIQ - Contract Analysis Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        input[type="file"],
        input[type="text"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input[type="file"]:focus,
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .button-group button {
            width: 100%;
        }
        
        .results {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .results h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .result-item {
            background: #f9f9f9;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            border-radius: 3px;
        }
        
        .result-item strong {
            color: #333;
            display: block;
            margin-bottom: 5px;
        }
        
        .result-item p {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 10px;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .status.warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .status.info {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: none;
        }
        
        .error-message.show {
            display: block;
        }
        
        .contracts-list {
            margin-top: 30px;
        }
        
        .contract-item {
            background: #f9f9f9;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .contract-info {
            flex: 1;
        }
        
        .contract-info strong {
            color: #333;
            display: block;
        }
        
        .contract-info small {
            color: #999;
            display: block;
            margin-top: 5px;
        }
        
        .contract-actions {
            display: flex;
            gap: 10px;
        }
        
        .contract-actions button {
            width: auto;
            padding: 8px 15px;
            font-size: 14px;
        }
        
        footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .button-group {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 ContractIQ</h1>
            <p class="subtitle">AI-Powered Contract Testing & Validation Platform</p>
        </header>
        
        <div class="main-content">
            <!-- Upload Section -->
            <div class="card">
                <h2>📄 Upload Contract</h2>
                <form id="uploadForm">
                    <div class="form-group">
                        <label for="contractFile">Select PDF or DOCX file</label>
                        <input type="file" id="contractFile" name="file" accept=".pdf,.docx" required>
                    </div>
                    <button type="submit">Upload Contract</button>
                </form>
            </div>
            
            <!-- Analysis Section -->
            <div class="card">
                <h2>🔍 Analyze Contract</h2>
                <form id="analysisForm">
                    <div class="form-group">
                        <label for="contractId">Contract ID</label>
                        <input type="text" id="contractId" name="contractId" placeholder="Enter contract ID" required>
                    </div>
                    <div class="button-group">
                        <button type="button" onclick="analyzeContract()">Analyze</button>
                        <button type="button" onclick="validateContract()">Validate</button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Contracts List -->
        <div class="card contracts-list" id="contractsList" style="display: none;">
            <h2>📋 Uploaded Contracts</h2>
            <div id="contractsContainer"></div>
        </div>
        
        <!-- Results Section -->
        <div class="card results" id="results">
            <h2>📊 Analysis Results</h2>
            <div class="error-message" id="errorMessage"></div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 10px; color: #666;">Processing...</p>
            </div>
            <div id="resultsContainer"></div>
        </div>
        
        <footer>
            <p>ContractIQ v1.0.0 | API Documentation: <a href="http://localhost:8000/docs" style="color: white; text-decoration: underline;">http://localhost:8000/docs</a></p>
        </footer>
    </div>
    
    <script>
        const API_BASE = 'http://localhost:8000/api/v1';
        
        // Upload contract
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('contractFile');
            const file = fileInput.files[0];
            
            if (!file) {
                showError('Please select a file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            showLoading();
            
            try {
                const response = await fetch(`${API_BASE}/contracts/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`Upload failed: ${response.statusText}`);
                }
                
                const contract = await response.json();
                showResults(`Contract uploaded successfully!`, {
                    id: contract.id,
                    name: contract.name,
                    type: contract.file_type,
                    size: `${(contract.file_size / 1024 / 1024).toFixed(2)} MB`,
                    status: contract.text_extracted ? 'Text Extracted ✓' : 'Pending text extraction'
                });
                
                document.getElementById('contractId').value = contract.id;
                fileInput.value = '';
                listContracts();
                
            } catch (error) {
                showError(`Error: ${error.message}`);
            }
        });
        
        // Analyze contract
        async function analyzeContract() {
            const contractId = document.getElementById('contractId').value;
            
            if (!contractId) {
                showError('Please enter a contract ID');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch(`${API_BASE}/analyze/${contractId}`, {
                    method: 'POST'
                });
                
                if (!response.ok) {
                    throw new Error(`Analysis failed: ${response.statusText}`);
                }
                
                const data = await response.json();
                displayAnalysisResults(data);
                
            } catch (error) {
                showError(`Error: ${error.message}`);
            }
        }
        
        // Validate contract
        async function validateContract() {
            const contractId = document.getElementById('contractId').value;
            
            if (!contractId) {
                showError('Please enter a contract ID');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch(`${API_BASE}/validate/${contractId}`, {
                    method: 'POST'
                });
                
                if (!response.ok) {
                    throw new Error(`Validation failed: ${response.statusText}`);
                }
                
                const data = await response.json();
                displayValidationResults(data);
                
            } catch (error) {
                showError(`Error: ${error.message}`);
            }
        }
        
        // List contracts
        async function listContracts() {
            try {
                const response = await fetch(`${API_BASE}/contracts/`);
                const contracts = await response.json();
                
                if (contracts.length === 0) {
                    document.getElementById('contractsList').style.display = 'none';
                    return;
                }
                
                let html = '';
                contracts.forEach(contract => {
                    html += `
                        <div class="contract-item">
                            <div class="contract-info">
                                <strong>${contract.name}</strong>
                                <small>ID: ${contract.id} | Type: ${contract.file_type} | Size: ${(contract.file_size / 1024).toFixed(2)} KB</small>
                            </div>
                            <div class="contract-actions">
                                <button onclick="deleteContract(${contract.id})">Delete</button>
                            </div>
                        </div>
                    `;
                });
                
                document.getElementById('contractsContainer').innerHTML = html;
                document.getElementById('contractsList').style.display = 'block';
                
            } catch (error) {
                console.error('Error listing contracts:', error);
            }
        }
        
        // Delete contract
        async function deleteContract(contractId) {
            if (!confirm('Are you sure you want to delete this contract?')) return;
            
            try {
                await fetch(`${API_BASE}/contracts/${contractId}`, {
                    method: 'DELETE'
                });
                listContracts();
            } catch (error) {
                showError(`Error: ${error.message}`);
            }
        }
        
        // Display analysis results
        function displayAnalysisResults(data) {
            let html = '<h3>📌 Extracted Clauses</h3>';
            
            if (data.clauses && data.clauses.length > 0) {
                data.clauses.forEach(clause => {
                    html += `
                        <div class="result-item">
                            <strong>${clause.clause_type} <span class="status info">${clause.confidence_score}%</span></strong>
                            <p>${clause.clause_text || 'N/A'}</p>
                        </div>
                    `;
                });
            } else {
                html += '<p>No clauses extracted</p>';
            }
            
            hideLoading();
            document.getElementById('resultsContainer').innerHTML = html;
            document.getElementById('results').classList.add('show');
        }
        
        // Display validation results
        function displayValidationResults(data) {
            let html = '<h3>✅ Validation Results</h3>';
            
            if (data.summary) {
                html += `
                    <div class="result-item">
                        <strong>Summary</strong>
                        <p>✓ Passed: ${data.summary.passed} | ✗ Errors: ${data.summary.errors} | ⚠ Warnings: ${data.summary.warnings} | ℹ Info: ${data.summary.info}</p>
                    </div>
                `;
            }
            
            if (data.results && data.results.length > 0) {
                data.results.forEach(result => {
                    const statusClass = result.is_passed ? 'success' : result.severity === 'ERROR' ? 'error' : result.severity === 'WARNING' ? 'warning' : 'info';
                    const statusText = result.is_passed ? '✓ PASS' : '✗ FAIL';
                    
                    html += `
                        <div class="result-item">
                            <strong>${result.rule_name} <span class="status ${statusClass}">${statusText}</span></strong>
                            <p>${result.message || result.rule_description}</p>
                        </div>
                    `;
                });
            }
            
            hideLoading();
            document.getElementById('resultsContainer').innerHTML = html;
            document.getElementById('results').classList.add('show');
        }
        
        // UI Helpers
        function showLoading() {
            document.getElementById('loading').classList.add('show');
            document.getElementById('errorMessage').classList.remove('show');
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.remove('show');
        }
        
        function showError(message) {
            hideLoading();
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.classList.add('show');
            document.getElementById('results').classList.add('show');
        }
        
        function showResults(title, data) {
            hideLoading();
            let html = `<h3>${title}</h3>`;
            Object.entries(data).forEach(([key, value]) => {
                html += `<div class="result-item"><strong>${key}:</strong> <p>${value}</p></div>`;
            });
            document.getElementById('resultsContainer').innerHTML = html;
            document.getElementById('results').classList.add('show');
        }
        
        // Load contracts on page load
        window.addEventListener('load', listContracts);
    </script>
</body>
</html>
"""


def get_frontend_html():
    """Return HTML content"""
    return HTML_CONTENT
