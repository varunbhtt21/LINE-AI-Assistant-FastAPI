from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from app.database.models import MessageLog, ErrorLog
from app.config import settings
import sys

def get_db():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def view_message_logs(limit=10):
    """View the most recent message logs"""
    db = get_db()
    logs = db.query(MessageLog).order_by(desc(MessageLog.created_at)).limit(limit).all()
    
    print("\n=== Recent Message Logs ===")
    for log in logs:
        print(f"\nTimestamp: {log.created_at}")
        print(f"Group ID: {log.line_group_id}")
        print(f"User ID: {log.user_id}")
        print(f"Message: {log.message_text}")
        print(f"Is Mention: {log.is_mention}")
        print(f"Processing Time: {log.processing_time_ms}ms")
        print("-" * 50)

def view_error_logs(limit=10):
    """View the most recent error logs"""
    db = get_db()
    logs = db.query(ErrorLog).order_by(desc(ErrorLog.created_at)).limit(limit).all()
    
    print("\n=== Recent Error Logs ===")
    for log in logs:
        print(f"\nTimestamp: {log.created_at}")
        print(f"Error Type: {log.error_type}")
        print(f"Message: {log.error_message}")
        print(f"Group ID: {log.line_group_id}")
        print("-" * 50)

if __name__ == "__main__":
    # Get number of logs to view from command line argument, default to 10
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    view_message_logs(limit)
    view_error_logs(limit) 