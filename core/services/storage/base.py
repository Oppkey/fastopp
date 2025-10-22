"""
Abstract base class for storage implementations.
"""

from abc import ABC, abstractmethod
from typing import Optional, List


class StorageInterface(ABC):
    """
    Abstract interface for file storage operations.
    
    This interface provides a consistent API for different storage backends
    (filesystem, S3, etc.) allowing the application to switch between them
    based on environment configuration.
    """
    
    @abstractmethod
    def ensure_directories(self, *paths: str) -> None:
        """
        Ensure that the specified directories exist.
        
        Args:
            *paths: Directory paths to create
        """
        pass
    
    @abstractmethod
    def save_file(self, content: bytes, path: str, content_type: Optional[str] = None) -> str:
        """
        Save file content to storage.
        
        Args:
            content: File content as bytes
            path: Storage path for the file
            content_type: MIME type of the content
            
        Returns:
            URL or path to access the saved file
        """
        pass
    
    @abstractmethod
    def get_file(self, path: str) -> bytes:
        """
        Retrieve file content from storage.
        
        Args:
            path: Storage path of the file
            
        Returns:
            File content as bytes
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        pass
    
    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """
        Check if a file exists in storage.
        
        Args:
            path: Storage path of the file
            
        Returns:
            True if file exists, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_file(self, path: str) -> bool:
        """
        Delete a file from storage.
        
        Args:
            path: Storage path of the file
            
        Returns:
            True if file was deleted, False if it didn't exist
        """
        pass
    
    @abstractmethod
    def list_files(self, prefix: str = "") -> List[str]:
        """
        List files in storage with optional prefix filter.
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            List of file paths
        """
        pass
    
    @abstractmethod
    def get_file_url(self, path: str) -> str:
        """
        Get the public URL for accessing a file.
        
        Args:
            path: Storage path of the file
            
        Returns:
            Public URL to access the file
        """
        pass
