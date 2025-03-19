from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time

from app.config import settings
from app.database import init_db
from app.api.webhook import router as webhook_router
from app.utils.logging import logger

# Initialize the database
init_db()

# Create the FastAPI application
app = FastAPI(
    title="Makkaizou-LINE Integration",
    description="Integration between Makkaizou and LINE Official Account",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all requests.
    
    Args:
        request: FastAPI request object.
        call_next: Next middleware function.
        
    Returns:
        Response: FastAPI response object.
    """
    start_time = time.time()
    
    # Log the request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log the response
    logger.info(f"Response: {response.status_code} ({process_time:.4f}s)")
    
    return response

# Include routers
app.include_router(webhook_router, tags=["webhook"])

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: Status message.
    """
    return {"status": "ok", "message": "Makkaizou-LINE Integration API"}

# Health check endpoint
@app.get("/health")
async def health():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status.
    """
    return {"status": "ok"} 