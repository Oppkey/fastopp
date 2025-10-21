"""
Storage abstraction module for modular file storage.

This module provides a clean abstraction for file storage operations,
supporting both local filesystem and S3-compatible object storage.
"""

from .base import StorageInterface
from .filesystem import FilesystemStorage
from .s3 import S3Storage
from .factory import get_storage

__all__ = [
    "StorageInterface",
    "FilesystemStorage",
    "S3Storage",
    "get_storage"
]
