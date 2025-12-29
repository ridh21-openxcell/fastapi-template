"""AWS module configuration."""
from src.config import settings

# AWS Configuration
AWS_REGION = settings.AWS_REGION or "us-east-1"
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

# AWS Service endpoints (if using localstack or custom endpoints)
AWS_ENDPOINT_URL = None  # e.g., "http://localhost:4566" for localstack

