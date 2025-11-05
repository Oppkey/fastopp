#!/usr/bin/env python3
"""
Oppkey Management Tool (oppman.py)
Main entry point for FastOpp management commands.
"""
import argparse
import asyncio
import os
import sys

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import command modules
    # Simple environment variable configuration
    from dotenv import load_dotenv

    from scripts.check_env import check_environment
    from scripts.commands import database, project, server, users
    from scripts.emergency_access import main as emergency_access_main
    from scripts.generate_secrets import main as generate_secrets_main
    from scripts.help import show_help
    from scripts.migrate.cli import run_migrate_command, show_migration_help
    load_dotenv()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts/ directory")
    sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Oppkey Management Tool for FastAPI Admin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
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
            # Migration commands (Django-style)
            "makemigrations", "sqlmigrate", "showmigrations",
            # Core database and user management
            "db", "superuser", "check_users", "test_auth", "change_password", "list_users", "emergency",
            # Project management
            "clean"
        ],
        help="Command to execute"
    )
    
    parser.add_argument(
        "migrate_command",
        nargs="?",
        help="Migration subcommand (for 'migrate') or revision hash (for 'sqlmigrate')"
    )
    
    parser.add_argument(
        "migrate_args",
        nargs="*",
        help="Additional arguments for migration commands"
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
    
    # Handle database commands
    if args.command == "delete":
        # Delete database (with backup)
        database.delete_database()
        # Always attempt to backup and clean migrations regardless of DB deletion result
        database.backup_migrations()
        database.delete_migration_files()
        return
    
    if args.command == "backup":
        database.backup_database()
        return
    
    # Handle server commands
    if args.command == "runserver":
        server.run_server()
        return
    
    if args.command == "stopserver":
        server.stop_server()
        return
    
    if args.command == "production":
        server.run_production_server()
        return
    
    # Handle migration commands
    if args.command == "migrate":
        if not args.migrate_command:
            show_migration_help()
            return
        
        success = run_migrate_command(args.migrate_command, args.migrate_args)
        if not success:
            sys.exit(1)
        return
    
    # Handle Django-style migration commands
    if args.command == "makemigrations":
        success = run_migrate_command("makemigrations", args.migrate_args)
        if not success:
            sys.exit(1)
        return
    
    if args.command == "sqlmigrate":
        if not args.migrate_args:
            print("❌ Revision required for sqlmigrate")
            print("Usage: uv run python oppman.py sqlmigrate <revision>")
            sys.exit(1)
        success = run_migrate_command("sqlmigrate", args.migrate_args)
        if not success:
            sys.exit(1)
        return
    
    if args.command == "showmigrations":
        success = run_migrate_command("showmigrations", args.migrate_args)
        if not success:
            sys.exit(1)
        return
    
    # Handle environment commands
    if args.command == "env":
        check_environment()
        return
    
    if args.command == "secrets":
        try:
            generate_secrets_main()
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Make sure scripts/generate_secrets.py exists")
            sys.exit(1)
        return
    
    # Handle demo command
    if args.command == "demo":
        project.demo_command_help()
        return
    
    # Handle project commands
    if args.command == "clean":
        success = project.clean_project()
        if not success:
            sys.exit(1)
        return
    
    # Handle user management commands (async)
    core_commands = ["db", "superuser", "check_users", "test_auth", "change_password", "list_users"]
    
    # Handle emergency access command (non-async)
    if args.command == "emergency":
        emergency_access_main()
        return
    
    if args.command in core_commands:
        # Run async commands
        async def run_command():
            if args.command == "db":
                await users.run_init()
            elif args.command == "superuser":
                await users.run_superuser()
            elif args.command == "check_users":
                await users.run_check_users()
            elif args.command == "test_auth":
                await users.run_test_auth()
            elif args.command == "change_password":
                await users.run_change_password()
            elif args.command == "list_users":
                await users.run_list_users()
        
        # Run the async command
        asyncio.run(run_command())
        return


if __name__ == "__main__":
    main()
