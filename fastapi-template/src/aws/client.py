"""AWS client for external service communication."""
import boto3
from typing import Optional, BinaryIO
from datetime import datetime, timedelta
from botocore.exceptions import ClientError, BotoCoreError
from src.aws.config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ENDPOINT_URL
from src.aws.exceptions import AWSConnectionError, S3UploadError, S3DownloadError
from src.aws.constants import DEFAULT_BUCKET_NAME


class S3Client:
    """S3 client for file operations."""
    
    def __init__(self):
        """Initialize S3 client."""
        try:
            self.s3_client = boto3.client(
                's3',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                endpoint_url=AWS_ENDPOINT_URL
            )
        except Exception as e:
            raise AWSConnectionError(f"Failed to initialize S3 client: {str(e)}")
    
    def upload_file(
        self,
        file_obj: BinaryIO,
        file_key: str,
        bucket_name: str = DEFAULT_BUCKET_NAME,
        content_type: Optional[str] = None
    ) -> str:
        """Upload a file to S3."""
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                file_key,
                ExtraArgs=extra_args
            )
            
            # Return file URL
            if AWS_ENDPOINT_URL:
                file_url = f"{AWS_ENDPOINT_URL}/{bucket_name}/{file_key}"
            else:
                file_url = f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
            
            return file_url
        except (ClientError, BotoCoreError) as e:
            raise S3UploadError(f"Failed to upload file: {str(e)}")
    
    def download_file(
        self,
        file_key: str,
        bucket_name: str = DEFAULT_BUCKET_NAME
    ) -> bytes:
        """Download a file from S3."""
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
            return response['Body'].read()
        except (ClientError, BotoCoreError) as e:
            raise S3DownloadError(f"Failed to download file: {str(e)}")
    
    def delete_file(
        self,
        file_key: str,
        bucket_name: str = DEFAULT_BUCKET_NAME
    ) -> bool:
        """Delete a file from S3."""
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_key)
            return True
        except (ClientError, BotoCoreError) as e:
            raise S3DownloadError(f"Failed to delete file: {str(e)}")
    
    def generate_presigned_url(
        self,
        file_key: str,
        bucket_name: str = DEFAULT_BUCKET_NAME,
        expiration: int = 3600
    ) -> str:
        """Generate a presigned URL for file access."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
        except (ClientError, BotoCoreError) as e:
            raise S3DownloadError(f"Failed to generate presigned URL: {str(e)}")


# Singleton instance
s3_client = S3Client()

