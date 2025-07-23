# API Gateway main application
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend_python.api_gateway.app.routes.gateway import router as gateway_router
from backend_python.shared.auth import create_access_token
from backend_python.shared.logger import setup_logger

# Initialize FastAPI app and logger
app = FastAPI(title="API Gateway", version="1.0.0")
logger = setup_logger("api_gateway")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include gateway routes
app.include_router(gateway_router, prefix="/api", tags=["gateway"])

class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    # Simple authentication logic (replace with real authentication)
    if request.username == "admin" and request.password == "password":
        token = create_access_token({"sub": request.username, "role": "admin"})
        logger.info(f"User {request.username} logged in successfully")
        return {"access_token": token, "token_type": "bearer"}
    
    logger.warning(f"Failed login attempt for user: {request.username}")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    logger.info("Health check requested")
    return {"status": "healthy", "service": "api_gateway"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting API Gateway on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)