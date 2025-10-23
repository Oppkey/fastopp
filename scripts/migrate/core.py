#!/usr/bin/env python3
"""
Migration Management Core
Handles Alembic migrations for the FastAPI application.
"""
import os
import subprocess
import glob
from pathlib import Path
from typing import Optional, List, Tuple


class MigrationManager:
    """Manages database migrations using Alembic"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.alembic_dir = self.project_root / "alembic"
        self.alembic_ini = self.project_root / "alembic.ini"
        
    def _run_alembic_command(self, command: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """Run an alembic command and return (return_code, stdout, stderr)"""
        try:
            result = subprocess.run(
                ["alembic"] + command,
                capture_output=capture_output,
                text=True,
                cwd=self.project_root
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            return 1, "", "Alembic not found. Install with: uv add alembic"
        except Exception as e:
            return 1, "", f"Error running alembic: {e}"
    
    def is_initialized(self) -> bool:
        """Check if Alembic is initialized in this project"""
        return self.alembic_dir.exists() and self.alembic_ini.exists()
    
    def initialize(self) -> bool:
        """Initialize Alembic in the project"""
        if self.is_initialized():
            print("ℹ️  Alembic already initialized")
            return True

        print("🔄 Initializing Alembic...")
        return_code, stdout, stderr = self._run_alembic_command(["init", "alembic"])

        if return_code == 0:
            print("✅ Alembic initialized successfully")
            if stdout:
                print(stdout.strip())
            print("📝 Next steps:")
            print("   1. Update alembic.ini with your database URL")
            print("   2. Update alembic/env.py to import your models")
            print("   3. Run: python oppman.py migrate create")
            return True
        else:
            print(f"❌ Failed to initialize Alembic: {stderr}")
            return False
    
    def create_migration(self, message: str) -> bool:
        """Create a new migration"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False

        print(f"🔄 Creating migration: {message}")
        return_code, stdout, stderr = self._run_alembic_command([
            "revision", "--autogenerate", "-m", message
        ])

        if return_code == 0:
            print("✅ Migration created successfully")
            if stdout:
                print(stdout.strip())
            # Post-process the generated migration file to add sqlmodel import
            self._fix_migration_imports()
            return True
        else:
            print(f"❌ Failed to create migration: {stderr}")
            return False

    def _fix_migration_imports(self):
        """Fix sqlmodel imports in the latest migration file"""
        try:
            # Find the latest migration file
            versions_dir = self.project_root / "alembic" / "versions"
            migration_files = glob.glob(str(versions_dir / "*.py"))

            if not migration_files:
                return

            # Get the most recent migration file
            latest_migration = max(migration_files, key=os.path.getctime)

            # Read the file content
            with open(latest_migration, 'r') as f:
                content = f.read()

            # Check if sqlmodel import is missing
            if 'import sqlmodel' not in content and 'sqlmodel.sql.sqltypes' in content:
                # Add sqlmodel import after the existing imports
                lines = content.split('\n')
                new_lines = []
                imports_added = False

                for line in lines:
                    new_lines.append(line)  # type: ignore
                    # Add sqlmodel import after the sqlalchemy import
                    if 'import sqlalchemy as sa' in line and not imports_added:
                        new_lines.append('import sqlmodel')  # type: ignore
                        imports_added = True

                # Write the updated content back
                content = '\n'.join(new_lines)  # type: ignore
                with open(latest_migration, 'w') as f:
                    f.write(content)
                
                print(f"✅ Fixed sqlmodel import in {os.path.basename(latest_migration)}")
        
        except Exception as e:
            print(f"⚠️  Warning: Could not fix migration imports: {e}")

    def upgrade(self, revision: str = "head") -> bool:
        """Upgrade database to specified revision (default: head)"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print(f"🔄 Upgrading database to: {revision}")
        return_code, stdout, stderr = self._run_alembic_command(["upgrade", revision])
        
        if return_code == 0:
            print("✅ Database upgraded successfully")
            if stdout:
                print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to upgrade database: {stderr}")
            return False
    
    def downgrade(self, revision: str) -> bool:
        """Downgrade database to specified revision"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print(f"🔄 Downgrading database to: {revision}")
        return_code, stdout, stderr = self._run_alembic_command(["downgrade", revision])
        
        if return_code == 0:
            print("✅ Database downgraded successfully")
            if stdout:
                print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to downgrade database: {stderr}")
            return False
    
    def current(self) -> bool:
        """Show current database revision"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print("📋 Current database revision:")
        return_code, stdout, stderr = self._run_alembic_command(["current"])
        
        if return_code == 0:
            print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to get current revision: {stderr}")
            return False
    
    def history(self, verbose: bool = False) -> bool:
        """Show migration history"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        command = ["history"]
        if verbose:
            command.append("--verbose")
        
        print("📋 Migration history:")
        return_code, stdout, stderr = self._run_alembic_command(command)
        
        if return_code == 0:
            print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to get history: {stderr}")
            return False
    
    def show(self, revision: str = "head") -> bool:
        """Show migration details"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print(f"📋 Migration details for: {revision}")
        return_code, stdout, stderr = self._run_alembic_command(["show", revision])
        
        if return_code == 0:
            print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to show migration: {stderr}")
            return False
    
    def stamp(self, revision: str = "head") -> bool:
        """Mark database as being at a specific revision without running migrations"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print(f"🔄 Stamping database with revision: {revision}")
        return_code, stdout, stderr = self._run_alembic_command(["stamp", revision])
        
        if return_code == 0:
            print("✅ Database stamped successfully")
            if stdout:
                print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to stamp database: {stderr}")
            return False
    
    def check(self) -> bool:
        """Check if database is up to date"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print("🔍 Checking database status...")
        return_code, stdout, stderr = self._run_alembic_command(["current"])
        
        if return_code == 0:
            current = stdout.strip()
            if "head" in current or "up to date" in current:
                print("✅ Database is up to date")
                return True
            else:
                print("⚠️  Database is not up to date")
                print(f"Current: {current}")
                return False
        else:
            print(f"❌ Failed to check database status: {stderr}")
            return False
    
    def sqlmigrate(self, revision: str) -> bool:
        """Show SQL statements for a migration (Django-style sqlmigrate)"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print(f"📋 SQL statements for migration: {revision}")
        return_code, stdout, stderr = self._run_alembic_command(["upgrade", "--sql", revision])
        
        if return_code == 0:
            print(stdout.strip())
            return True
        else:
            print(f"❌ Failed to get SQL for migration: {stderr}")
            return False
    
    def show_migrations(self) -> bool:
        """Show all migrations with applied status (Django-style showmigrations)"""
        if not self.is_initialized():
            print("❌ Alembic not initialized. Run: python oppman.py migrate init")
            return False
        
        print("📋 Migration status:")
        
        # Get current revision
        return_code, current_stdout, current_stderr = self._run_alembic_command(["current"])
        if return_code != 0:
            print(f"❌ Failed to get current revision: {current_stderr}")
            return False
        
        # Get migration history
        return_code, history_stdout, history_stderr = self._run_alembic_command(["history", "--verbose"])
        if return_code != 0:
            print(f"❌ Failed to get migration history: {history_stderr}")
            return False
        
        # Parse current revision
        current_revision = None
        for line in current_stdout.split('\n'):
            if 'Rev:' in line:
                # Extract revision from line like "Rev: abc123def456 (head)"
                parts = line.split('Rev:')
                if len(parts) > 1:
                    revision_part = parts[1].strip().split()[0]
                    current_revision = revision_part
                break
        
        # Parse history and show status
        lines = history_stdout.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('Rev:') or line.startswith('Path:'):
                continue
            
            # Check if this migration is applied
            if current_revision and current_revision in line:
                status = "[X]"
            else:
                status = "[ ]"
            
            # Extract migration info
            if 'Rev:' in line:
                # Format: "Rev: abc123def456 (head), Parent: xyz789abc123"
                parts = line.split('Rev:')
                if len(parts) > 1:
                    rev_info = parts[1].strip()
                    # Extract revision hash and description
                    if '(' in rev_info:
                        revision_hash = rev_info.split('(')[0].strip()
                        description = rev_info.split('(')[1].split(')')[0].strip()
                        print(f"{status} {revision_hash} {description}")
                    else:
                        print(f"{status} {rev_info}")
        
        return True


def setup_alembic_config():
    """Create or update Alembic configuration files"""
    project_root = Path(__file__).parent.parent.parent
    
    # Create alembic.ini if it doesn't exist
    alembic_ini = project_root / "alembic.ini"
    if not alembic_ini.exists():
        print("❌ alembic.ini not found. Run: python oppman.py migrate init")
        return False
    
    # Update alembic.ini with correct database URL
    try:
        with open(alembic_ini, 'r') as f:
            content = f.read()
        
        # Update database URL for SQLite
        content = content.replace(
            'sqlalchemy.url = driver://user:pass@localhost/dbname',
            'sqlalchemy.url = sqlite+aiosqlite:///./test.db'
        )
        
        with open(alembic_ini, 'w') as f:
            f.write(content)
        
        print("✅ Updated alembic.ini with SQLite configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to update alembic.ini: {e}")
        return False
    
    # Update env.py to import models
    env_py = project_root / "alembic" / "env.py"
    if env_py.exists():
        try:
            with open(env_py, 'r') as f:
                content = f.read()
            
            # Add model imports
            if 'from models import SQLModel' not in content:
                # Find the target_metadata line and add imports before it
                lines = content.split('\n')
                new_lines = []
                imports_added = False
                
                for line in lines:
                    if 'target_metadata = None' in line and not imports_added:
                        new_lines.extend([
                            '',
                            '# Import your models here',
                            'from models import SQLModel',
                            'from models import User, Product',
                            '',
                            '# Set target metadata',
                            'target_metadata = SQLModel.metadata',
                            ''
                        ])
                        imports_added = True
                    else:
                        new_lines.append(line)
                
                content = '\n'.join(new_lines)
                
                with open(env_py, 'w') as f:
                    f.write(content)
                
                print("✅ Updated alembic/env.py with model imports")
                return True
        except Exception as e:
            print(f"❌ Failed to update env.py: {e}")
            return False
    
    return True