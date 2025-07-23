# Centralized logging configuration for all microservices
import logging
import sys
from datetime import datetime
from backend_python.shared.config import settings

def setup_logger(service_name: str) -> logging.Logger:
    """Configure structured logging for microservices"""
    # Create logger with service name
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        f'%(asctime)s - {service_name} - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger