#!/usr/bin/env python3
"""
Help text for oppman.py
"""


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
    makemigrations  Create new migration (Django-style)
    sqlmigrate  Show SQL for a migration (Django-style)
    showmigrations  Show migration status (Django-style)
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
    clean       DANGER: delete all demo files
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
    uv run python oppman.py makemigrations # Create migration (Django-style)
    uv run python oppman.py migrate        # Apply migrations (Django-style)
    uv run python oppman.py sqlmigrate abc123def  # Show SQL for migration
    uv run python oppman.py showmigrations # Show migration status
    
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
    uv run python oppman.py clean          # Run destroy then move remaining files to backup
    
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
