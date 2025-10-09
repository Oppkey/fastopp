---
layout: post
title: "File Upload Demo Now Runs on S3 in Addition to Local Files"
date: 2025-10-08
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/2025_10/run.jpg
excerpt: "Moved image upload storage from only files to include S3"
---

## 🎯 Overview

FastOpp demo system moved to a modular storage system that abstracts file storage operations, supporting both local filesystem and S3-compatible object storage. The system is designed to work seamlessly in development (filesystem) and production (S3) environments, with automatic backend selection based on environment variables.

## 🚀 Key Features

### **Modular Storage Architecture**
- **Abstract Interface**: Clean abstraction for storage operations
- **Multiple Backends**: Filesystem and S3-compatible storage
- **Environment-Based Configuration**: Automatic backend selection
- **Production-Ready**: Supports LeapCell Object Storage and AWS S3

### **Demo Assets Integration**
- **Save/Restore Support**: Storage system included in demo workflow
- **Destroy/Restore Cycle**: Storage system can be removed and restored
- **Change Detection**: Storage system changes tracked in diff operations

## 📁 Files Added

### **Storage System Core**
- `services/storage/__init__.py` - Module exports and imports
- `services/storage/base.py` - Abstract storage interface
- `services/storage/filesystem.py` - Filesystem storage implementation
- `services/storage/s3.py` - S3-compatible storage implementation
- `services/storage/factory.py` - Storage factory for backend selection
- `services/storage/README.md` - Comprehensive documentation

## 🔄 Files Modified

### **Core Application Files**
- `oppdemo.py` - Updated to use modular storage system
  - `ensure_upload_dirs()` now uses storage abstraction
  - Added storage system to save/restore/destroy workflow
  - Added storage system to diff comparison

### **Scripts Updated**
- `scripts/download_sample_photos.py` - Updated to use storage abstraction
- `demo_scripts/download_sample_photos.py` - Updated to use storage abstraction

### **Configuration**
- `example.env` - Added comprehensive storage configuration options
  - Storage type selection (`STORAGE_TYPE`)
  - Filesystem storage options (`UPLOAD_DIR`)
  - S3 storage options (access keys, bucket, endpoint, CDN)

## 🗑️ Files Removed

### **Cleanup**
- `storage/` (project root) - Redundant folder removed
  - Contained only `base.py` which was identical to `services/storage/base.py`
  - No code references to old location

## 🔧 Technical Implementation

### **Storage Interface**
```python
class StorageInterface(ABC):
    def ensure_directories(self, *paths: str) -> None
    def save_file(self, content: bytes, path: str, content_type: Optional[str] = None) -> str
    def get_file(self, path: str) -> bytes
    def file_exists(self, path: str) -> bool
    def delete_file(self, path: str) -> bool
    def list_files(self, prefix: str = "") -> List[str]
    def get_file_url(self, path: str) -> str
```

### **Backend Implementations**

#### **FilesystemStorage**
- Local file storage for development
- Automatic directory creation
- Static file serving via FastAPI mounts
- URL generation for static file access

#### **S3Storage**
- S3-compatible object storage for production
- Supports AWS S3, LeapCell Object Storage, and other S3-compatible services
- CDN URL support for public file access
- Automatic content type detection

### **Factory Pattern**
```python
def get_storage() -> StorageInterface:
    storage_type = os.getenv("STORAGE_TYPE", "filesystem").lower()
    if storage_type == "s3":
        return _create_s3_storage()
    else:
        return _create_filesystem_storage()
```

## 🌍 Environment Configuration

### **Development (Default)**
```bash
# No configuration needed - uses filesystem storage
STORAGE_TYPE=filesystem
UPLOAD_DIR=static/uploads
```

### **Production with LeapCell**
```bash
STORAGE_TYPE=s3
S3_ACCESS_KEY=your_leapcell_access_key
S3_SECRET_KEY=your_leapcell_secret_key
S3_BUCKET=your_bucket_name
S3_ENDPOINT_URL=https://objstorage.leapcell.io
S3_CDN_URL=https://your-account.leapcellobj.com/your-bucket
```

### **Production with AWS S3**
```bash
STORAGE_TYPE=s3
S3_ACCESS_KEY=your_aws_access_key
S3_SECRET_KEY=your_aws_secret_key
S3_BUCKET=your_bucket_name
S3_REGION=us-west-2
```

## 🔄 Migration Guide

### **From Hardcoded Paths**
**Before:**
```python
upload_dir = "static/uploads"
photo_path = Path(upload_dir) / "photos" / filename
photo_path.parent.mkdir(parents=True, exist_ok=True)
with open(photo_path, "wb") as f:
    f.write(content)
```

**After:**
```python
from services.storage import get_storage
storage = get_storage()
storage.ensure_directories("photos")
photo_url = storage.save_file(content, f"photos/{filename}", "image/jpeg")
```

### **From Environment Variables**
**Before:**
```python
upload_dir = os.getenv("UPLOAD_DIR", "static/uploads")
```

**After:**
```python
from services.storage import get_storage
storage = get_storage()  # Automatically configured based on environment
```

## 🧪 Testing

### **Storage System Tests**
- ✅ Filesystem storage functionality
- ✅ S3 storage configuration (without actual S3 access)
- ✅ Environment detection and backend selection
- ✅ Import path validation
- ✅ Demo assets integration

### **Demo Workflow Tests**
- ✅ Save functionality includes storage system
- ✅ Restore functionality restores storage system
- ✅ Destroy functionality removes storage system
- ✅ Diff functionality compares storage system
- ✅ No differences found after save/restore cycle

## 📚 Documentation

### **Comprehensive README**
- **Quick Start Guide**: Development and production setup
- **Environment Variables**: Complete configuration reference
- **Usage Examples**: Basic and advanced usage patterns
- **Migration Guide**: Step-by-step migration instructions
- **Configuration Examples**: Development, LeapCell, and AWS S3 setups
- **Error Handling**: Consistent error handling across backends

### **Code Documentation**
- **Type Hints**: Full type annotations for all methods
- **Docstrings**: Comprehensive documentation for all classes and methods
- **Examples**: Usage examples in docstrings
- **Error Handling**: Clear error messages and exception handling

## 🎯 Benefits

### **For Development**
- **Zero Configuration**: Works out of the box with filesystem storage
- **Easy Testing**: Simple to mock and test
- **Clear Separation**: Storage logic separated from business logic
- **Type Safety**: Full type hints and validation

### **For Production**
- **Cloud-Ready**: Seamless S3 integration for cloud deployments
- **CDN Support**: Built-in CDN URL generation
- **Scalable**: Object storage scales with application needs
- **Persistent**: Files persist across deployments

### **For Deployment**
- **Environment-Based**: Automatic backend selection
- **LeapCell Compatible**: Works with LeapCell Object Storage
- **AWS Compatible**: Works with AWS S3
- **Flexible**: Easy to add new storage backends

## 🔄 Demo Assets Integration

### **Save Workflow**
```bash
uv run python oppdemo.py save
# → Saves services/storage/ to demo_assets/services/storage/
```

### **Restore Workflow**
```bash
uv run python oppdemo.py restore
# → Restores services/storage/ from demo_assets/services/storage/
```

### **Destroy Workflow**
```bash
uv run python oppdemo.py destroy
# → Removes services/ directory (including storage/)
```

### **Diff Workflow**
```bash
uv run python oppdemo.py diff
# → Shows differences in services/storage/ module
```

## 🚀 Usage Examples

### **Basic Usage**
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

### **Advanced Usage**
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

## ✅ Quality Assurance

### **Code Quality**
- **Linting**: All code passes linting checks
- **Type Safety**: Full type hints throughout
- **Error Handling**: Comprehensive error handling
- **Documentation**: Complete docstrings and comments

### **Testing**
- **Unit Tests**: Storage system functionality tested
- **Integration Tests**: Demo workflow integration tested
- **Environment Tests**: Multiple environment configurations tested
- **Error Tests**: Error conditions and edge cases tested

### **Documentation**
- **README**: Comprehensive documentation with examples
- **Code Comments**: Clear comments explaining complex logic
- **Type Hints**: Full type annotations for IDE support
- **Examples**: Practical usage examples throughout

## 🎉 Summary

1. **Clean Architecture**: Abstract interface with concrete implementations
2. **Environment Flexibility**: Automatic backend selection based on configuration
3. **Production Ready**: Full S3 support for cloud deployments
4. **Development Friendly**: Zero-configuration filesystem storage
5. **Demo Integration**: Seamless integration with demo assets workflow
6. **Comprehensive Documentation**: Complete usage and configuration guide

The storage system is now a first-class citizen in the application, providing a clean abstraction for file operations while maintaining backward compatibility and adding powerful new capabilities for production deployments.
