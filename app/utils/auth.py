import hmac
import hashlib
import base64
from fastapi import HTTPException, Header, Depends, status
from typing import Optional

from app.config import settings

def validate_line_signature(body: bytes, signature: str) -> bool:
    """
    Validate the signature from LINE.
    
    Args:
        body: The request body as bytes.
        signature: The signature from the X-Line-Signature header.
        
    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    hash = hmac.new(settings.LINE_CHANNEL_SECRET.encode('utf-8'), body, hashlib.sha256).digest()
    calculated_signature = base64.b64encode(hash).decode('utf-8')
    
    return hmac.compare_digest(calculated_signature, signature)

async def verify_line_signature(
    body: bytes,
    x_line_signature: str
) -> None:
    """
    Verify the LINE signature.
    
    Args:
        body: The request body as bytes.
        x_line_signature: The signature from the X-Line-Signature header.
        
    Raises:
        HTTPException: If the signature is invalid or missing.
    """
    if not x_line_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Line-Signature header is missing"
        )
    
    # Convert x_line_signature to string if it's not already
    signature_str = str(x_line_signature)
    
    if not validate_line_signature(body, signature_str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        ) 