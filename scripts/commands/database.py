#!/usr/bin/env python3
"""
Database management commands for oppman.py
"""
from datetime import datetime
from pathlib import Path
import shutil


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
