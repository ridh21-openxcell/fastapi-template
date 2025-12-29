"""Auth dependencies."""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth import schemas, service, exceptions
from src.auth.utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> schemas.UserResponse:
    """Get current authenticated user."""
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise exceptions.InvalidTokenError()
    except exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = service.get_user_by_email(db, email)
    if user is None:
        raise exceptions.UserNotFoundError()
    
    return user


async def get_current_active_user(
    current_user: schemas.UserResponse = Depends(get_current_user)
) -> schemas.UserResponse:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: schemas.UserResponse = Depends(get_current_active_user)
) -> schemas.UserResponse:
    """Get current admin user."""
    if not current_user.is_superuser:
        raise exceptions.InsufficientPermissionsError()
    return current_user

