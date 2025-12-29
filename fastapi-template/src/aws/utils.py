"""AWS utility functions."""
from typing import Optional
from src.aws.constants import MAX_FILE_SIZE, ALLOWED_FILE_TYPES
from src.aws.exceptions import InvalidFileTypeError, FileTooLargeError


def validate_file_type(content_type: str) -> bool:
    """Validate file type."""
    if content_type not in ALLOWED_FILE_TYPES:
        raise InvalidFileTypeError(
            f"File type {content_type} not allowed. Allowed types: {', '.join(ALLOWED_FILE_TYPES)}"
        )
    return True


def validate_file_size(file_size: int) -> bool:
    """Validate file size."""
    if file_size > MAX_FILE_SIZE:
        raise FileTooLargeError(
            f"File size {file_size} exceeds maximum allowed size of {MAX_FILE_SIZE} bytes"
        )
    return True


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return filename.split('.')[-1].lower() if '.' in filename else ""


def generate_file_key(prefix: str, filename: str) -> str:
    """Generate S3 file key with prefix."""
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    extension = get_file_extension(filename)
    return f"{prefix}/{timestamp}_{filename}"

