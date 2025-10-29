"""
Ruff configuration setup for project management
"""

import re
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
    """Add Ruff configuration to pyproject.toml"""
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

    # Check if [project.optional-dependencies] already exists
    if "[project.optional-dependencies]" in content:
        # Check if ruff is already in dev dependencies
        if '"ruff"' in content or "'ruff" in content:
            # Ruff already exists, skip adding it
            pass
        elif re.search(r'\[project\.optional-dependencies\][^\[]*dev\s*=', content, re.DOTALL):
            # Dev key exists, add ruff to it
            dev_pattern = r'(dev\s*=\s*\[)([^\]]*?)(\])'
            dev_match = re.search(dev_pattern, content, re.DOTALL)
            if dev_match:
                existing_deps = dev_match.group(2).strip()
                if existing_deps:
                    # Add ruff to existing list
                    new_dev = f'{dev_match.group(1)}{existing_deps.rstrip(",").rstrip()},\n    "ruff"{dev_match.group(3)}'
                else:
                    new_dev = f'{dev_match.group(1)}"ruff"{dev_match.group(3)}'
                content = re.sub(dev_pattern, new_dev, content, flags=re.DOTALL)
        else:
            # Section exists but no dev key, add it after the section header
            # Find the section and add dev key right after it
            content = re.sub(
                r'(\[project\.optional-dependencies\]\s*)',
                r'\1dev = ["ruff"]\n',
                content,
            )
    else:
        # Section doesn't exist, add it with dev key
        optional_deps_section = '[project.optional-dependencies]\ndev = ["ruff"]\n\n'
        content = content.rstrip() + "\n\n" + optional_deps_section

    # Extract all [tool.ruff*] sections from template
    tool_ruff_indices = []
    for match in re.finditer(r"\[tool\.ruff[^\]]*\]", template_content):
        tool_ruff_indices.append(match.start())

    # Extract each tool.ruff section
    ruff_tool_sections = []
    for i, start_idx in enumerate(tool_ruff_indices):
        if i + 1 < len(tool_ruff_indices):
            end_idx = tool_ruff_indices[i + 1]
        else:
            end_idx = len(template_content)

        ruff_section = template_content[start_idx:end_idx].strip()
        ruff_tool_sections.append(ruff_section)

    # Append tool.ruff sections to end of file
    if ruff_tool_sections:
        ruff_config_text = "\n\n".join(ruff_tool_sections) + "\n"
        content = content.rstrip() + "\n\n" + ruff_config_text

    pyproject_path.write_text(content)
    print(
        f"✅ Added Ruff configuration to pyproject.toml (target-version: {python_version})"
    )
    print("💡 To install Ruff, run: uv sync --all  (or: uv add ruff --dev)")
    return True
