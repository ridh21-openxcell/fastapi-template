"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import os

from src.config import settings
from src.exceptions import (
    BaseAPIException,
    base_exception_handler,
    validation_exception_handler,
    http_exception_handler
)
from src.database import engine, Base

# Import routers
from src.auth.router import router as auth_router
from src.posts.router import router as posts_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(BaseAPIException, base_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(posts_router, prefix="/api/v1/posts", tags=["posts"])

# Serve static files and templates
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
if os.path.exists(templates_dir):
    app.mount("/static", StaticFiles(directory=templates_dir), name="static")


@app.get("/")
async def root():
    """Root endpoint - serves index.html if available."""
    index_path = os.path.join(templates_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
