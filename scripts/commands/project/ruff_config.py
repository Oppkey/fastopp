"""
Ruff configuration setup for project management
"""

import re
import subprocess
from pathlib import Path

from .constants import RUFF_TEMPLATE


def detect_python_version(pyproject_content):
    """Detect Python version from pyproject.toml content"""
    python_version = "py312"  # default
    requires_python_match = re.search(
        r'requires-python\s*=\s*[">=]+(\d+)\.(\d+)', pyproject_content
    )
    if requires_python_match:
        major = requires_python_match.group(1)
        minor = requires_python_match.group(2)
        python_version = f"py{major}{minor}"
    return python_version


def add_ruff_configuration(pyproject_path):
    """Add Ruff configuration to pyproject.toml and install it"""
    # Read the already-saved pyproject.toml to detect Python version
    content = pyproject_path.read_text()

    # Detect Python version from requires-python
    python_version = detect_python_version(content)

    # Use embedded template and adjust target-version
    template_content = RUFF_TEMPLATE
    template_content = re.sub(
        r'target-version\s*=\s*"[^"]+"',
        f'target-version = "{python_version}"',
        template_content,
    )

    # Extract sections from template
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
    tool_ruff_indices = []
    for match in re.finditer(r"\[tool\.ruff[^\]]*\]", template_content):
        tool_ruff_indices.append(match.start())

    # Extract each section
    for i, start_idx in enumerate(tool_ruff_indices):
        if i + 1 < len(tool_ruff_indices):
            end_idx = tool_ruff_indices[i + 1]
        else:
            end_idx = len(template_content)

        ruff_section = template_content[start_idx:end_idx].strip()
        ruff_config_parts.append(ruff_section)

    # Add Ruff configuration to pyproject.toml (append to end)
    if ruff_config_parts:
        ruff_tool_sections = "\n\n".join(
            part for part in ruff_config_parts if "[tool.ruff" in part
        )
        optional_deps_text = ""
        if opt_deps_match:
            optional_deps_text = opt_deps_match.group(0) + "\n"

        # Append to end of file
        content = content.rstrip()
        if optional_deps_text:
            content += "\n\n" + optional_deps_text
        if ruff_tool_sections:
            content += "\n\n" + ruff_tool_sections + "\n"

        pyproject_path.write_text(content)
        print(
            f"✅ Added Ruff configuration to pyproject.toml (target-version: {python_version})"
        )

        # Install Ruff
        install_ruff()
        return True

    return False


def install_ruff():
    """Install Ruff to project dependencies using uv"""
    print("⚠️  Installing Ruff to project dependencies...")
    try:
        subprocess.run(
            ["uv", "add", "ruff", "--dev"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("✅ Ruff installed successfully")
    except subprocess.CalledProcessError as e:
        print(
            f"⚠️  Failed to install Ruff automatically: {e.stderr if e.stderr else 'Unknown error'}"
        )
        print("💡 You can install it manually with: uv add ruff --dev")
    except FileNotFoundError:
        print(
            "⚠️  uv command not found. Please install Ruff manually with: uv add ruff --dev"
        )
