"""Auth module exceptions."""
from src.exceptions import BaseAPIException, UnauthorizedError, ForbiddenError
from src.auth.constants import (
    ERROR_INVALID_CREDENTIALS,
    ERROR_USER_NOT_FOUND,
    ERROR_USER_ALREADY_EXISTS,
    ERROR_INVALID_TOKEN,
    ERROR_TOKEN_EXPIRED,
    ERROR_INSUFFICIENT_PERMISSIONS
)


class InvalidCredentialsError(UnauthorizedError):
    """Invalid credentials exception."""
    def __init__(self, message: str = ERROR_INVALID_CREDENTIALS):
        super().__init__(message)


class UserNotFoundError(BaseAPIException):
    """User not found exception."""
    def __init__(self, message: str = ERROR_USER_NOT_FOUND):
        super().__init__(message, status_code=404)


class UserAlreadyExistsError(BaseAPIException):
    """User already exists exception."""
    def __init__(self, message: str = ERROR_USER_ALREADY_EXISTS):
        super().__init__(message, status_code=409)


class InvalidTokenError(UnauthorizedError):
    """Invalid token exception."""
    def __init__(self, message: str = ERROR_INVALID_TOKEN):
        super().__init__(message)


class TokenExpiredError(UnauthorizedError):
    """Token expired exception."""
    def __init__(self, message: str = ERROR_TOKEN_EXPIRED):
        super().__init__(message)


class InsufficientPermissionsError(ForbiddenError):
    """Insufficient permissions exception."""
    def __init__(self, message: str = ERROR_INSUFFICIENT_PERMISSIONS):
        super().__init__(message)

