"""Auth database models."""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from src.models import BaseModel
from src.auth.constants import UserRole


class User(BaseModel):
    """User model."""
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

