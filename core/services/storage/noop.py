"""
No-op storage implementation for serverless environments.
"""

from typing import List, Optional

from .base import StorageInterface


class NoOpStorage(StorageInterface):
    """
    No-op storage implementation for serverless environments.
    
    This storage implementation does nothing and always returns errors,
    allowing the application to run without file upload capabilities
    when UPLOAD_DIR is not set or filesystem access is not available.
    """
    
    def __init__(self):
        """Initialize no-op storage."""
        pass
    
    def ensure_directories(self, *paths: str) -> None:
        """No-op: directories cannot be created in serverless environments."""
        pass
    
    def save_file(self, content: bytes, path: str, content_type: Optional[str] = None) -> str:
        """Raise error: file uploads not supported in serverless mode."""
        raise RuntimeError(
            "File uploads are not available. The application is running in serverless mode. "
            "To enable file uploads, configure S3 storage by setting STORAGE_TYPE=s3 and "
            "providing S3_ACCESS_KEY, S3_SECRET_KEY, and S3_BUCKET environment variables."
        )
    
    def get_file(self, path: str) -> bytes:
        """Raise error: file retrieval not supported in serverless mode."""
        raise RuntimeError(
            "File retrieval is not available. The application is running in serverless mode. "
            "To enable file access, configure S3 storage by setting STORAGE_TYPE=s3 and "
            "providing S3_ACCESS_KEY, S3_SECRET_KEY, and S3_BUCKET environment variables."
        )
    
    def file_exists(self, path: str) -> bool:
        """Return False: no files exist in serverless mode."""
        return False
    
    def delete_file(self, path: str) -> bool:
        """Return False: no files to delete in serverless mode."""
        return False
    
    def list_files(self, prefix: str = "") -> List[str]:
        """Return empty list: no files in serverless mode."""
        return []
    
    def get_file_url(self, path: str) -> str:
        """Return placeholder URL: no files in serverless mode."""
        return "/static/placeholder.jpg"
