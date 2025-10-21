# Storage System

This module provides a modular file storage system that supports both local filesystem and S3-compatible object storage. The storage backend is automatically selected based on environment variables, making it easy to switch between development and production configurations.

## Features

- **Modular Design**: Clean abstraction that allows switching between storage backends
- **Environment-Based Configuration**: Automatic backend selection via environment variables
- **S3-Compatible**: Works with AWS S3, LeapCell Object Storage, and other S3-compatible services
- **Development-Friendly**: Defaults to filesystem storage for local development
- **Production-Ready**: Supports S3 for cloud deployments where filesystem access is limited

## Quick Start

### Development (Filesystem Storage)

No configuration needed! The system defaults to filesystem storage:

```bash
# Files are stored in static/uploads/ by default
uv run python scripts/download_sample_photos.py
```

> **Note**: The application automatically loads environment variables from a `.env` file if present. You can copy `example.env` to `.env` and modify the values as needed.
### Production (S3 Storage)

Create a `.env` file with the required environment variables:

```bash
# Required for S3 storage
STORAGE_TYPE=s3
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_BUCKET=your_bucket_name

# Optional S3 configuration
S3_ENDPOINT_URL=https://objstorage.leapcell.io  # For LeapCell
S3_REGION=us-east-1
S3_CDN_URL=https://your-account.leapcellobj.com/your-bucket
```

## Environment Variables

### Storage Selection

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_TYPE` | `filesystem` | Storage backend: `filesystem` or `s3` |

### Filesystem Storage

| Variable | Default | Description |
|----------|---------|-------------|
| `UPLOAD_DIR` | `static/uploads` | Base directory for file storage |

### S3 Storage

| Variable | Required | Description |
|----------|----------|-------------|
| `S3_ACCESS_KEY` | Yes | S3 access key |
| `S3_SECRET_KEY` | Yes | S3 secret key |
| `S3_BUCKET` | Yes | S3 bucket name |
| `S3_ENDPOINT_URL` | No | S3 endpoint URL (for non-AWS services) |
| `S3_REGION` | `us-east-1` | S3 region |
| `S3_CDN_URL` | No | CDN URL for public file access |

## Usage

### Basic Usage

```python

from services.storage import get_storage

# Get configured storage instance
storage = get_storage()

# Ensure directories exist
storage.ensure_directories("photos", "sample_photos")

# Save a file
photo_url = storage.save_file(
    content=image_bytes,
    path="photos/avatar.jpg",
    content_type="image/jpeg"
)

# Check if file exists
if storage.file_exists("photos/avatar.jpg"):
    print("File exists!")

# Get file content
image_data = storage.get_file("photos/avatar.jpg")

# Get public URL
public_url = storage.get_file_url("photos/avatar.jpg")

```
### Advanced Usage
```python

from services.storage import get_storage

storage = get_storage()

# List files with prefix
photos = storage.list_files("photos/")

# Delete a file
success = storage.delete_file("photos/old_avatar.jpg")

# Check storage type
if isinstance(storage, FilesystemStorage):
    print("Using local filesystem")
elif isinstance(storage, S3Storage):
    print("Using S3 object storage")

```
## Storage Backends

### FilesystemStorage

- **Use Case**: Development, local deployments
- **Pros**: Simple, fast, no external dependencies
- **Cons**: Not suitable for cloud deployments, no CDN support

### S3Storage

- **Use Case**: Production, cloud deployments
- **Pros**: Scalable, CDN support, persistent across deployments
- **Cons**: Requires S3 credentials, network dependency

## Configuration Examples

### Development (.env)

Create a `.env` file:

```bash
# Use filesystem storage (default)
STORAGE_TYPE=filesystem
UPLOAD_DIR=static/uploads
```
### Production with LeapCell

Create a `.env` file:

```bash
# Use S3 storage with LeapCell Object Storage
STORAGE_TYPE=s3
S3_ACCESS_KEY=your_leapcell_access_key
S3_SECRET_KEY=your_leapcell_secret_key
S3_BUCKET=your_bucket_name
S3_ENDPOINT_URL=https://objstorage.leapcell.io
S3_CDN_URL=https://your-account.leapcellobj.com/your-bucket
```
### Production with AWS S3

Create a `.env` file:

```bash
# Use S3 storage with AWS S3
STORAGE_TYPE=s3
S3_ACCESS_KEY=your_aws_access_key
S3_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_bucket_name
S3_REGION=us-west-2
```
## Migration Guide

### From Hardcoded Paths

**Before:**

```python

# Hardcoded filesystem paths
upload_dir = "static/uploads"
photo_path = Path(upload_dir) / "photos" / filename
photo_path.parent.mkdir(parents=True, exist_ok=True)
with open(photo_path, "wb") as f:
    f.write(content)

```
**After:**

```python

# Modular storage system
from services.storage import get_storage
storage = get_storage()
storage.ensure_directories("photos")
photo_url = storage.save_file(content, f"photos/{filename}", "image/jpeg")

```
### From Environment Variables

**Before:**

```python

# Manual environment variable handling
upload_dir = os.getenv("UPLOAD_DIR", "static/uploads")

```
**After:**

```python

# Automatic configuration
from services.storage import get_storage
storage = get_storage()  # Automatically configured based on environment

```
## Error Handling

The storage system provides consistent error handling across backends:
```python

from services.storage import get_storage

storage = get_storage()

try:
    content = storage.get_file("nonexistent.jpg")
except FileNotFoundError:
    print("File not found")

try:
    url = storage.save_file(content, "path/file.jpg")
except RuntimeError as e:
    print(f"Storage error: {e}")

```
## Testing

The storage system can be easily mocked for testing:
```python

from unittest.mock import Mock
from services.storage import get_storage

# Mock storage for testing
mock_storage = Mock()
mock_storage.save_file.return_value = "/static/uploads/test.jpg"
mock_storage.file_exists.return_value = True

# Use in tests
with patch('services.storage.get_storage', return_value=mock_storage):
    # Your test code here
    pass

```
