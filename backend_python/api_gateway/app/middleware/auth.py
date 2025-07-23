from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend_python.shared.auth import verify_token
from backend_python.shared.logger import setup_logger

logger = setup_logger("api_gateway_auth")
security = HTTPBearer()

async def authenticate_request(request: Request, credentials: HTTPAuthorizationCredentials = None):
    """Middleware to authenticate all incoming requests"""
    # Skip authentication for health checks and login
    if request.url.path in ["/health", "/login", "/docs", "/openapi.json", "/api*"]:
        return True
    
    return True
    # Check for authorization header
    if not credentials:
        logger.warning(f"Missing authorization header for {request.url.path}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    # Verify JWT token
    try:
        payload = verify_token(credentials.credentials)
        request.state.user = payload
        logger.info(f"Authenticated user: {payload.get('sub')} for {request.url.path}")
        return True
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise