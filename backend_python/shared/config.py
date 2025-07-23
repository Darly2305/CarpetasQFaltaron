# Configuration management for microservices
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Global configuration settings for all microservices"""
    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # Service URLs
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://ai_service:8001")
    NOTIFICATION_SERVICE_URL: str = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification_service:8002")
    SENSOR_SERVICE_URL: str = os.getenv("SENSOR_SERVICE_URL", "http://sensor_service:8003")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./microservices.db")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"

settings = Settings()