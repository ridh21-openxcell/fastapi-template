"""Auth router endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth import schemas, service, dependencies

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    return service.create_user(db, user)


@router.post("/login", response_model=schemas.Token)
async def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    return service.login_user(db, login_data)


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(
    current_user: schemas.UserResponse = Depends(dependencies.get_current_active_user)
):
    """Get current user information."""
    return current_user

