import sys
import traceback
from loguru import logger
from sqlalchemy.orm import Session

from app.database.models import ErrorLog, MessageLog
from app.config import settings

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG" if settings.DEBUG else "INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

def log_error(db: Session, error_type: str, error_message: str, stack_trace: str = None, request_data: dict = None, line_group_id: str = None):
    """
    Log an error to the database and console.
    
    Args:
        db: Database session.
        error_type: Type of error.
        error_message: Error message.
        stack_trace: Stack trace of the error.
        request_data: Request data that caused the error.
        line_group_id: LINE group ID where the error occurred.
    """
    # Log to console
    logger.error(f"{error_type}: {error_message}")
    if stack_trace:
        logger.error(f"Stack trace: {stack_trace}")
    
    # Log to database
    error_log = ErrorLog(
        error_type=error_type,
        error_message=error_message,
        stack_trace=stack_trace,
        request_data=request_data,
        line_group_id=line_group_id
    )
    
    db.add(error_log)
    db.commit()

def log_message(
    db: Session,
    line_group_id: str,
    user_id: str,
    message_text: str,
    is_mention: bool = False,
    makkaizou_request: dict = None,
    makkaizou_response: dict = None,
    line_response_status: str = None,
    processing_time_ms: int = None
):
    """
    Log a message interaction to the database.
    
    Args:
        db: Database session.
        line_group_id: LINE group ID.
        user_id: User ID.
        message_text: Message text.
        is_mention: Whether the message mentions the LINE Official Account.
        makkaizou_request: Request sent to Makkaizou API.
        makkaizou_response: Response from Makkaizou API.
        line_response_status: Status of the LINE response.
        processing_time_ms: Processing time in milliseconds.
    """
    message_log = MessageLog(
        line_group_id=line_group_id,
        user_id=user_id,
        message_text=message_text,
        is_mention=is_mention,
        makkaizou_request=makkaizou_request,
        makkaizou_response=makkaizou_response,
        line_response_status=line_response_status,
        processing_time_ms=processing_time_ms
    )
    
    db.add(message_log)
    db.commit()

def get_exception_traceback():
    """
    Get the traceback of the current exception.
    
    Returns:
        str: Traceback as a string.
    """
    return traceback.format_exc() 