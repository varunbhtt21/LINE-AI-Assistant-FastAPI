import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """Application settings."""
    
    # FastAPI settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "makkaizou_line")
    
    # LINE settings
    LINE_CHANNEL_SECRET: str = os.getenv("LINE_CHANNEL_SECRET", "")
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    
    # Makkaizou settings
    MAKKAIZOU_API_KEY: str = os.getenv("MAKKAIZOU_API_KEY", "")
    MAKKAIZOU_API_URL: str = os.getenv("MAKKAIZOU_API_URL", "")
    MAKKAIZOU_LEARNING_MODEL_CODE: str = os.getenv("MAKKAIZOU_LEARNING_MODEL_CODE", "")
    
    class Config:
        extra = "ignore"

# Create settings instance
settings = Settings() 