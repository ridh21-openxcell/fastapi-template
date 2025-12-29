"""AWS module constants."""

# S3 bucket names
DEFAULT_BUCKET_NAME = "default-bucket"

# S3 settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ["image/jpeg", "image/png", "image/gif", "application/pdf"]

# Error messages
ERROR_AWS_CONNECTION_FAILED = "Failed to connect to AWS service"
ERROR_S3_UPLOAD_FAILED = "Failed to upload file to S3"
ERROR_S3_DOWNLOAD_FAILED = "Failed to download file from S3"
ERROR_INVALID_FILE_TYPE = "Invalid file type"
ERROR_FILE_TOO_LARGE = "File size exceeds maximum allowed size"

