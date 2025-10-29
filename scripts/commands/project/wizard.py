"""
Interactive project setup wizard
"""

import re
from pathlib import Path

from .ruff_config import add_ruff_configuration


def run_setup_wizard():
    """Run interactive project setup wizard"""
    print("\n3️⃣  Setting up new project configuration...")

    # Collect user input
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

    # Delete README.md (it was already moved to backup)
    readme_path = Path("README.md")
    if readme_path.exists():
        readme_path.unlink()
        print("✅ Deleted README.md")

    # Update and save pyproject.toml immediately with name, author, description
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
        pyproject_path.write_text(content)
        print("✅ Updated pyproject.toml")

    # Ask about Ruff configuration
    add_ruff = input("Add Ruff configuration? (press Enter to skip): ").strip().lower()
    use_ruff = add_ruff in ["yes", "y"]

    # Add Ruff configuration if requested
    if use_ruff:
        add_ruff_configuration(pyproject_path)

    # Create new README.md
    generate_readme(project_name, author_name, description)


def generate_readme(project_name, author_name, description):
    """Generate a new README.md file"""
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
