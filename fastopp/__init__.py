# FastOpp Package
# This package provides a FastAPI starter template for AI web applications

from fastapi import FastAPI
from typing import Optional
import os


def create_app(
    database_url: Optional[str] = None,
    secret_key: Optional[str] = None,
    environment: Optional[str] = None,
    openrouter_api_key: Optional[str] = None,
) -> FastAPI:
    """
    Create a FastAPI application with FastOpp features.

    Args:
        database_url: Database connection string (default: sqlite+aiosqlite:///./app.db)
        secret_key: Secret key for JWT tokens (default: auto-generated)
        environment: Environment setting (default: development)
        openrouter_api_key: OpenRouter API key for AI features (optional)

    Returns:
        Configured FastAPI application
    """
    # Set up environment variables if provided
    if database_url:
        os.environ["DATABASE_URL"] = database_url
    if secret_key:
        os.environ["SECRET_KEY"] = secret_key
    if environment:
        os.environ["ENVIRONMENT"] = environment
    if openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_api_key

    # Import and return the main app
    # Note: This will only work if the full project structure is available
    try:
        from main import app

        return app
    except ImportError:
        # Fallback: create a basic FastAPI app
        app = FastAPI(
            title="FastOpp",
            description="FastAPI starter package for AI web applications",
            version="0.2.3",
        )

        @app.get("/")
        async def root():
            return {
                "message": "FastOpp - FastAPI starter for AI web apps",
                "docs": "/docs",
                "note": "This is a basic installation. For full features, run: uv run python -m fastopp startproject",
            }

        return app


# For backward compatibility
app = create_app()


def startproject():
    """Start a new FastOpp project with full structure from GitHub"""
    import subprocess
    import shutil
    import time
    import platform
    from pathlib import Path
    from importlib.metadata import version

    def remove_directory_with_retry(path: Path, max_retries: int = 5, delay: float = 0.5):
        """
        Remove a directory with retry logic for Windows file locking issues.
        
        Args:
            path: Path to directory to remove
            max_retries: Maximum number of retry attempts
            delay: Delay in seconds between retries
        """
        import os
        
        if not path.exists():
            return True
        
        is_windows = platform.system() == "Windows"
        
        for attempt in range(max_retries):
            try:
                # On Windows, try to remove read-only files first
                if is_windows:
                    # Remove read-only attribute from files before deletion
                    if path.is_dir():
                        try:
                            for root, dirs, files in os.walk(path):
                                for d in dirs:
                                    dir_path = os.path.join(root, d)
                                    try:
                                        os.chmod(dir_path, 0o777)
                                    except Exception:
                                        pass
                                for f in files:
                                    file_path = os.path.join(root, f)
                                    try:
                                        os.chmod(file_path, 0o777)
                                    except Exception:
                                        pass
                        except Exception:
                            pass
                
                shutil.rmtree(path)
                return True
                
            except (PermissionError, OSError) as e:
                if attempt < max_retries - 1:
                    wait_time = delay * (attempt + 1)  # Exponential backoff
                    if is_windows and attempt == 0:
                        # First retry: give Windows a bit more time to release locks
                        wait_time = 1.0
                    time.sleep(wait_time)
                    
                    # Try to remove read-only attributes again before retry
                    if is_windows and path.is_dir():
                        try:
                            for root, dirs, files in os.walk(path):
                                for f in files:
                                    file_path = os.path.join(root, f)
                                    try:
                                        os.chmod(file_path, 0o777)
                                    except Exception:
                                        pass
                        except Exception:
                            pass
                else:
                    # Last attempt failed - try Windows-specific command
                    if is_windows:
                        try:
                            # Use Windows rmdir command as last resort
                            result = os.system(f'rmdir /s /q "{path}"')
                            time.sleep(0.5)  # Wait for command to complete
                            if not path.exists():
                                return True
                        except Exception:
                            pass
                    raise e
        
        return False

    print("🚀 Starting new FastOpp project...")

    # Get the installed fastopp version
    try:
        package_version = version("fastopp")
        print(f"📦 Detected fastopp version: {package_version}")
    except Exception as e:
        print(f"⚠️ Could not detect fastopp version: {e}")
        package_version = None

    # Note: We allow git repositories since uv init creates them
    # Our copy technique works by cloning to a temp directory first

    # Check if current directory has non-uv files (allow uv init files)
    uv_files = {
        ".venv",
        "pyproject.toml",
        "uv.lock",
        "main.py",
        ".python-version",
        "README.md",
        ".git",
        ".gitignore",
    }
    existing_files = {
        item.name for item in Path(".").iterdir() if item.is_file() or item.is_dir()
    }
    non_uv_files = existing_files - uv_files

    if non_uv_files:
        print(f"❌ Current directory contains non-uv files: {', '.join(non_uv_files)}")
        print(
            "Please run this command in an empty directory or one with only uv files."
        )
        return False

    try:
        # Clone the repository to a temporary directory
        print("📥 Cloning FastOpp repository...")
        temp_dir = Path("fastopp-temp")
        subprocess.run(
            ["git", "clone", "https://github.com/Oppkey/fastopp.git", str(temp_dir)],
            check=True,
            capture_output=True,
            text=True,
        )

        print("✅ Repository cloned successfully")

        # Try to checkout the matching version tag
        if package_version:
            tag_name = f"v{package_version}"
            print(f"🏷️ Attempting to checkout tag: {tag_name}")

            try:
                # Try to checkout the exact version tag
                subprocess.run(
                    ["git", "checkout", tag_name],
                    cwd=temp_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                print(f"✅ Using template from tag: {tag_name}")
            except subprocess.CalledProcessError:
                # Tag doesn't exist, try to get latest release tag
                print(f"⚠️ Tag {tag_name} not found, looking for latest release...")

                try:
                    # Get the latest tag
                    result = subprocess.run(
                        ["git", "describe", "--tags", "--abbrev=0"],
                        cwd=temp_dir,
                        check=True,
                        capture_output=True,
                        text=True,
                    )

                    latest_tag = result.stdout.strip()
                    if latest_tag:
                        subprocess.run(
                            ["git", "checkout", latest_tag],
                            cwd=temp_dir,
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        print(f"✅ Using template from latest release: {latest_tag}")
                        print(
                            f"ℹ️ Note: {tag_name} not yet tagged, using stable release {latest_tag}"
                        )
                    else:
                        print("⚠️ No tags found, using main branch")
                except subprocess.CalledProcessError:
                    print("⚠️ Could not find any tags, using main branch")
        else:
            print("⚠️ No version detected, using main branch")

        # Give Windows time to release any file locks after git operations
        if platform.system() == "Windows":
            print("⏳ Waiting for file handles to release...")
            time.sleep(1.0)

        # Move files from temp directory to current directory
        print("📁 Moving files to current directory...")
        for item in temp_dir.iterdir():
            if item.name != ".git":  # Skip .git directory
                dest = Path(".") / item.name
                if dest.exists():
                    if dest.is_dir():
                        remove_directory_with_retry(dest)
                    else:
                        dest.unlink()
                shutil.move(str(item), str(dest))

        # Explicitly remove .git directory from temp before removing temp directory
        # This helps avoid Windows file locking issues
        git_dir = temp_dir / ".git"
        if git_dir.exists():
            print("🧹 Cleaning up temporary .git directory...")
            remove_directory_with_retry(git_dir)

        # Remove temp directory with retry logic
        print("🧹 Removing temporary directory...")
        if not remove_directory_with_retry(temp_dir):
            print("⚠️ Warning: Could not fully remove temporary directory")
            print(f"   You may need to manually delete: {temp_dir}")
        
        print("✅ Files moved successfully")

        # Remove .git directory to start fresh
        if Path(".git").exists():
            remove_directory_with_retry(Path(".git"))
            print("✅ Removed .git directory for fresh start")

        # Create new git repository
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from FastOpp template"], check=True
        )
        print("✅ Initialized new git repository")

        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Dependencies installed")

        # Create .env file
        env_content = """DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
OPENROUTER_API_KEY=your-openrouter-api-key-here
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file")

        # Initialize database
        print("🗄️ Initializing database...")
        subprocess.run(
            ["uv", "run", "python", "oppman.py", "migrate", "init"], check=True
        )
        subprocess.run(
            [
                "uv",
                "run",
                "python",
                "oppman.py",
                "migrate",
                "create",
                "Initial migration",
            ],
            check=True,
        )
        subprocess.run(
            ["uv", "run", "python", "oppman.py", "migrate", "upgrade"], check=True
        )
        print("✅ Database initialized")

        # Initialize demo data
        print("🎭 Setting up demo data...")
        subprocess.run(["uv", "run", "python", "oppdemo.py", "init"], check=True)
        print("✅ Demo data initialized")

        print("\n🎉 FastOpp project started successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your configuration")
        print("2. Run: uv run python oppman.py runserver")
        print("3. Visit: http://localhost:8000")
        print("4. Admin panel: http://localhost:8000/admin/")
        print("   - Email: admin@example.com")
        print("   - Password: admin123")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


# Export the main components
__all__ = ["app", "create_app", "startproject"]
