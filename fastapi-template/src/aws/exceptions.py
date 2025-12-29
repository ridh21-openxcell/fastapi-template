"""AWS module exceptions."""
from src.exceptions import BaseAPIException
from src.aws.constants import (
    ERROR_AWS_CONNECTION_FAILED,
    ERROR_S3_UPLOAD_FAILED,
    ERROR_S3_DOWNLOAD_FAILED,
    ERROR_INVALID_FILE_TYPE,
    ERROR_FILE_TOO_LARGE
)


class AWSConnectionError(BaseAPIException):
    """AWS connection error."""
    def __init__(self, message: str = ERROR_AWS_CONNECTION_FAILED):
        super().__init__(message, status_code=503)


class S3UploadError(BaseAPIException):
    """S3 upload error."""
    def __init__(self, message: str = ERROR_S3_UPLOAD_FAILED):
        super().__init__(message, status_code=500)


class S3DownloadError(BaseAPIException):
    """S3 download error."""
    def __init__(self, message: str = ERROR_S3_DOWNLOAD_FAILED):
        super().__init__(message, status_code=500)


class InvalidFileTypeError(BaseAPIException):
    """Invalid file type error."""
    def __init__(self, message: str = ERROR_INVALID_FILE_TYPE):
        super().__init__(message, status_code=400)


class FileTooLargeError(BaseAPIException):
    """File too large error."""
    def __init__(self, message: str = ERROR_FILE_TOO_LARGE):
        super().__init__(message, status_code=400)

