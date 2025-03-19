import httpx
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json

from app.config import settings
from app.database.models import MakkaizouConfig
from app.utils.logging import log_error, logger

class MakkaizouService:
    """Service for interacting with the Makkaizou API."""
    
    def __init__(self, db: Session, makkaizou_config: Optional[MakkaizouConfig] = None):
        """
        Initialize the Makkaizou service.
        
        Args:
            db: Database session.
            makkaizou_config: Makkaizou configuration to use. If None, the default configuration will be used.
        """
        self.db = db
        self.makkaizou_config = makkaizou_config
        
        # Use the provided configuration or get the default one
        if makkaizou_config is None:
            self.makkaizou_config = self._get_default_makkaizou_config()
        
        # Use the configuration or settings
        if self.makkaizou_config:
            self.api_key = self.makkaizou_config.api_key
            self.api_url = self.makkaizou_config.api_url
            self.learning_model_code = self.makkaizou_config.learning_model_code
            self.model_settings = self.makkaizou_config.model_settings
        else:
            # Use the settings if no configuration is found
            self.api_key = settings.MAKKAIZOU_API_KEY
            self.api_url = settings.MAKKAIZOU_API_URL
            self.learning_model_code = settings.MAKKAIZOU_LEARNING_MODEL_CODE
            self.model_settings = {}
    
    def _get_default_makkaizou_config(self) -> Optional[MakkaizouConfig]:
        """
        Get the default Makkaizou configuration.
        
        Returns:
            Optional[MakkaizouConfig]: The default Makkaizou configuration, or None if not found.
        """
        return self.db.query(MakkaizouConfig).filter(MakkaizouConfig.is_active == True).first()
    
    async def process_prompt(self, talk_id: str, prompt: str) -> Dict[str, Any]:
        """
        Process a prompt using the Makkaizou API.
        
        Args:
            talk_id: Talk ID for Makkaizou.
            prompt: Prompt to process.
            
        Returns:
            Dict[str, Any]: Response from Makkaizou API.
        """
        # Prepare the request headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # Prepare the request payload as form data
        form_data = {
            "external_integration_key": self.api_key,
            "learning_model_code": self.learning_model_code,
            "message": prompt,
            "talk_id": talk_id
        }
        
        try:
            # Send the request to Makkaizou API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    data=form_data,
                    headers=headers,
                    timeout=30.0  # 30 seconds timeout
                )
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Parse the response
                result = response.json()
                
                logger.info(f"Received response from Makkaizou API: {json.dumps(result)[:100]}...")
                
                # Check if there's an error in the response
                if "error_code" in result:
                    error_message = f"Makkaizou API error: {result.get('error_code')} - {result.get('message', 'Unknown error')}"
                    log_error(
                        self.db,
                        "MakkaizouAPIError",
                        error_message,
                        None,
                        {"talk_id": talk_id, "prompt": prompt}
                    )
                    
                    return {
                        "status": "error",
                        "error": error_message
                    }
                
                return {
                    "status": "success",
                    "response": result
                }
        
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors
            error_message = f"HTTP error: {e.response.status_code} - {e.response.text}"
            log_error(
                self.db,
                "MakkaizouAPIHTTPError",
                error_message,
                None,
                {"talk_id": talk_id, "prompt": prompt}
            )
            
            return {
                "status": "error",
                "error": error_message
            }
        
        except httpx.RequestError as e:
            # Handle request errors (connection, timeout, etc.)
            error_message = f"Request error: {str(e)}"
            log_error(
                self.db,
                "MakkaizouAPIRequestError",
                error_message,
                None,
                {"talk_id": talk_id, "prompt": prompt}
            )
            
            return {
                "status": "error",
                "error": error_message
            }
        
        except Exception as e:
            # Handle other errors
            error_message = f"Unexpected error: {str(e)}"
            log_error(
                self.db,
                "MakkaizouAPIUnexpectedError",
                error_message,
                None,
                {"talk_id": talk_id, "prompt": prompt}
            )
            
            return {
                "status": "error",
                "error": error_message
            } 