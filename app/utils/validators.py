from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class LineWebhookEvent(BaseModel):
    """Model for LINE webhook events."""
    
    type: str
    mode: str
    timestamp: int
    source: Dict[str, Any]
    replyToken: Optional[str] = None
    message: Optional[Dict[str, Any]] = None
    
class LineWebhookRequest(BaseModel):
    """Model for LINE webhook requests."""
    
    destination: str
    events: List[LineWebhookEvent]

def is_mention_event(event: LineWebhookEvent) -> bool:
    """
    Check if the event is a mention event specifically for @bot.
    
    Args:
        event: LINE webhook event.
        
    Returns:
        bool: True if @bot is mentioned at the start with content after, False otherwise.
    """
    try:
        # Check if the event is a message event
        if event.type != "message":
            logger.debug("Not a message event")
            return False
        
        # Check if the message is a text message
        if event.message is None or event.message.get("type") != "text":
            logger.debug("Not a text message")
            return False
            
        # Check if the message has a mention structure
        mention = event.message.get("mention")
        if not mention:
            logger.debug("No mention structure in message")
            return False
        
        # Get mentionees
        mentionees = mention.get("mentionees", [])
        if not mentionees:
            logger.debug("No mentionees in mention")
            return False
            
        # Get the message text
        message_text = event.message.get("text", "").strip()
        if not message_text:
            logger.debug("Empty message text")
            return False
            
        logger.debug(f"Processing message text: '{message_text}'")
            
        # Check each mentionee to find our bot's mention at the start
        for mentionee in mentionees:
            # Only process user mentions that are marked as our bot
            if mentionee.get("type") != "user" or not mentionee.get("isSelf", False):
                logger.debug("Not a user mention or not our bot")
                return False
                
            # Check if this mention is at the start
            start_index = mentionee.get("index", -1)
            if start_index != 0:
                logger.debug("Mention is not at the start of message")
                return False
                
            # Get the mention length
            length = mentionee.get("length", 0)
            if start_index + length > len(message_text):
                logger.debug("Invalid mention bounds")
                return False
                
            # Extract and verify the mentioned text
            mentioned_text = message_text[start_index:start_index + length].strip()
            if mentioned_text != "@bot":
                logger.debug(f"Mention is not @bot: '{mentioned_text}'")
                return False
                
            # Get the content after the mention
            remaining_text = message_text[length:].strip()
            if not remaining_text:
                logger.debug("No content after mention")
                return False
                
            # If we got here, we found a valid @bot mention at the start with content after
            logger.debug(f"Valid @bot mention with content: '{remaining_text}'")
            return True
            
        logger.debug("No valid @bot mention found at start of message")
        return False
        
    except Exception as e:
        logger.error(f"Error in is_mention_event: {str(e)}")
        return False

def extract_group_id(event: LineWebhookEvent) -> Optional[str]:
    """
    Extract the group ID from the event.
    
    Args:
        event: LINE webhook event.
        
    Returns:
        Optional[str]: Group ID if the event is from a group, None otherwise.
    """
    source = event.source
    if source.get("type") == "group":
        return source.get("groupId")
    elif source.get("type") == "room":
        return source.get("roomId")
    return None

def extract_user_id(event: LineWebhookEvent) -> Optional[str]:
    """
    Extract the user ID from the event.
    
    Args:
        event: LINE webhook event.
        
    Returns:
        Optional[str]: User ID if available, None otherwise.
    """
    return event.source.get("userId")

def extract_message_text(event: LineWebhookEvent) -> Optional[str]:
    """
    Extract the message text from the event.
    
    Args:
        event: LINE webhook event.
        
    Returns:
        Optional[str]: Message text if available, None otherwise.
    """
    if event.message is None or event.message.get("type") != "text":
        return None
    return event.message.get("text") 