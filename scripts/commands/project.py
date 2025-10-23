#!/usr/bin/env python3
"""
Project management commands for oppman.py
"""
import shutil
import subprocess
import re
from datetime import datetime
from pathlib import Path


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


def clean_project():
    """Clean project by first running oppdemo.py destroy, then moving remaining files to backup"""
    # Files and directories to move to backup (after destroy)
    files_to_clean = [
        "demo_assets",
        "base_assets", 
        "scripts/demo",
        "docs",
        "tests",
        "oppdemo.py",
        "pytest.ini",
        "LICENSE",
        "fastopp",
        "README.md"
    ]
    
    # Show initial confirmation prompt
    print("🧹 FastOpp Project Cleanup")
    print("=" * 50)
    print("This will perform a three-step cleanup process:")
    print()
    print("1️⃣  First: Run 'oppdemo.py destroy' to switch to minimal app")
    print("2️⃣  Then: Move remaining files to backup location")
    print("3️⃣  Finally: Interactive project setup wizard")
    print()
    print("Files that will be moved to backup after destroy:")
    print()
    
    # Check which files/directories exist
    existing_items = []
    for item in files_to_clean:
        path = Path(item)
        if path.exists():
            existing_items.append(item)
            if path.is_dir():
                print(f"  📁 {item}/ (directory)")
            else:
                print(f"  📄 {item} (file)")
    
    if not existing_items:
        print("ℹ️  No files to clean - all specified files/directories are already missing")
        return True
    
    print()
    print("⚠️  WARNING: This will switch to minimal app mode and move files to backup!")
    print("💡 Files will be preserved in the backup directory")
    print()
    
    # Get user confirmation
    while True:
        response = input("Do you want to proceed with cleanup? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            break
        elif response in ['no', 'n']:
            print("❌ Cleanup cancelled by user")
            return False
        else:
            print("Please enter 'yes' or 'no'")
    
    # Step 1: Run oppdemo.py destroy
    print("\n1️⃣  Running 'oppdemo.py destroy' to switch to minimal app...")
    try:
        result = subprocess.run([
            "uv", "run", "python", "oppdemo.py", "destroy"
        ], check=True, capture_output=True, text=True)
        print("✅ oppdemo.py destroy completed successfully")
        if result.stdout:
            print("📋 Destroy output:")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run oppdemo.py destroy: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error running oppdemo.py destroy: {e}")
        return False
    
    # Step 2: Create backup directory and move remaining files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups") / "clean" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n2️⃣  Moving remaining files to backup: {backup_dir}")
    
    # Re-check which files still exist after destroy
    remaining_items = []
    for item in files_to_clean:
        path = Path(item)
        if path.exists():
            remaining_items.append(item)
    
    if not remaining_items:
        print("ℹ️  No remaining files to move after destroy")
        print("\n🎉 Project cleanup completed successfully!")
        print("Your project is now ready to be used as a base for new applications.")
        return True
    
    # Move remaining files and directories to backup
    moved_count = 0
    failed_count = 0
    
    for item in remaining_items:
        source_path = Path(item)
        backup_path = backup_dir / item
        
        try:
            if source_path.is_dir():
                shutil.move(str(source_path), str(backup_path))
                print(f"✅ Moved directory: {item}/")
            else:
                shutil.move(str(source_path), str(backup_path))
                print(f"✅ Moved file: {item}")
            moved_count += 1
        except Exception as e:
            print(f"❌ Failed to move {item}: {e}")
            failed_count += 1
    
    # Summary
    print("\n📊 Cleanup Summary:")
    print(f"  ✅ Successfully moved: {moved_count} items")
    if failed_count > 0:
        print(f"  ❌ Failed to move: {failed_count} items")
    
    if failed_count == 0:
        print("\n🎉 Project cleanup completed successfully!")
        print(f"📦 Files backed up to: {backup_dir}")
        print("Your project is now ready to be used as a base for new applications.")
    else:
        print(f"\n⚠️  Cleanup completed with {failed_count} errors.")
        print("Some files may still need manual cleanup.")
    
    # Step 3: Interactive project setup wizard
    print("\n3️⃣  Setting up new project configuration...")
    project_name = input("Enter project name (press Enter for 'my_fastopp_project'): ").strip() or "my_fastopp_project"
    author_name = input("Enter author name (press Enter for 'Your Name'): ").strip() or "Your Name"
    description = input("Enter project description (press Enter for 'A new FastOpp project'): ").strip() or "A new FastOpp project"
    
    # Delete README.md (it was already moved to backup)
    readme_path = Path("README.md")
    if readme_path.exists():
        readme_path.unlink()
        print("✅ Deleted README.md")
    
    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text()
        # Replace fields
        content = re.sub(r'name = ".*?"', f'name = "{project_name}"', content)
        content = re.sub(r'version = ".*?"', 'version = "0.1.0"', content)
        content = re.sub(r'\{name = ".*?"\}', f'{{name = "{author_name}"}}', content)
        content = re.sub(r'description = ".*?"', f'description = "{description}"', content)
        pyproject_path.write_text(content)
        print("✅ Updated pyproject.toml")
    
    # Create new README.md
    new_readme = f"""# {project_name}

{description}

## Author

{author_name}

## Setup

This project is built with FastOpp.

### Installation

```bash
uv sync
```

### Initialize Database

```bash
uv run python oppman.py migrate init
uv run python oppman.py makemigrations
uv run python oppman.py migrate
```

### Run Development Server

```bash
uv run python oppman.py runserver
```

Visit http://localhost:8000
"""
    Path("README.md").write_text(new_readme)
    print("✅ Created new README.md")
    
    return failed_count == 0
