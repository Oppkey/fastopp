"""
Project management commands for oppman.py

This module provides project cleanup and setup functionality.
"""

from .cleanup import (
    backup_remaining_files,
    run_destroy_step,
    show_cleanup_preview,
)
from .wizard import run_setup_wizard


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
    print(
        "   uv run python oppdemo.py clear_registrants # Clear and add fresh registrants"
    )
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


def clean_project():
    """Clean project by first running oppdemo.py destroy, then moving remaining files to backup"""
    # Step 1: Show preview and get confirmation
    confirmed, existing_items = show_cleanup_preview()
    if not confirmed:
        return False

    if not existing_items:
        # User cancelled or no items to clean
        return True

    # Step 2: Run oppdemo.py destroy
    if not run_destroy_step():
        return False

    # Step 3: Backup remaining files
    failed_count = backup_remaining_files(existing_items)

    # Step 4: Run setup wizard
    run_setup_wizard()

    return failed_count == 0
