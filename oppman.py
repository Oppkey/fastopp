#!/usr/bin/env python3
"""
Oppkey Management Tool (oppman.py)
A core tool for managing database migrations, user management, and application setup.
Demo commands have been moved to oppdemo.py for better separation of concerns.
"""
import argparse
import asyncio
import os
import shutil
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Core management scripts only (demo scripts moved to oppdemo.py)
    from scripts.migrate.cli import run_migrate_command, show_migration_help
    from scripts.check_env import check_environment
    # Core database and user management scripts
    from scripts.init_db import init_db
    from scripts.create_superuser import create_superuser
    from scripts.check_users import check_users
    from scripts.test_auth import test_auth
    from scripts.change_password import list_users, change_password_interactive
    from scripts.emergency_access import main as emergency_access_main
    from dependencies.config import get_settings
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts/ directory")
    sys.exit(1)


def backup_database():
    """Backup the current database with timestamp"""
    db_path = Path("test.db")
    if not db_path.exists():
        print("❌ No database file found to backup")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(f"test.db.{timestamp}")
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to backup database: {e}")
        return False


def demo_command_help():
    """Show help message for demo commands that have been moved to oppdemo.py"""
    print("🔄 Demo commands have been moved to a new file: oppdemo.py")
    print()
    print("📋 Available demo file management commands:")
    print("   uv run python oppdemo.py save      # Save demo files")
    print("   uv run python oppdemo.py restore   # Restore demo files")
    print("   uv run python oppdemo.py destroy   # Switch to minimal app")
    print("   uv run python oppdemo.py diff      # Show differences")
    print("   uv run python oppdemo.py backups   # List all backups")
    print()
    print("📊 Available demo data initialization commands:")
    print("   uv run python oppdemo.py init      # Full initialization")
    print("   uv run python oppdemo.py db        # Initialize database only")
    print("   uv run python oppdemo.py superuser # Create superuser only")
    print("   uv run python oppdemo.py users     # Add test users only")
    print("   uv run python oppdemo.py products  # Add sample products only")
    print("   uv run python oppdemo.py webinars  # Add sample webinars only")
    print("   uv run python oppdemo.py download_photos  # Download sample photos")
    print("   uv run python oppdemo.py registrants      # Add sample registrants")
    print("   uv run python oppdemo.py clear_registrants # Clear and add fresh registrants")
    print("   uv run python oppdemo.py check_users      # Check existing users")
    print("   uv run python oppdemo.py test_auth        # Test authentication")
    print("   uv run python oppdemo.py change_password  # Change user password")
    print("   uv run python oppdemo.py list_users       # List all users")
    print()
    print("💡 For more information:")
    print("   uv run python oppdemo.py help")
    print()
    print("🔧 oppman.py now focuses on core database and application management.")
    print("📚 oppdemo.py handles all demo-related functionality.")


def delete_database():
    """Delete the current database file"""
    db_path = Path("test.db")
    if not db_path.exists():
        print("❌ No database file found to delete")
        return False

    try:
        # Backup first
        if backup_database():
            db_path.unlink()
            print("✅ Database deleted successfully")
            return True
        else:
            print("❌ Failed to backup database, not deleting")
            return False
    except Exception as e:
        print(f"❌ Failed to delete database: {e}")
        return False


def backup_migrations() -> Path | None:
    """Backup Alembic migration files (alembic/versions) to a timestamped directory."""
    versions_dir = Path("alembic") / "versions"
    if not versions_dir.exists():
        print("❌ No alembic/versions directory found to backup")
        return None

    migration_files = [p for p in versions_dir.glob("*.py") if p.is_file()]
    if not migration_files:
        print("ℹ️  No migration files found to backup")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = Path("alembic") / f"versions_backup_{timestamp}"
    backup_root.mkdir(parents=True, exist_ok=True)

    try:
        for migration_file in migration_files:
            shutil.copy2(migration_file, backup_root / migration_file.name)
        print(f"✅ Migrations backed up to: {backup_root}")
        return backup_root
    except Exception as e:
        print(f"❌ Failed to backup migrations: {e}")
        return None


def delete_migration_files() -> bool:
    """Delete all Alembic migration .py files from alembic/versions and clean __pycache__."""
    versions_dir = Path("alembic") / "versions"
    if not versions_dir.exists():
        print("❌ No alembic/versions directory found")
        return False

    migration_files = [p for p in versions_dir.glob("*.py") if p.is_file()]
    if not migration_files:
        print("ℹ️  No migration files to delete")
        # Still attempt to remove __pycache__ if present
        pycache_dir = versions_dir / "__pycache__"
        if pycache_dir.exists():
            try:
                shutil.rmtree(pycache_dir)
                print("🧹 Removed alembic/versions/__pycache__")
            except Exception as e:
                print(f"⚠️  Failed to remove __pycache__: {e}")
        return True

    try:
        for migration_file in migration_files:
            migration_file.unlink()
        print("✅ Deleted migration files from alembic/versions")
        # Clean __pycache__ as well
        pycache_dir = versions_dir / "__pycache__"
        if pycache_dir.exists():
            try:
                shutil.rmtree(pycache_dir)
                print("🧹 Removed alembic/versions/__pycache__")
            except Exception as e:
                print(f"⚠️  Failed to remove __pycache__: {e}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete migration files: {e}")
        return False


# Core database and user management functions
async def run_init():
    """Initialize a new database"""
    print("🔄 Initializing database...")
    await init_db()
    print("✅ Database initialization complete")


async def run_superuser():
    """Create superuser"""
    print("🔄 Creating superuser...")
    await create_superuser()
    print("✅ Superuser creation complete")


async def run_check_users():
    """Check existing users and their permissions"""
    print("🔄 Checking users...")
    await check_users()
    print("✅ User check complete")


async def run_test_auth():
    """Test the authentication system"""
    print("🔄 Testing authentication system...")
    await test_auth()
    print("✅ Authentication test complete")


async def run_change_password():
    """Change user password interactively"""
    print("🔐 Changing user password...")
    await change_password_interactive()


async def run_list_users():
    """List all users"""
    print("👥 Listing users...")
    await list_users()


def run_emergency_access():
    """Generate emergency access token"""
    print("🚨 Generating emergency access token...")
    emergency_access_main()


def run_server():
    """Start the development server with uvicorn"""
    settings = get_settings()
    print("🚀 Starting development server...")
    print(f"📡 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"🔧 Admin panel: http://{settings.host}:{settings.port}/admin/")
    print(f"📚 API docs: http://{settings.host}:{settings.port}/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start uvicorn with reload
        subprocess.run([
            "uv", "run", "python", "-m", "uvicorn", "main:app", "--reload", 
            "--host", settings.host, "--port", str(settings.port)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def stop_server():
    """Stop the development server"""
    print("🛑 Stopping development server...")
    
    try:
        # Kill uvicorn processes
        result = subprocess.run([
            "pkill", "-f", "uv run uvicorn main:app"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Development server stopped successfully")
            return True
        else:
            print("ℹ️  No development server found running")
            return True
    except Exception as e:
        print(f"❌ Failed to stop server: {e}")
        return False


def run_production_server():
    """Start the production server with Gunicorn"""
    settings = get_settings()
    print("🚀 Starting FastAPI production server...")
    print(f"📡 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"🔧 Admin panel: http://{settings.host}:{settings.port}/admin/")
    print(f"📚 API docs: http://{settings.host}:{settings.port}/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start gunicorn with uvicorn workers
        subprocess.run([
            "uv", "run", "gunicorn",
            "main:app",
            "-w", "4",  # 4 workers
            "-k", "uvicorn.workers.UvicornWorker",
            "--bind", f"{settings.host}:{settings.port}",
            "--timeout", "120",
            "--keep-alive", "5",
            "--max-requests", "1000",
            "--max-requests-jitter", "50"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        print("Make sure asyncpg and gunicorn are installed: uv add asyncpg gunicorn")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def show_help():
    """Show detailed help information"""
    help_text = """
Oppkey Management Tool (oppman.py)

A core tool for managing database migrations, user management, and application setup.
Similar to Django's manage.py, this tool focuses on core application management.
Demo commands have been moved to oppdemo.py for better separation of concerns.

USAGE:
    uv run python oppman.py <command> [options]

COMMANDS:
    # Core application management
    runserver   Start development server with uvicorn --reload
    stopserver  Stop development server
    production  Start production server with Gunicorn (no Nginx)
    
    # Database management
    delete      Delete current database (with backup)
    backup      Backup current database
    migrate     Database migration management (see examples below)
    db          Initialize database (creates all tables)
    
    # User management
    superuser   Create superuser account
    check_users Check existing users and their permissions
    test_auth   Test the authentication system
    change_password Change user password interactively
    list_users  List all users in the database
    emergency   Generate emergency access token for password recovery
    
    # Environment and utilities
    env         Check environment configuration
    secrets     Generate SECRET_KEY for .env file
    demo        Demo commands have been moved to oppdemo.py
    help        Show this help message
    

EXAMPLES:
    # Core application management
    uv run python oppman.py runserver      # Start development server
    uv run python oppman.py stopserver     # Stop development server
    uv run python oppman.py production     # Start production server
    
    # Database management
    uv run python oppman.py db             # Initialize database (creates all tables)
    uv run python oppman.py backup         # Backup database
    uv run python oppman.py delete         # Delete database (with backup)
    uv run python oppman.py migrate init   # Initialize migrations
    uv run python oppman.py migrate create "Add new table"  # Create migration
    uv run python oppman.py migrate upgrade  # Apply migrations
    uv run python oppman.py migrate current  # Show current migration
    
    # User management
    uv run python oppman.py superuser      # Create superuser
    uv run python oppman.py check_users    # Check existing users
    uv run python oppman.py test_auth      # Test authentication
    uv run python oppman.py change_password # Change user password
    uv run python oppman.py list_users     # List all users
    uv run python oppman.py emergency      # Generate emergency access token
    
    # Environment management
    uv run python oppman.py env            # Check environment configuration
    uv run python oppman.py secrets        # Generate SECRET_KEY for .env file
    
    # Demo file management (use oppdemo.py)
    uv run python oppdemo.py save          # Save demo files
    uv run python oppdemo.py restore       # Restore demo files
    uv run python oppdemo.py destroy       # Switch to minimal app
    uv run python oppdemo.py diff          # Show differences

IMPORTANT NOTES:
    - oppman.py: Core application management (database, users, migrations)
    - oppdemo.py: Demo-specific commands (init, products, webinars, file management)
    - Both have 'db' and 'superuser' commands - use either one
    - Emergency access is only available in oppman.py

DEFAULT CREDENTIALS:
    Superuser: admin@example.com / admin123
    Test Users: test123 (for all test users)
    
    Test Users Created:
    - admin@example.com (superuser, admin)
    - admin2@example.com (superuser, admin)
    - john@example.com (staff, marketing)
    - jane@example.com (staff, sales)
    - staff@example.com (staff, support)
    - marketing@example.com (staff, marketing)
    - sales@example.com (staff, sales)
    - bob@example.com (inactive)

PERMISSION LEVELS:
    - Superusers: Full admin access (users + products + webinars + audit)
    - Marketing: Product management + webinar management
    - Sales: Product management + assigned webinar viewing
    - Support: Product management only
    - Regular users: No admin access

PASSWORD MANAGEMENT:
    - change_password: Interactive password change for any user
    - list_users: View all users and their status
    - Usage: uv run python oppdemo.py change_password
    - Direct script: uv run python scripts/change_password.py --email user@example.com --password newpass

WEBINAR REGISTRANTS:
    - Access: http://localhost:8000/webinar-registrants
    - Login required: Staff or admin access
    - Features: Photo upload, registrant management
    - Sample data: 5 registrants with professional photos
    - Commands: Use oppdemo.py for all demo-related functionality

DATABASE:
    - Development: SQLite (test.db)
    - Backup format: test.db.YYYYMMDD_HHMMSS
    - Base Assets Mode: Only creates 'users' table (minimal setup)
    - Full Mode: Creates all tables (users, products, webinar_registrants, audit_logs)

SERVER:
    - Development server: http://localhost:8000
    - Admin panel: http://localhost:8000/admin/
    - API docs: http://localhost:8000/docs
    - Webinar registrants: http://localhost:8000/webinar-registrants

SECURITY & ENVIRONMENT SETUP:
    🔐 SECRET_KEY Generation:
       uv run python oppman.py secrets      # Generate secure SECRET_KEY
       # Add the output to your .env file
    
    ⚠️  CRITICAL SECURITY WARNINGS:
       - NEVER commit .env files to version control
       - Add .env to your .gitignore file
       - Keep your SECRET_KEY secure and private
       - Use different SECRET_KEYs for different environments
       - The .env file should NEVER be committed to GitHub
    
    📁 Required .env file structure:
       SECRET_KEY=your_generated_secret_key_here
       DATABASE_URL=sqlite:///./test.db
       # Add other environment variables as needed

NOTE: All demo-related functionality has been moved to oppdemo.py.
Use 'uv run python oppdemo.py <command>' for demo data initialization and management.
    """
    print(help_text)


def startproject():
    """Start a new FastOpp project with full structure from GitHub"""
    import subprocess
    import shutil
    from pathlib import Path
    
    print("🚀 Starting new FastOpp project...")
    
    # Note: We allow git repositories since uv init creates them
    # Our copy technique works by cloning to a temp directory first
    
    # Check if current directory has non-uv files (allow uv init files)
    uv_files = {".venv", "pyproject.toml", "uv.lock", "main.py", ".python-version", "README.md", ".git", ".gitignore"}
    existing_files = {item.name for item in Path(".").iterdir() if item.is_file() or item.is_dir()}
    non_uv_files = existing_files - uv_files
    
    if non_uv_files:
        print(f"❌ Current directory contains non-uv files: {', '.join(non_uv_files)}")
        print("Please run this command in an empty directory or one with only uv files.")
        return False
    
    try:
        # Clone the repository to a temporary directory
        print("📥 Cloning FastOpp repository...")
        temp_dir = Path("fastopp-temp")
        subprocess.run([
            "git", "clone", 
            "https://github.com/Oppkey/fastopp.git",
            str(temp_dir)
        ], check=True, capture_output=True, text=True)
        
        print("✅ Repository cloned successfully")
        
        # Move files from temp directory to current directory
        print("📁 Moving files to current directory...")
        for item in temp_dir.iterdir():
            if item.name != ".git":  # Skip .git directory
                dest = Path(".") / item.name
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                shutil.move(str(item), str(dest))
        
        # Remove temp directory
        shutil.rmtree(temp_dir)
        print("✅ Files moved successfully")
        
        # Remove .git directory to start fresh
        if Path(".git").exists():
            shutil.rmtree(".git")
            print("✅ Removed .git directory for fresh start")
        
        # Create new git repository
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from FastOpp template"], check=True)
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
        subprocess.run(["uv", "run", "python", "oppman.py", "migrate", "init"], check=True)
        subprocess.run(["uv", "run", "python", "oppman.py", "migrate", "create", "Initial migration"], check=True)
        subprocess.run(["uv", "run", "python", "oppman.py", "migrate", "upgrade"], check=True)
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


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Oppkey Management Tool for FastAPI Admin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python oppman.py startproject  # Start new FastOpp project from GitHub
  uv run python oppman.py db            # Initialize database only
  uv run python oppman.py delete        # Delete database with backup
  uv run python oppdemo.py init         # Full initialization with sample data
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            # Core application management
            "runserver", "stopserver", "production", "delete", "backup", "migrate", "env", "secrets", "help", "demo",
            # Core database and user management
            "startproject", "db", "superuser", "check_users", "test_auth", "change_password", "list_users", "emergency"
        ],
        help="Command to execute"
    )
    
    parser.add_argument(
        "migrate_command",
        nargs="?",
        help="Migration subcommand (use with 'migrate')"
    )
    
    parser.add_argument(
        "migrate_args",
        nargs="*",
        help="Additional arguments for migration command"
    )
    
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        show_help()
        return
    
    # Handle help command
    if args.command == "help":
        show_help()
        return
    
    # Handle non-async commands
    if args.command == "delete":
        # Delete database (with backup)
        delete_database()
        # Always attempt to backup and clean migrations regardless of DB deletion result
        backup_migrations()
        delete_migration_files()
        return
    
    if args.command == "backup":
        backup_database()
        return
    
    if args.command == "demo":
        demo_command_help()
        return
    
    if args.command == "runserver":
        run_server()
        return
    
    if args.command == "stopserver":
        stop_server()
        return
    
    if args.command == "production":
        run_production_server()
        return
    
    if args.command == "migrate":
        if not args.migrate_command:
            show_migration_help()
            return
        
        success = run_migrate_command(args.migrate_command, args.migrate_args)
        if not success:
            sys.exit(1)
        return
    
    if args.command == "env":
        check_environment()
        return
    
    if args.command == "secrets":
        # Import and run the secrets generation
        try:
            from scripts.generate_secrets import main as generate_secrets_main
            generate_secrets_main()
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Make sure scripts/generate_secrets.py exists")
            sys.exit(1)
        return
    
    # Handle init command with redirect message
    if args.command == "init":
        print("🔄 The 'init' command has been moved to oppdemo.py for better organization.")
        print()
        print("📊 To initialize the database and load with sample data, use:")
        print("   uv run python oppdemo.py init")
        print()
        print("💡 This will:")
        print("   - Initialize the database")
        print("   - Create a superuser (admin@example.com / admin123)")
        print("   - Add test users")
        print("   - Add sample products and webinars")
        print("   - Download sample photos")
        print("   - Add webinar registrants with photos")
        print()
        print("🔧 For database-only initialization, use:")
        print("   uv run python oppman.py db")
        return
    
    # Handle core database and user management commands
    core_commands = ["db", "superuser", "check_users", "test_auth", "change_password", "list_users"]
    
    # Handle emergency access command (non-async)
    if args.command == "emergency":
        run_emergency_access()
        return
    
    if args.command == "startproject":
        # Start new project
        success = startproject()
        if not success:
            sys.exit(1)
        return
    
    if args.command in core_commands:
        # Run async commands
        async def run_command():
            if args.command == "db":
                await run_init()
            elif args.command == "superuser":
                await run_superuser()
            elif args.command == "check_users":
                await run_check_users()
            elif args.command == "test_auth":
                await run_test_auth()
            elif args.command == "change_password":
                await run_change_password()
            elif args.command == "list_users":
                await run_list_users()
        
        # Run the async command
        asyncio.run(run_command())
        return


if __name__ == "__main__":
    main()
