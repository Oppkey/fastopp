"""
File cleanup and backup operations for project management
"""

from datetime import datetime
from pathlib import Path
import shutil
import subprocess

# Files and directories to move to backup (after destroy)
FILES_TO_CLEAN = [
    "demo_assets",
    "base_assets",
    "scripts/demo",
    "docs",
    "tests",
    "blog",
    "oppdemo.py",
    "pytest.ini",
    "LICENSE",
    "fastopp",
    "README.md",
    ".github",
    ".cursor",
    ".git",
]


def show_cleanup_preview():
    """Show what will be cleaned and get confirmation"""
    print("🧹 FastOpp Project Cleanup")
    print("=" * 50)
    print("This will perform a three-step cleanup process:")
    print()
    print("1️⃣  First: Run 'oppdemo.py destroy' to switch to minimal app")
    print("2️⃣  Then: Move remaining files to backup location")
    print("3️⃣  Finally: Interactive project setup wizard")
    print()
    print("Files that will be moved to backup after destroy:")
    print(
        "(Migration files will be moved but alembic/versions directory structure preserved)"
    )
    print()

    # Check which files/directories exist
    existing_items = []
    for item in FILES_TO_CLEAN:
        path = Path(item)
        if path.exists():
            existing_items.append(item)
            if path.is_dir():
                print(f"  📁 {item}/ (directory)")
            else:
                print(f"  📄 {item} (file)")

    if not existing_items:
        print(
            "ℹ️  No files to clean - all specified files/directories are already missing"
        )
        return False, []

    print()
    print("⚠️  WARNING: This will switch to minimal app mode and move files to backup!")
    print("💡 Files will be preserved in the backup directory")
    print(
        "🔧 This includes project metadata (.git, .github, .cursor) for a fresh start"
    )
    print()

    # Get user confirmation
    while True:
        response = (
            input("Do you want to proceed with cleanup? (yes/no): ").strip().lower()
        )
        if response in ["yes", "y"]:
            return True, existing_items
        elif response in ["no", "n"]:
            print("❌ Cleanup cancelled by user")
            return False, []
        else:
            print("Please enter 'yes' or 'no'")


def run_destroy_step():
    """Run oppdemo.py destroy subprocess"""
    print("\n1️⃣  Running 'oppdemo.py destroy' to switch to minimal app...")
    try:
        result = subprocess.run(
            ["uv", "run", "python", "oppdemo.py", "destroy"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("✅ oppdemo.py destroy completed successfully")
        if result.stdout:
            print("📋 Destroy output:")
            print(result.stdout)
        return True
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


def backup_remaining_files(existing_items):
    """Backup remaining files after destroy step"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups") / "clean" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n2️⃣  Moving remaining files to backup: {backup_dir}")

    # Re-check which files still exist after destroy
    remaining_items = []
    for item in existing_items:
        path = Path(item)
        if path.exists():
            remaining_items.append(item)

    if not remaining_items:
        print("ℹ️  No remaining files to move after destroy")
        print("\n🎉 Project cleanup completed successfully!")
        print("Your project is now ready to be used as a base for new applications.")
        return 0  # No failures

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

    # Special handling for alembic/versions directory
    failed_count += handle_migration_cleanup(backup_dir)

    if failed_count == 0:
        print("\n🎉 Project cleanup completed successfully!")
        print(f"📦 Files backed up to: {backup_dir}")
        print("Your project is now ready to be used as a base for new applications.")
    else:
        print(f"\n⚠️  Cleanup completed with {failed_count} errors.")
        print("Some files may still need manual cleanup.")

    return failed_count


def handle_migration_cleanup(backup_dir):
    """Handle alembic migration file cleanup while preserving directory structure"""
    print("\n🗄️  Cleaning up migration files while preserving directory structure...")
    alembic_versions_dir = Path("alembic/versions")
    failed_count = 0

    if not alembic_versions_dir.exists():
        print("  ℹ️  alembic/versions directory not found")
        return failed_count

    # Create alembic backup subdirectory
    alembic_backup_dir = backup_dir / "alembic" / "versions"
    alembic_backup_dir.mkdir(parents=True, exist_ok=True)

    # Move all files in alembic/versions to backup (but keep the directory)
    migration_files_moved = 0
    for item in alembic_versions_dir.iterdir():
        if item.is_file():  # Only move files, not subdirectories like __pycache__
            try:
                backup_path = alembic_backup_dir / item.name
                shutil.move(str(item), str(backup_path))
                print(f"  ✅ Moved migration file: {item.name}")
                migration_files_moved += 1
            except Exception as e:
                print(f"  ❌ Failed to move {item.name}: {e}")
                failed_count += 1

    if migration_files_moved > 0:
        print(f"  📦 Moved {migration_files_moved} migration files to backup")
        print("  🔧 Preserved empty alembic/versions directory for new migrations")
    else:
        print("  ℹ️  No migration files found in alembic/versions")

    # Clean up __pycache__ directories in alembic/versions
    pycache_dir = alembic_versions_dir / "__pycache__"
    if pycache_dir.exists() and pycache_dir.is_dir():
        try:
            shutil.rmtree(str(pycache_dir))
            print("  🧹 Cleaned up __pycache__ directory in alembic/versions")
        except Exception as e:
            print(f"  ❌ Failed to clean __pycache__ directory: {e}")
            failed_count += 1

    return failed_count
