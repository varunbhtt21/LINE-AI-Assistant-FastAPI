from fastapi import APIRouter, Depends, Request, Response, HTTPException, status, Header
from sqlalchemy.orm import Session
import json
from typing import Optional

from app.database.database import get_db
from app.services.message_service import MessageService
from app.utils.auth import verify_line_signature
from app.utils.validators import LineWebhookRequest
from app.utils.logging import log_error, get_exception_traceback, logger

router = APIRouter()

@router.post("/webhook")
async def line_webhook(
    request: Request,
    x_line_signature: Optional[str] = Header(None, convert_underscores=False),
    db: Session = Depends(get_db)
):
    """
    Endpoint for LINE webhook events.
    
    Args:
        request: FastAPI request object.
        x_line_signature: LINE signature header.
        db: Database session.
        
    Returns:
        Response: FastAPI response object.
    """
    # Get the request body
    body = await request.body()
    
    # If this is a verification request from LINE (empty body or very small), 
    # return 200 OK without verification
    if len(body) < 10:
        logger.info("Received verification request from LINE")
        return Response(status_code=status.HTTP_200_OK)
    
    try:
        # Verify the signature for normal webhook events
        if x_line_signature:
            try:
                await verify_line_signature(body, x_line_signature)
            except HTTPException as e:
                # Log the error but continue processing
                logger.error(f"Signature verification failed: {str(e)}")
                # For LINE verification, we still want to return 200
                if len(body) < 100:  # Likely a verification request
                    return Response(status_code=status.HTTP_200_OK)
                raise
        
        # Parse the request body
        webhook_data = json.loads(body)
        webhook_request = LineWebhookRequest(**webhook_data)
        
        # Process each event
        for event in webhook_request.events:
            try:
                # Create a message service
                message_service = MessageService(db)
                
                # Process the event
                await message_service.process_event(event)
            
            except Exception as e:
                # Log the error but continue processing other events
                log_error(
                    db,
                    "EventProcessingError",
                    str(e),
                    get_exception_traceback(),
                    {"event": event.dict()}
                )
        
        # Return a 200 OK response
        return Response(status_code=status.HTTP_200_OK)
    
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Log the error
        log_error(
            db,
            "WebhookProcessingError",
            str(e),
            get_exception_traceback(),
            {"body": body.decode("utf-8")}
        )
        
        # Return a 200 OK response to prevent LINE from retrying
        return Response(status_code=status.HTTP_200_OK) 