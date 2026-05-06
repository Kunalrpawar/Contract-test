"""
Frontend route for serving HTML interface
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.frontend import get_frontend_html

router = APIRouter()


@router.get("/ui", response_class=HTMLResponse)
def get_frontend():
    """Serve the frontend HTML interface"""
    return get_frontend_html()


@router.get("/", response_class=HTMLResponse)
def root_html():
    """Root endpoint with welcome message"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ContractIQ - API Server</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 40px; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #667eea; }
            .link-group { margin: 20px 0; }
            a { color: #667eea; text-decoration: none; font-weight: bold; margin-right: 15px; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ContractIQ API Server</h1>
            <p>AI-Powered Contract Testing & Validation Platform</p>
            <div class="link-group">
                <strong>Quick Links:</strong><br><br>
                <a href="/api/v1/health">Health Check</a><br>
                <a href="/docs">API Documentation (Swagger)</a><br>
                <a href="/redoc">API Documentation (ReDoc)</a><br>
                <a href="/ui">Web Interface</a><br>
            </div>
            <div class="link-group">
                <strong>API Endpoints:</strong><br><br>
                <code>POST /api/v1/contracts/upload</code> - Upload contract<br>
                <code>GET /api/v1/contracts</code> - List contracts<br>
                <code>POST /api/v1/analyze/{id}</code> - Analyze contract<br>
                <code>POST /api/v1/validate/{id}</code> - Validate contract<br>
                <code>POST /api/v1/compare/{id1}/{id2}</code> - Compare contracts<br>
            </div>
        </div>
    </body>
    </html>
    """
