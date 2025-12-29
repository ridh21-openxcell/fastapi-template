"""Auth service layer."""
from typing import Optional
from sqlalchemy.orm import Session
from src.auth import models, schemas, exceptions
from src.auth.utils import verify_password, get_password_hash, create_access_token
from datetime import timedelta
from src.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user."""
    # Check if user already exists
    if get_user_by_email(db, user.email):
        raise exceptions.UserAlreadyExistsError()
    
    if get_user_by_username(db, user.username):
        raise exceptions.UserAlreadyExistsError("Username already exists")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate a user."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login_user(db: Session, login_data: schemas.LoginRequest) -> schemas.Token:
    """Login a user and return access token."""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise exceptions.InvalidCredentialsError()
    
    if not user.is_active:
        raise exceptions.InvalidCredentialsError("User account is inactive")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return schemas.Token(access_token=access_token, token_type="bearer")

