import pytest
from fastapi.testclient import TestClient
import json
import base64
import hmac
import hashlib

from app.main import app
from app.config import settings

client = TestClient(app)

def generate_signature(body: bytes, channel_secret: str) -> str:
    """
    Generate a signature for testing.
    
    Args:
        body: Request body as bytes.
        channel_secret: LINE channel secret.
        
    Returns:
        str: Generated signature.
    """
    hash = hmac.new(channel_secret.encode('utf-8'), body, hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode('utf-8')
    return signature

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Makkaizou-LINE Integration API"}

def test_webhook_missing_signature():
    """Test the webhook endpoint with missing signature."""
    response = client.post("/webhook/line", json={})
    assert response.status_code == 401
    assert "X-Line-Signature header is missing" in response.text

def test_webhook_invalid_signature():
    """Test the webhook endpoint with invalid signature."""
    body = json.dumps({"events": []}).encode('utf-8')
    response = client.post(
        "/webhook/line",
        headers={"X-Line-Signature": "invalid-signature"},
        content=body
    )
    assert response.status_code == 401
    assert "Invalid signature" in response.text

def test_webhook_valid_signature():
    """Test the webhook endpoint with valid signature."""
    # Create a sample webhook event
    webhook_event = {
        "destination": "xxxxxxxxxx",
        "events": []
    }
    
    # Convert to JSON and then to bytes
    body = json.dumps(webhook_event).encode('utf-8')
    
    # Generate a valid signature
    signature = generate_signature(body, settings.LINE_CHANNEL_SECRET)
    
    # Send the request
    response = client.post(
        "/webhook/line",
        headers={"X-Line-Signature": signature},
        content=body
    )
    
    # Check the response
    assert response.status_code == 200 