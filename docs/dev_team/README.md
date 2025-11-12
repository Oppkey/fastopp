# FastOpp Developer Tooling

- Install `uv`
- Install dev dependencies (including ruff) with `uv sync --group dev` or `uv sync --all-groups`

## Development Editor

- Use VS Code or Cursor.  Install Ruff extension

![ruff extension](images/ruff_extension.png)

- if on Windows, use WSL with Cursor installed in WSL

- install prettier inside of WSL


## New project based on FastOpp

The Ruff configuration is already included in the root `pyproject.toml` file. You can copy the relevant `[tool.ruff]` sections into your own `pyproject.toml` file.
