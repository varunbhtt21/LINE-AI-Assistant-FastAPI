from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base

class LineAccount(Base):
    """Model for LINE Official Accounts."""
    
    __tablename__ = "line_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String(100), nullable=False)
    channel_id = Column(String(50), unique=True, nullable=False)
    channel_secret = Column(String(100), nullable=False)
    channel_access_token = Column(String(200), nullable=False)
    webhook_url = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    groups = relationship("LineGroup", back_populates="line_account")
    makkaizou_mappings = relationship("LineAccountMakkaizouMapping", back_populates="line_account")

class MakkaizouConfig(Base):
    """Model for Makkaizou API configurations."""
    
    __tablename__ = "makkaizou_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String(100), nullable=False)
    api_url = Column(String(200), nullable=False)
    learning_model_code = Column(String(100), nullable=False)
    model_settings = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    line_account_mappings = relationship("LineAccountMakkaizouMapping", back_populates="makkaizou_config")

class LineAccountMakkaizouMapping(Base):
    """Model for mapping LINE accounts to Makkaizou configurations."""
    
    __tablename__ = "line_account_makkaizou_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    line_account_id = Column(Integer, ForeignKey("line_accounts.id", ondelete="CASCADE"))
    makkaizou_config_id = Column(Integer, ForeignKey("makkaizou_configs.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    line_account = relationship("LineAccount", back_populates="makkaizou_mappings")
    makkaizou_config = relationship("MakkaizouConfig", back_populates="line_account_mappings")

class LineGroup(Base):
    """Model for LINE groups."""
    
    __tablename__ = "line_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    line_group_id = Column(String(100), unique=True, nullable=False)
    group_name = Column(String(100))
    line_account_id = Column(Integer, ForeignKey("line_accounts.id", ondelete="CASCADE"))
    makkaizou_talk_id = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    line_account = relationship("LineAccount", back_populates="groups")
    message_logs = relationship("MessageLog", back_populates="line_group")

class MessageLog(Base):
    """Model for message logs."""
    
    __tablename__ = "message_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    line_group_id = Column(String(100), ForeignKey("line_groups.line_group_id"))
    user_id = Column(String(100), nullable=False)
    message_text = Column(Text, nullable=False)
    is_mention = Column(Boolean, default=False)
    makkaizou_request = Column(JSON)
    makkaizou_response = Column(JSON)
    line_response_status = Column(String(50))
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    line_group = relationship("LineGroup", back_populates="message_logs")

class ErrorLog(Base):
    """Model for error logs."""
    
    __tablename__ = "error_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text)
    request_data = Column(JSON)
    line_group_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 