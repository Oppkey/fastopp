"""
Storage factory for creating storage instances based on configuration.
"""

import os

from .base import StorageInterface
from .filesystem import FilesystemStorage
from .s3 import S3Storage


def get_storage() -> StorageInterface:
    """
    Get storage instance based on environment configuration.
    
    Environment variables:
    - STORAGE_TYPE: "filesystem" or "s3" (default: "filesystem")
    - UPLOAD_DIR: Base directory for filesystem storage (default: "static/uploads")
    - S3_ACCESS_KEY: S3 access key (required for S3 storage)
    - S3_SECRET_KEY: S3 secret key (required for S3 storage)
    - S3_BUCKET: S3 bucket name (required for S3 storage)
    - S3_ENDPOINT_URL: S3 endpoint URL (optional, for non-AWS services)
    - S3_REGION: S3 region (default: "us-east-1")
    - S3_CDN_URL: CDN URL for public file access (optional)
    
    Returns:
        StorageInterface: Configured storage instance
    """
    storage_type = os.getenv("STORAGE_TYPE", "filesystem").lower()
    
    if storage_type == "s3":
        return _create_s3_storage()
    else:
        return _create_filesystem_storage()


def _create_filesystem_storage() -> FilesystemStorage:
    """Create filesystem storage instance."""
    upload_dir = os.getenv("UPLOAD_DIR", "static/uploads")
    return FilesystemStorage(base_path=upload_dir)


def _create_s3_storage() -> S3Storage:
    """Create S3 storage instance."""
    # Get required S3 configuration
    access_key = os.getenv("S3_ACCESS_KEY")
    secret_key = os.getenv("S3_SECRET_KEY")
    bucket = os.getenv("S3_BUCKET")
    
    if not all([access_key, secret_key, bucket]):
        raise ValueError(
            "S3 storage requires S3_ACCESS_KEY, S3_SECRET_KEY, and S3_BUCKET environment variables"
        )
    
    # Get optional S3 configuration
    endpoint_url = os.getenv("S3_ENDPOINT_URL")
    region = os.getenv("S3_REGION", "us-east-1")
    cdn_url = os.getenv("S3_CDN_URL")
    
    return S3Storage(
        access_key=access_key,
        secret_key=secret_key,
        bucket=bucket,
        endpoint_url=endpoint_url,
        region=region,
        cdn_url=cdn_url
    )
