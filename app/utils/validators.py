from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

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
    Check if the event is a mention event.
    
    Args:
        event: LINE webhook event.
        
    Returns:
        bool: True if the event is a mention event, False otherwise.
    """
    # Check if the event is a message event
    if event.type != "message":
        return False
    
    # Check if the message is a text message
    if event.message is None or event.message.get("type") != "text":
        return False
    
    # Check if the message has a mention
    mention = event.message.get("mention")
    if mention is None:
        return False
    
    # Check if the mention is for the LINE Official Account
    mentionees = mention.get("mentionees", [])
    for mentionee in mentionees:
        if mentionee.get("type") == "user":
            return True
    
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