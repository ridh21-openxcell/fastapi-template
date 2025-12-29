"""Auth module constants."""
from enum import Enum


class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class TokenType(str, Enum):
    """Token types."""
    ACCESS = "access"
    REFRESH = "refresh"


# Error messages
ERROR_INVALID_CREDENTIALS = "Invalid email or password"
ERROR_USER_NOT_FOUND = "User not found"
ERROR_USER_ALREADY_EXISTS = "User already exists"
ERROR_INVALID_TOKEN = "Invalid token"
ERROR_TOKEN_EXPIRED = "Token has expired"
ERROR_INSUFFICIENT_PERMISSIONS = "Insufficient permissions"

