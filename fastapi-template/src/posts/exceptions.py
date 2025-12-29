"""Posts module exceptions."""
from src.exceptions import BaseAPIException, NotFoundError, ForbiddenError
from src.posts.constants import (
    ERROR_POST_NOT_FOUND,
    ERROR_POST_ALREADY_EXISTS,
    ERROR_UNAUTHORIZED_POST_ACCESS
)


class PostNotFoundError(NotFoundError):
    """Post not found exception."""
    def __init__(self, message: str = ERROR_POST_NOT_FOUND):
        super().__init__(message)


class PostAlreadyExistsError(BaseAPIException):
    """Post already exists exception."""
    def __init__(self, message: str = ERROR_POST_ALREADY_EXISTS):
        super().__init__(message, status_code=409)


class UnauthorizedPostAccessError(ForbiddenError):
    """Unauthorized post access exception."""
    def __init__(self, message: str = ERROR_UNAUTHORIZED_POST_ACCESS):
        super().__init__(message)

