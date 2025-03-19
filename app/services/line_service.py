from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import uuid

from app.config import settings
from app.database.models import LineAccount, LineGroup
from app.utils.logging import log_error, logger

class LineService:
    """Service for interacting with the LINE API."""
    
    def __init__(self, db: Session, line_account: Optional[LineAccount] = None):
        """
        Initialize the LINE service.
        
        Args:
            db: Database session.
            line_account: LINE account to use. If None, the default account will be used.
        """
        self.db = db
        self.line_account = line_account
        
        # Use the provided account or get the default one
        if line_account is None:
            self.line_account = self._get_default_line_account()
        
        # Initialize the LINE Bot API client
        if self.line_account:
            self.line_bot_api = LineBotApi(self.line_account.channel_access_token)
        else:
            # Use the settings if no account is found
            self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    
    def _get_default_line_account(self) -> Optional[LineAccount]:
        """
        Get the default LINE account.
        
        Returns:
            Optional[LineAccount]: The default LINE account, or None if not found.
        """
        return self.db.query(LineAccount).filter(LineAccount.is_active == True).first()
    
    def get_or_create_line_group(self, group_id: str) -> LineGroup:
        """
        Get or create a LINE group.
        
        Args:
            group_id: LINE group ID.
            
        Returns:
            LineGroup: The LINE group.
        """
        # Check if the group exists
        group = self.db.query(LineGroup).filter(LineGroup.line_group_id == group_id).first()
        
        # If not, create it
        if group is None:
            # Generate a unique talk_id for Makkaizou
            talk_id = f"line-{uuid.uuid4()}"
            
            # Create the group
            group = LineGroup(
                line_group_id=group_id,
                line_account_id=self.line_account.id if self.line_account else None,
                makkaizou_talk_id=talk_id
            )
            
            # Save to database
            self.db.add(group)
            self.db.commit()
            self.db.refresh(group)
        
        return group
    
    def send_reply(self, reply_token: str, message: str) -> Dict[str, Any]:
        """
        Send a reply message to LINE.
        
        Args:
            reply_token: Reply token from the webhook event.
            message: Message to send.
            
        Returns:
            Dict[str, Any]: Response from LINE API.
        """
        try:
            # Create a text message
            text_message = TextSendMessage(text=message)
            
            # Send the reply
            response = self.line_bot_api.reply_message(reply_token, text_message)
            
            logger.info(f"Sent reply to LINE: {message}")
            
            return {"status": "success", "response": response}
        
        except LineBotApiError as e:
            # Log the error
            log_error(
                self.db,
                "LineBotApiError",
                str(e),
                None,
                {"reply_token": reply_token, "message": message}
            )
            
            return {"status": "error", "error": str(e)} 