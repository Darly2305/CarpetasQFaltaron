# Shared authentication utilities
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from backend_python.shared.config import settings

def create_access_token(data: dict) -> str:
    """Generate JWT access token for authenticated users"""
    # Copy data and add expiration time
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode JWT token
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        # Decode token and return payload
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )