"""
S3-compatible object storage implementation.
"""

from typing import Optional, List
from urllib.parse import quote

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    boto3 = None
    ClientError = Exception

from .base import StorageInterface


class S3Storage(StorageInterface):
    """
    S3-compatible object storage implementation.
    
    Supports any S3-compatible service including AWS S3, LeapCell Object Storage, etc.
    """
    
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket: str,
        endpoint_url: Optional[str] = None,
        region: str = "us-east-1",
        cdn_url: Optional[str] = None
    ):
        """
        Initialize S3 storage.
        
        Args:
            access_key: S3 access key
            secret_key: S3 secret key
            bucket: S3 bucket name
            endpoint_url: S3 endpoint URL (for non-AWS services)
            region: S3 region
            cdn_url: CDN URL for public file access (optional)
        """
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 is required for S3 storage. Install with: pip install boto3")
        
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.region = region
        self.cdn_url = cdn_url
        
        # Initialize S3 client
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
            region_name=region
        )
    
    def ensure_directories(self, *paths: str) -> None:
        """
        Ensure that the specified directories exist.
        
        Note: S3 doesn't have directories, but we can create placeholder objects
        to simulate directory structure if needed.
        """
        # S3 doesn't require directories to be created
        # Files can be stored with path-like keys
        pass
    
    def save_file(self, content: bytes, path: str, content_type: Optional[str] = None) -> str:
        """Save file content to S3."""
        try:
            # Upload to S3
            self.client.put_object(
                Bucket=self.bucket,
                Key=path,
                Body=content,
                ContentType=content_type or "application/octet-stream"
            )
            
            # Return public URL
            return self.get_file_url(path)
            
        except ClientError as e:
            raise RuntimeError(f"Failed to upload file to S3: {e}")
    
    def get_file(self, path: str) -> bytes:
        """Retrieve file content from S3."""
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=path)
            return response["Body"].read()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File not found: {path}")
            raise RuntimeError(f"Failed to retrieve file from S3: {e}")
    
    def file_exists(self, path: str) -> bool:
        """Check if a file exists in S3."""
        try:
            print(f"DEBUG: Checking if file exists: {path} in bucket: {self.bucket}")
            
            # Try head_object first (preferred method)
            try:
                response = self.client.head_object(Bucket=self.bucket, Key=path)
                print(f"DEBUG: File exists (head_object): {path}")
                return True
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    print(f"DEBUG: File not found (404): {path}")
                    return False
                # For other errors, fall back to list_files method
                print(f"DEBUG: HeadObject failed, trying list_files: {e}")
            
            # Fallback: Use list_files to check existence
            # This is less efficient but more reliable
            try:
                # Get directory path for the file
                if "/" in path:
                    prefix = path.rsplit("/", 1)[0] + "/"
                else:
                    prefix = ""
                
                print(f"DEBUG: Using list_files fallback with prefix: '{prefix}'")
                files = self.list_files(prefix)
                file_exists = path in files
                print(f"DEBUG: File exists (list_files): {path} = {file_exists}")
                return file_exists
                
            except Exception as list_error:
                print(f"DEBUG: List files also failed: {list_error}")
                return False
                
        except Exception as e:
            print(f"DEBUG: Unexpected error checking {path}: {e}")
            return False
    
    def delete_file(self, path: str) -> bool:
        """Delete a file from S3."""
        try:
            self.client.delete_object(Bucket=self.bucket, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return False
            raise RuntimeError(f"Failed to delete file from S3: {e}")
    
    def list_files(self, prefix: str = "") -> List[str]:
        """List files in S3 with optional prefix filter."""
        try:
            print(f"DEBUG: Listing files with prefix: '{prefix}' in bucket: {self.bucket}")
            response = self.client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=prefix
            )
            
            files = []
            for obj in response.get("Contents", []):
                files.append(obj["Key"])
                print(f"DEBUG: Found file: {obj['Key']}")
            
            print(f"DEBUG: Total files found: {len(files)}")
            return files
            
        except ClientError as e:
            print(f"DEBUG: Error listing files: {e}")
            raise RuntimeError(f"Failed to list files in S3: {e}")
    
    def get_file_url(self, path: str) -> str:
        """Get the public URL for accessing a file."""
        if self.cdn_url:
            # Use CDN URL if provided
            encoded_path = quote(path, safe="/")
            return f"{self.cdn_url.rstrip('/')}/{encoded_path}"
        else:
            # Use S3 endpoint URL
            if self.endpoint_url:
                return f"{self.endpoint_url.rstrip('/')}/{self.bucket}/{path}"
            else:
                # AWS S3 URL format
                return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{path}"
