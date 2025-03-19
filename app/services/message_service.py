import time
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.services.line_service import LineService
from app.services.makkaizou_service import MakkaizouService
from app.utils.validators import LineWebhookEvent, is_mention_event, extract_group_id, extract_user_id, extract_message_text
from app.utils.logging import log_message, log_error, logger

class MessageService:
    """Service for processing messages."""
    
    def __init__(self, db: Session):
        """
        Initialize the message service.
        
        Args:
            db: Database session.
        """
        self.db = db
        self.line_service = LineService(db)
        self.makkaizou_service = MakkaizouService(db)
    
    async def process_event(self, event: LineWebhookEvent) -> Dict[str, Any]:
        """
        Process a LINE webhook event.
        
        Args:
            event: LINE webhook event.
            
        Returns:
            Dict[str, Any]: Processing result.
        """
        # Start timing
        start_time = time.time()
        
        # Check if the event is a mention event
        if not is_mention_event(event):
            logger.debug("Event is not a mention event, ignoring")
            return {"status": "ignored", "reason": "not_mention_event"}
        
        # Extract information from the event
        group_id = extract_group_id(event)
        user_id = extract_user_id(event)
        message_text = extract_message_text(event)
        reply_token = event.replyToken
        
        # Check if we have all the required information
        if not group_id or not user_id or not message_text or not reply_token:
            logger.warning("Missing required information from event")
            return {"status": "error", "reason": "missing_information"}
        
        # Get or create the LINE group
        line_group = self.line_service.get_or_create_line_group(group_id)
        
        # Log the message
        log_message(
            self.db,
            group_id,
            user_id,
            message_text,
            is_mention=True
        )
        
        # Process the message with Makkaizou
        makkaizou_request = {
            "external_integration_key": self.makkaizou_service.api_key,
            "learning_model_code": self.makkaizou_service.learning_model_code,
            "message": message_text,
            "talk_id": line_group.makkaizou_talk_id
        }
        
        logger.info(f"Processing message with Makkaizou: {message_text}")
        
        makkaizou_response = await self.makkaizou_service.process_prompt(
            line_group.makkaizou_talk_id,
            message_text
        )
        
        # Check if Makkaizou processing was successful
        if makkaizou_response["status"] == "success":
            # Extract the response text from Makkaizou
            response_text = self._extract_response_text(makkaizou_response["response"])
            
            # Send the response back to LINE
            line_response = self.line_service.send_reply(reply_token, response_text)
            
            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Update the message log
            log_message(
                self.db,
                group_id,
                user_id,
                message_text,
                is_mention=True,
                makkaizou_request=makkaizou_request,
                makkaizou_response=makkaizou_response["response"],
                line_response_status=line_response["status"],
                processing_time_ms=processing_time_ms
            )
            
            return {
                "status": "success",
                "processing_time_ms": processing_time_ms,
                "makkaizou_response": makkaizou_response["response"],
                "line_response": line_response
            }
        else:
            # Makkaizou processing failed
            error_message = makkaizou_response.get("error", "Unknown error")
            
            # Send an error message to LINE
            fallback_message = "I'm sorry, but I'm having trouble processing your request. Please try again later."
            line_response = self.line_service.send_reply(reply_token, fallback_message)
            
            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Log the error
            log_error(
                self.db,
                "MakkaizouProcessingError",
                error_message,
                None,
                makkaizou_request,
                group_id
            )
            
            # Update the message log
            log_message(
                self.db,
                group_id,
                user_id,
                message_text,
                is_mention=True,
                makkaizou_request=makkaizou_request,
                makkaizou_response={"error": error_message},
                line_response_status=line_response["status"],
                processing_time_ms=processing_time_ms
            )
            
            return {
                "status": "error",
                "error": error_message,
                "processing_time_ms": processing_time_ms,
                "line_response": line_response
            }
    
    def _extract_response_text(self, makkaizou_response: Dict[str, Any]) -> str:
        """
        Extract the response text from the Makkaizou response.
        
        Args:
            makkaizou_response: Response from Makkaizou API.
            
        Returns:
            str: Response text.
        """
        # According to the Makkaizou API documentation, the response has a "message" field
        if "message" in makkaizou_response:
            message = makkaizou_response["message"]
            
            # Check if there are references to include
            if "references" in makkaizou_response and makkaizou_response["references"]:
                references = makkaizou_response["references"]
                reference_texts = []
                
                for ref in references:
                    # Add the reference content
                    if "content" in ref:
                        reference_texts.append(f"- {ref['content']}")
                    
                    # Add file information if available
                    if "files" in ref and ref["files"]:
                        for file in ref["files"]:
                            if "name" in file and "download_url" in file:
                                reference_texts.append(f"  - {file['name']}: {file['download_url']}")
                
                # If there are references, append them to the message
                if reference_texts:
                    message += "\n\n参考情報:\n" + "\n".join(reference_texts)
            
            return message
        
        # If the response format is different, log a warning and return a fallback message
        logger.warning(f"Could not extract response text from Makkaizou response: {makkaizou_response}")
        return "I'm sorry, but I couldn't generate a proper response. Please try again." 