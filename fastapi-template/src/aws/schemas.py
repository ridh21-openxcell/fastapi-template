"""AWS Pydantic schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class S3UploadResponse(BaseModel):
    """S3 upload response schema."""
    file_url: str
    file_key: str
    bucket_name: str
    uploaded_at: datetime


class S3FileInfo(BaseModel):
    """S3 file information schema."""
    file_key: str
    bucket_name: str
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[datetime] = None


class PresignedURLRequest(BaseModel):
    """Presigned URL request schema."""
    file_key: str
    expiration: int = 3600  # seconds


class PresignedURLResponse(BaseModel):
    """Presigned URL response schema."""
    url: str
    expires_in: int

