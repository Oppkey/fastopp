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
        "README.md",
        ".github",
        ".cursor",
        ".git",
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
    print(
        "(Migration files will be moved but alembic/versions directory structure preserved)"
    )
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
        print(
            "ℹ️  No files to clean - all specified files/directories are already missing"
        )
        return True

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
            break
        elif response in ["no", "n"]:
            print("❌ Cleanup cancelled by user")
            return False
        else:
            print("Please enter 'yes' or 'no'")

    # Step 1: Run oppdemo.py destroy
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

    # Special handling for alembic/versions directory
    print("\n🗄️  Cleaning up migration files while preserving directory structure...")
    alembic_versions_dir = Path("alembic/versions")
    if alembic_versions_dir.exists():
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
    else:
        print("  ℹ️  alembic/versions directory not found")

    if failed_count == 0:
        print("\n🎉 Project cleanup completed successfully!")
        print(f"📦 Files backed up to: {backup_dir}")
        print("Your project is now ready to be used as a base for new applications.")
    else:
        print(f"\n⚠️  Cleanup completed with {failed_count} errors.")
        print("Some files may still need manual cleanup.")

    # Step 3: Interactive project setup wizard
    print("\n3️⃣  Setting up new project configuration...")
    project_name = (
        input("Enter project name (press Enter for 'my_fastopp_project'): ").strip()
        or "my_fastopp_project"
    )
    author_name = (
        input("Enter author name (press Enter for 'Your Name'): ").strip()
        or "Your Name"
    )
    description = (
        input(
            "Enter project description (press Enter for 'A new FastOpp project'): "
        ).strip()
        or "A new FastOpp project"
    )

    # Ask about Ruff configuration
    add_ruff = (
        input("Add Ruff configuration? (press Enter for 'yes'): ").strip().lower()
        or "yes"
    )
    use_ruff = add_ruff in ["yes", "y"]

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
        content = re.sub(
            r'description = ".*?"', f'description = "{description}"', content
        )

        # Add Ruff configuration if requested
        if use_ruff:
            # Read template file
            template_path = Path("docs/dev_team/template_pyproject.toml")
            if not template_path.exists():
                print("⚠️  Template file not found, skipping Ruff configuration")
            else:
                template_content = template_path.read_text()

                # Detect Python version from requires-python
                python_version = "py312"  # default
                requires_python_match = re.search(
                    r'requires-python\s*=\s*[">=]+(\d+)\.(\d+)', content
                )
                if requires_python_match:
                    major = requires_python_match.group(1)
                    minor = requires_python_match.group(2)
                    python_version = f"py{major}{minor}"

                # Extract Ruff config sections from template
                ruff_config_parts = []

                # Extract [project.optional-dependencies] dev section
                opt_deps_match = re.search(
                    r"\[project\.optional-dependencies\]\s*dev\s*=\s*\[.*?\]",
                    template_content,
                    re.DOTALL,
                )
                if opt_deps_match:
                    ruff_config_parts.append(opt_deps_match.group(0))

                # Extract all [tool.ruff*] sections
                # Find all tool.ruff section headers
                tool_ruff_indices = []
                for match in re.finditer(r"\[tool\.ruff[^\]]*\]", template_content):
                    tool_ruff_indices.append(match.start())

                # Extract each section (from header to next [ or end of file)
                for i, start_idx in enumerate(tool_ruff_indices):
                    # Find the end - either next section header or end of file
                    if i + 1 < len(tool_ruff_indices):
                        end_idx = tool_ruff_indices[i + 1]
                    else:
                        end_idx = len(template_content)

                    ruff_section = template_content[start_idx:end_idx].strip()
                    # Adjust target-version to match detected Python version
                    ruff_section = re.sub(
                        r'target-version\s*=\s*"[^"]+"',
                        f'target-version = "{python_version}"',
                        ruff_section,
                    )
                    ruff_config_parts.append(ruff_section)

                # Add Ruff configuration to pyproject.toml
                if ruff_config_parts:
                    # Check if [project.optional-dependencies] already exists
                    if "[project.optional-dependencies]" in content:
                        # Check if ruff is already in dev dependencies
                        if '"ruff"' not in content and "'ruff'" not in content:
                            # Merge dev dependencies if the section exists
                            if "dev = [" in content:
                                # Find the dev array and add ruff to it
                                # Match dev = [...] including multiline arrays
                                dev_pattern = r"(dev\s*=\s*\[)([^\]]*?)(\])"
                                dev_match = re.search(dev_pattern, content, re.DOTALL)
                                if dev_match:
                                    existing_deps = dev_match.group(2).strip()
                                    if existing_deps:
                                        # Add comma and ruff if there are existing deps
                                        new_dev_line = f'{dev_match.group(1)}{existing_deps.rstrip(",").rstrip()},\n    "ruff"{dev_match.group(3)}'
                                    else:
                                        # Just add ruff if array is empty
                                        new_dev_line = f'{dev_match.group(1)}"ruff"{dev_match.group(3)}'
                                    content = re.sub(
                                        dev_pattern,
                                        new_dev_line,
                                        content,
                                        flags=re.DOTALL,
                                    )
                                else:
                                    # dev array doesn't exist in expected format, add it
                                    content = re.sub(
                                        r"(\[project\.optional-dependencies\]\s*)",
                                        r'\1dev = ["ruff"]\n',
                                        content,
                                    )
                            else:
                                # Add dev line to existing optional-dependencies section
                                content = re.sub(
                                    r"(\[project\.optional-dependencies\]\s*)",
                                    r'\1dev = ["ruff"]\n',
                                    content,
                                )
                    else:
                        # Add the entire [project.optional-dependencies] section
                        if opt_deps_match:
                            content = (
                                content.rstrip()
                                + "\n\n"
                                + opt_deps_match.group(0)
                                + "\n"
                            )

                    # Append all [tool.ruff*] sections
                    ruff_tool_sections = "\n\n".join(
                        part for part in ruff_config_parts if "[tool.ruff" in part
                    )
                    if ruff_tool_sections:
                        content = content.rstrip() + "\n\n" + ruff_tool_sections + "\n"

                    print(
                        f"✅ Added Ruff configuration (target-version: {python_version})"
                    )

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
