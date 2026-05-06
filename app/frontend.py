"""
Modern HTML Frontend for ContractIQ
Professional UI with modern design and no external dependencies
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
        
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --dark: #1f2937;
            --gray: #6b7280;
            --light: #f9fafb;
            --border: #e5e7eb;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Header */
        header {
            background: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            border-bottom: 4px solid var(--primary);
            text-align: center;
        }
        
        h1 {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        
        .subtitle {
            color: var(--gray);
            font-size: 16px;
            font-weight: 500;
        }
        
        /* Main Content */
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 1px solid var(--border);
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        }
        
        .card h2 {
            font-size: 22px;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .card h2 span {
            font-size: 28px;
        }
        
        /* Form Styles */
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            color: var(--dark);
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        input[type="file"],
        input[type="text"],
        select {
            width: 100%;
            padding: 14px 16px;
            border: 2px solid var(--border);
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s ease;
            background: var(--light);
            font-family: inherit;
        }
        
        input[type="file"]:focus,
        input[type="text"]:focus,
        select:focus {
            outline: none;
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }
        
        /* Button Styles */
        button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 14px 28px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .button-group button {
            width: 100%;
        }
        
        /* Results Section */
        .results {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            display: none;
            border-top: 4px solid var(--primary);
        }
        
        .results.show {
            display: block;
            animation: slideUp 0.3s ease;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .results h3 {
            font-size: 20px;
            color: var(--dark);
            margin-bottom: 20px;
            font-weight: 700;
        }
        
        /* Result Items */
        .result-item {
            background: linear-gradient(135deg, var(--light) 0%, #ffffff 100%);
            padding: 18px;
            margin-bottom: 15px;
            border-left: 5px solid var(--primary);
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        
        .result-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .result-item strong {
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            font-size: 15px;
        }
        
        .result-item p {
            color: var(--gray);
            font-size: 14px;
            line-height: 1.6;
        }
        
        /* Status Badges */
        .status {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status.success {
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
        }
        
        .status.error {
            background: rgba(239, 68, 68, 0.15);
            color: var(--danger);
        }
        
        .status.warning {
            background: rgba(245, 158, 11, 0.15);
            color: var(--warning);
        }
        
        .status.info {
            background: rgba(59, 130, 246, 0.15);
            color: var(--info);
        }
        
        /* Loading Spinner */
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid rgba(99, 102, 241, 0.15);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading p {
            margin-top: 15px;
            color: var(--gray);
            font-weight: 500;
        }
        
        /* Error Message */
        .error-message {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            padding: 16px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
            border-left: 4px solid var(--danger);
            font-weight: 500;
        }
        
        .error-message.show {
            display: block;
            animation: slideUp 0.3s ease;
        }
        
        /* Contracts List */
        .contracts-list {
            margin-top: 40px;
        }
        
        .contracts-list h2 {
            margin-bottom: 20px;
        }
        
        .contract-item {
            background: linear-gradient(135deg, var(--light) 0%, #ffffff 100%);
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
        }
        
        .contract-item:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .contract-info {
            flex: 1;
        }
        
        .contract-info strong {
            color: var(--dark);
            font-size: 16px;
            font-weight: 700;
        }
        
        .contract-info small {
            color: var(--gray);
            display: block;
            margin-top: 8px;
            font-size: 13px;
        }
        
        .contract-actions {
            display: flex;
            gap: 10px;
        }
        
        .contract-actions button {
            width: auto;
            padding: 10px 20px;
            font-size: 12px;
            background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%);
        }
        
        .contract-actions button:hover {
            background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        }
        
        /* Footer */
        footer {
            text-align: center;
            color: white;
            padding: 30px 20px;
            font-size: 14px;
            margin-top: 40px;
        }
        
        footer a {
            color: white;
            text-decoration: underline;
            transition: opacity 0.3s;
        }
        
        footer a:hover {
            opacity: 0.8;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            header {
                padding: 25px;
            }
            
            h1 {
                font-size: 28px;
            }
            
            .main-content {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .button-group {
                grid-template-columns: 1fr;
            }
            
            .card {
                padding: 20px;
            }
            
            .contract-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
            
            .contract-actions {
                width: 100%;
            }
            
            .contract-actions button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <h1>ContractIQ 🤖</h1>
            <p class="subtitle">AI-Powered Contract Testing & Validation Platform</p>
        </header>
        
        <!-- Main Content -->
        <div class="main-content">
            <!-- Upload Section -->
            <div class="card">
                <h2><span>📄</span> Upload Contract</h2>
                <form id="uploadForm">
                    <div class="form-group">
                        <label for="contractFile">Select PDF or DOCX file</label>
                        <input type="file" id="contractFile" name="file" accept=".pdf,.docx" required>
                    </div>
                    <button type="submit">📤 Upload Contract</button>
                </form>
            </div>
            
            <!-- Analysis Section -->
            <div class="card">
                <h2><span>🔍</span> Analyze & Validate</h2>
                <form id="analysisForm">
                    <div class="form-group">
                        <label for="contractId">Contract ID</label>
                        <input type="text" id="contractId" name="contractId" placeholder="Enter contract ID" required>
                    </div>
                    <div class="button-group">
                        <button type="button" onclick="analyzeContract()">🔬 Analyze</button>
                        <button type="button" onclick="validateContract()">✅ Validate</button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Contracts List -->
        <div class="card contracts-list" id="contractsList" style="display: none;">
            <h2><span>📋</span> Uploaded Contracts</h2>
            <div id="contractsContainer"></div>
        </div>
        
        <!-- Results Section -->
        <div class="card results" id="results">
            <h2><span>📊</span> Analysis Results</h2>
            <div class="error-message" id="errorMessage"></div>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>⏳ Processing your contract...</p>
            </div>
            <div id="resultsContainer"></div>
        </div>
        
        <!-- Footer -->
        <footer>
            <p>© ContractIQ v1.0.0 | <a href="http://localhost:8000/docs">📖 API Docs</a> | <a href="http://localhost:8000">🏠 Home</a></p>
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
                showResults(`✓ Contract uploaded successfully!`, {
                    'Contract ID': contract.id,
                    'Name': contract.name,
                    'Type': contract.file_type.toUpperCase(),
                    'Size': `${(contract.file_size / 1024 / 1024).toFixed(2)} MB`,
                    'Status': contract.text_extracted ? '✓ Text Extracted' : '⏳ Pending'
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
                                <strong>📄 ${contract.name}</strong>
                                <small>ID: ${contract.id} | Type: ${contract.file_type.toUpperCase()} | Size: ${(contract.file_size / 1024).toFixed(2)} KB</small>
                            </div>
                            <div class="contract-actions">
                                <button onclick="deleteContract(${contract.id})">🗑️ Delete</button>
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
                showResults('✓ Contract deleted', {'Status': 'Successfully removed'});
            } catch (error) {
                showError(`Error: ${error.message}`);
            }
        }
        
        // Display analysis results
        function displayAnalysisResults(data) {
            let html = '<h3>📦 Extracted Clauses</h3>';
            
            if (data.clauses && data.clauses.length > 0) {
                data.clauses.forEach(clause => {
                    html += `
                        <div class="result-item">
                            <strong>📌 ${clause.clause_type} <span class="status info">${clause.confidence_score}% Confidence</span></strong>
                            <p>${clause.clause_text || 'No content available'}</p>
                        </div>
                    `;
                });
            } else {
                html += '<p>ℹ️ No clauses extracted</p>';
            }
            
            hideLoading();
            document.getElementById('resultsContainer').innerHTML = html;
            document.getElementById('results').classList.add('show');
        }
        
        // Display validation results
        function displayValidationResults(data) {
            let html = '<h3>🛡️ Validation Results</h3>';
            
            if (data.summary) {
                html += `
                    <div class="result-item">
                        <strong>📈 Summary</strong>
                        <p>
                            <span class="status success">✓ ${data.summary.passed} Passed</span>
                            <span class="status error">✗ ${data.summary.errors} Errors</span>
                            <span class="status warning">⚠ ${data.summary.warnings} Warnings</span>
                            <span class="status info">ℹ ${data.summary.info} Info</span>
                        </p>
                    </div>
                `;
            }
            
            if (data.results && data.results.length > 0) {
                data.results.forEach(result => {
                    const statusClass = result.is_passed ? 'success' : result.severity === 'ERROR' ? 'error' : result.severity === 'WARNING' ? 'warning' : 'info';
                    const statusIcon = result.is_passed ? '✓' : '✗';
                    const statusText = result.is_passed ? 'PASS' : 'FAIL';
                    
                    html += `
                        <div class="result-item">
                            <strong>✓ ${result.rule_name} <span class="status ${statusClass}">${statusIcon} ${statusText}</span></strong>
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
