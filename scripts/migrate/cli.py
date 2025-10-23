#!/usr/bin/env python3
"""
Migration CLI Interface
Provides command-line interface for migration management.
"""
import argparse
import sys
from typing import Optional, List

from .core import MigrationManager, setup_alembic_config


def run_migrate_command(command: str, args: Optional[List[str]] = None) -> bool:
    """Run a migration command"""
    manager = MigrationManager()
    
    if command == "init":
        success = manager.initialize()
        if success:
            # Auto-setup configuration after initialization
            setup_alembic_config()
        return success
    
    elif command == "create":
        if not args:
            message = input("Enter migration message: ")
        else:
            message = args[0]
        
        return manager.create_migration(message)
    
    elif command == "makemigrations":
        # Django-style makemigrations - prompt for optional message
        if not args:
            message = input("Enter migration message (optional, press Enter to skip): ").strip()
            if not message:
                message = "Auto-generated migration"
        else:
            message = args[0]
        
        return manager.create_migration(message)
    
    elif command == "upgrade":
        revision = args[0] if args else "head"
        return manager.upgrade(revision)
    
    elif command == "downgrade":
        if not args:
            print("❌ Revision required for downgrade")
            print("Usage: python oppman.py migrate downgrade <revision>")
            return False
        return manager.downgrade(args[0])
    
    elif command == "current":
        return manager.current()
    
    elif command == "history":
        verbose = "--verbose" in args if args else False
        return manager.history(verbose)
    
    elif command == "show":
        revision = args[0] if args else "head"
        return manager.show(revision)
    
    elif command == "stamp":
        revision = args[0] if args else "head"
        return manager.stamp(revision)
    
    elif command == "check":
        return manager.check()
    
    elif command == "setup":
        return setup_alembic_config()
    
    elif command == "sqlmigrate":
        if not args:
            print("❌ Revision required for sqlmigrate")
            print("Usage: uv run python oppman.py sqlmigrate <revision>")
            return False
        return manager.sqlmigrate(args[0])
    
    elif command == "showmigrations":
        return manager.show_migrations()
    
    else:
        print(f"❌ Unknown migration command: {command}")
        return False


def show_migration_help():
    """Show migration help information"""
    help_text = """
Migration Management Commands

USAGE:
    # Django-style commands (recommended)
    python oppman.py makemigrations [message]
    python oppman.py migrate
    python oppman.py sqlmigrate <revision>
    python oppman.py showmigrations
    
    # Alembic-style commands (also available)
    python oppman.py migrate <command> [options]

DJANGO-STYLE COMMANDS:
    makemigrations    Create a new migration (prompts for optional message)
    migrate          Apply all pending migrations
    sqlmigrate       Show SQL statements for a specific migration
    showmigrations  Show all migrations with applied status [X] applied, [ ] pending

ALEMBIC-STYLE COMMANDS:
    init        Initialize Alembic in the project (first time setup)
    setup       Update Alembic configuration files
    create      Create a new migration (with message)
    upgrade     Upgrade database to latest revision (or specified)
    downgrade   Downgrade database to specified revision
    current     Show current database revision
    history     Show migration history
    show        Show details of a specific migration
    stamp       Mark database as being at a specific revision
    check       Check if database is up to date

EXAMPLES:
    # Django-style workflow (recommended)
    python oppman.py makemigrations                    # Create migration (prompts for message)
    python oppman.py migrate                           # Apply migrations
    python oppman.py sqlmigrate abc123def             # Show SQL for migration
    python oppman.py showmigrations                   # Show migration status
    
    # Alembic-style workflow (also available)
    python oppman.py migrate init                      # First time setup
    python oppman.py migrate create "Add user table"  # Create migration
    python oppman.py migrate upgrade                  # Apply migrations
    python oppman.py migrate current                   # Check status
    python oppman.py migrate history                  # View history

WORKFLOW:
    1. Initialize: python oppman.py migrate init
    2. Add models to models.py
    3. Create migration: python oppman.py makemigrations (or migrate create "Description")
    4. Apply migration: python oppman.py migrate (or migrate upgrade)
    5. Repeat steps 2-4 for new changes

TROUBLESHOOTING:
    - If migrations fail, check alembic.ini and alembic/env.py
    - Use 'python oppman.py migrate setup' to fix configuration
    - Use 'python oppman.py migrate check' to verify status
    """
    print(help_text)


def main():
    """Main entry point for migration CLI"""
    parser = argparse.ArgumentParser(
        description="Migration Management for FastAPI Admin",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "init", "setup", "create", "upgrade", "downgrade",
            "current", "history", "show", "stamp", "check", "help"
        ],
        help="Migration command to execute"
    )
    
    parser.add_argument(
        "args",
        nargs="*",
        help="Additional arguments for the command"
    )
    
    args = parser.parse_args()
    
    # Handle help command
    if not args.command or args.command == "help":
        show_migration_help()
        return
    
    # Run the migration command
    success = run_migrate_command(args.command, args.args)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()