"""
Constants for project management commands
"""

# Embedded Ruff configuration template
RUFF_TEMPLATE = """[project.optional-dependencies]
dev = ["ruff"]

[tool.ruff]
line-length = 120
target-version = "py312"
select = ["E", "F", "I", "B", "UP", "SIM", "C4"]
fix = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
skip-magic-trailing-comma = false

[tool.ruff.isort]
combine-as-imports = true
force-sort-within-sections = true
"""
