"""
Filesystem storage implementation.
"""

from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

from .base import StorageInterface


class FilesystemStorage(StorageInterface):
    """
    Filesystem-based storage implementation.
    
    Stores files on the local filesystem and serves them via static file mounting.
    """
    
    def __init__(self, base_path: str = "static/uploads"):
        """
        Initialize filesystem storage.
        
        Args:
            base_path: Base directory for file storage
        """
        self.base_path = Path(base_path)
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise RuntimeError(
                f"Cannot create upload directory '{base_path}': {e}. "
                "This may be due to serverless environment restrictions. "
                "To enable file uploads, configure S3 storage by setting STORAGE_TYPE=s3 and "
                "providing S3_ACCESS_KEY, S3_SECRET_KEY, and S3_BUCKET environment variables."
            )
    
    def ensure_directories(self, *paths: str) -> None:
        """Ensure that the specified directories exist."""
        for path in paths:
            full_path = self.base_path / path
            full_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(self, content: bytes, path: str, content_type: Optional[str] = None) -> str:
        """Save file content to filesystem."""
        file_path = self.base_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Return URL path for static file serving
        return f"/static/uploads/{path}"
    
    def get_file(self, path: str) -> bytes:
        """Retrieve file content from filesystem."""
        file_path = self.base_path / path
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        with open(file_path, "rb") as f:
            return f.read()
    
    def file_exists(self, path: str) -> bool:
        """Check if a file exists in filesystem."""
        file_path = self.base_path / path
        return file_path.exists()
    
    def delete_file(self, path: str) -> bool:
        """Delete a file from filesystem."""
        file_path = self.base_path / path
        
        if not file_path.exists():
            return False
        
        try:
            file_path.unlink()
            return True
        except OSError:
            return False
    
    def list_files(self, prefix: str = "") -> List[str]:
        """List files in filesystem with optional prefix filter."""
        search_path = self.base_path / prefix if prefix else self.base_path
        
        if not search_path.exists():
            return []
        
        files = []
        for file_path in search_path.rglob("*"):
            if file_path.is_file():
                # Get relative path from base_path
                relative_path = file_path.relative_to(self.base_path)
                files.append(str(relative_path))
        
        return files
    
    def get_file_url(self, path: str) -> str:
        """Get the public URL for accessing a file."""
        # URL encode the path to handle special characters
        encoded_path = quote(path, safe="/")
        return f"/static/uploads/{encoded_path}"
