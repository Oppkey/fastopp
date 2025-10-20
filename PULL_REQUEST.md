# Add Django-style `startproject` Command

## 🚀 Overview

This PR introduces a new `startproject` command that allows users to quickly bootstrap a complete FastOpp project from scratch, similar to Django's `django-admin startproject`. This addresses the limitation where `uv add fastopp` only installed the basic package without the full project structure, scripts, and demo data.

## 🎯 Problem

Previously, when users ran `uv add fastopp`, they only got a minimal FastAPI app without:
- Full project structure (templates, static files, scripts)
- Database initialization scripts
- Demo data and sample content
- Admin panels and management tools
- Complete documentation and examples

This created a poor user experience where users had to manually clone the repository and set up everything themselves.

## ✨ Solution

### New `startproject` Command

Added a new console script `fastopp-startproject` that:

1. **Clones the complete FastOpp repository** from GitHub
2. **Sets up the full project structure** with all files and directories
3. **Installs all dependencies** automatically
4. **Initializes the database** with proper migrations
5. **Populates demo data** including users, products, and webinars
6. **Creates a fresh git repository** for the new project
7. **Provides clear next steps** for the user

### Usage

```bash
# Create new project directory
mkdir my-fastapi-project && cd my-fastapi-project

# Initialize with uv (optional)
uv init  # or uv init --vcs none

# Install fastopp
uv add fastopp

# Start the complete project
uv run fastopp-startproject
```

## 🔧 Technical Implementation

### Console Scripts

Added to `pyproject.toml`:
```toml
[project.scripts]
fastopp = "fastopp:app"
fastopp-startproject = "fastopp:startproject"
```

### Smart Directory Handling

The command intelligently handles different scenarios:

- **Empty directory**: Works perfectly
- **`uv init` files**: Allows `.venv`, `pyproject.toml`, `uv.lock`, `main.py`, `.python-version`, `README.md`, `.git`, `.gitignore`
- **Existing git repo**: Clones to temp directory, moves files, reinitializes git
- **Non-empty directory**: Prevents accidental overwrites

### Copy Strategy

Uses a robust copy technique:
1. Clone repository to temporary directory (`fastopp-temp`)
2. Move all files (except `.git`) to current directory
3. Remove temporary directory
4. Initialize fresh git repository
5. Install dependencies and initialize database

## 📁 Files Changed

### Core Files
- `pyproject.toml` - Added console scripts and build configuration
- `fastopp/__init__.py` - Added `startproject` function and `create_app` fallback
- `oppman.py` - Added `startproject` command to CLI

### Documentation
- `README.md` - Updated with new installation instructions
- `docs/CONTRIBUTING.md` - Added publishing guidelines

## 🧪 Testing

### Tested Scenarios
- ✅ Empty directory
- ✅ Directory with `uv init` files
- ✅ Directory with `uv init --vcs none` files
- ✅ Directory with existing git repository
- ✅ Error handling for non-empty directories
- ✅ Database initialization and demo data loading
- ✅ Both `uv` and `pip` installation methods

### Test Commands
```bash
# Test with uv
mkdir test-project && cd test-project
uv init
uv add fastopp
uv run fastopp-startproject

# Test with pip
mkdir test-project && cd test-project
python -m venv venv
source venv/bin/activate
pip install fastopp
fastopp-startproject
```

## 🎉 Benefits

### For Users
- **One-command setup**: Complete project in seconds
- **Django-like experience**: Familiar workflow for Django developers
- **Full feature set**: Get everything, not just basic app
- **Demo data included**: Ready to explore and learn
- **Clear documentation**: Step-by-step instructions

### For Developers
- **Consistent project structure**: Every project starts the same way
- **Best practices included**: Proper git setup, dependency management
- **Easy customization**: Clean starting point for modifications
- **Comprehensive examples**: Learn from working code

## 🔄 Migration Guide

### Existing Users
No breaking changes! Existing installations continue to work.

### New Users
```bash
# Old way (basic app only)
uv add fastopp
# Result: Minimal FastAPI app

# New way (complete project)
uv add fastopp
uv run fastopp-startproject
# Result: Full FastOpp project with admin, demo data, etc.
```

## 📋 Checklist

- [x] Add `startproject` function to `fastopp/__init__.py`
- [x] Add `startproject` command to `oppman.py`
- [x] Update `pyproject.toml` with console scripts
- [x] Handle various directory states (empty, uv init, git repo)
- [x] Implement robust copy strategy
- [x] Add comprehensive error handling
- [x] Test with both `uv` and `pip`
- [x] Update documentation
- [x] Remove unused variables (code quality)
- [x] Test database initialization and demo data

## 🚀 Next Steps

After this PR is merged:
1. Publish updated package to PyPI
2. Update installation documentation
3. Create tutorial videos showing the new workflow
4. Consider adding project templates (e.g., `fastopp-startproject --template=minimal`)

## 🔗 Related Issues

Fixes the core issue where `uv add fastopp` only provided a basic app instead of the complete project template.

---

**Ready for review!** This PR significantly improves the developer experience by providing a Django-style project initialization command that sets up a complete, working FastOpp project in seconds.
