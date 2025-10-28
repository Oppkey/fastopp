# Contributing to FastOpp

Thank you for your interest in contributing to FastOpp! This guide will help you understand how to contribute to the project and publish changes to PyPI.

## Development Setup

### Prerequisites

- Python 3.12 or higher
- `uv` package manager
- Git

### Initial Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd fastopp
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Run the application**:

   ```bash
   uv run python oppman.py runserver
   ```

## Making Changes

### Development Workflow

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test them:

   ```bash
   # Run tests
   uv run pytest

   # Run linting
   uv run ruff check .
   uv run mypy .
   ```

3. **Update version** in `pyproject.toml` if needed:

   ```toml
   version = "0.4.5"  # Increment version number
   ```

4. **Commit your changes**:

   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

## Publishing Changes to PyPI

### Prerequisites for Publishing

#### Publishing For Maintainers (Project Owners)

1. **PyPI Account**: Create an account at <https://pypi.org/account/register/>
2. **API Token**: Generate an API token from your PyPI account settings
3. **Environment Variables**: Set up your credentials

#### Publishing For Contributors

**Important**: Only maintainers with PyPI access can publish releases. Contributors should:

1. **Submit Pull Requests** with their changes
2. **Let maintainers handle publishing** to PyPI
3. **Test locally** using `uv add .` to verify their changes work

#### Sharing PyPI Access (For Maintainers Only)

If you need to grant PyPI access to trusted contributors:

1. **Go to PyPI project settings**: <https://pypi.org/manage/project/fastopp/collaboration/>
2. **Add collaborators** with appropriate permissions:
   - **Owner**: Full access (can add/remove other collaborators)
   - **Maintainer**: Can upload new releases
3. **Share credentials securely**:
   - Use secure communication (encrypted email, secure messaging)
   - Never share credentials in public channels
   - Consider using team API tokens if available

### Publishing Process

#### Test on TestPyPI First (Recommended)

**Important**: Always test on TestPyPI before publishing to PyPI, especially for pre-release versions.

1. **Create TestPyPI account** at <https://test.pypi.org/>
2. **Get TestPyPI token** from your TestPyPI account
3. **Set up environment variables in `.env` file**:

   ```bash
   # Add to your .env file
   UV_PUBLISH_TOKEN=your-pypi-api-token
   UV_PUBLISH_TOKEN_TEST_PYPI=your-testpypi-api-token
   ```

4. **Upload to TestPyPI first**:

   ```bash
   # Load environment variables
   source .env

   # Publish to TestPyPI
   uv publish --publish-url https://test.pypi.org/legacy/ --token $UV_PUBLISH_TOKEN_TEST_PYPI
   ```

5. **Test installation from TestPyPI**:

   ```bash
   # Create a virtual environment first
   uv venv

   # Option 1: Activate the environment manually
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastopp==0.4.6a0 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match

   # Option 2: Specify Python path directly (no activation needed)
   uv pip install --python .venv/bin/python fastopp==0.4.6a0 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match
   ```

   **Note**: The `--index-strategy unsafe-best-match` flag is required when mixing TestPyPI and PyPI indexes, as TestPyPI may not have all dependencies.

   **If installation fails**, try adding the `--prerelease allow` flag:

   ```bash
   # Create a virtual environment first
   uv venv

   # Option 1: Activate the environment manually
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastopp==0.4.6a1 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match \
     --prerelease allow

   # Option 2: Specify Python path directly (no activation needed)
   uv pip install --python .venv/bin/python fastopp==0.4.6a1 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match \
     --prerelease allow
   ```

#### Pre-release Versioning Strategy

For pre-release versions, you have two options:

**Option 1: Increment version for each test** (Recommended)

```toml
# First test
version = "0.4.6a0"

# Second test (if first had issues)
version = "0.4.6a1"

# Third test (if needed)
version = "0.4.6a2"
```

**Option 2: Overwrite same version** (Possible but not recommended)

- TestPyPI allows overwriting the same version
- PyPI does NOT allow overwriting (you must increment)
- **Recommendation**: Use incrementing versions for consistency

#### Testing Pre-release Versions

##### Creating Git Tags for Pre-releases

When testing pre-release versions (e.g., `0.4.6a0`, `0.4.6a1`):

1. **Create and push the tag**:

   ```bash
   # Create the tag locally
   git tag v0.4.6a0

   # Push the tag to GitHub
   git push origin v0.4.6a0
   ```

2. **Test fastopp-startproject**:

   ```bash
   # Create a virtual environment first
   uv venv

   # Option 1: Activate the environment manually
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastopp==0.4.6a0 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match

   # Option 2: Specify Python path directly (no activation needed)
   uv pip install --python .venv/bin/python fastopp==0.4.6a0 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match

   # Test the startproject command
   mkdir test-project && cd test-project
   uv init --python 3.12
   uv add fastopp
   uv run fastopp-startproject
   ```

   **If installation fails**, try adding the `--prerelease allow` flag:

   ```bash
   # Create a virtual environment first
   uv venv

   # Option 1: Activate the environment manually
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install fastopp==0.4.6a1 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match \
     --prerelease allow

   # Option 2: Specify Python path directly (no activation needed)
   uv pip install --python .venv/bin/python fastopp==0.4.6a1 fastapi==0.120.1 \
     --index-url https://test.pypi.org/simple/ \
     --extra-index-url https://pypi.org/simple \
     --index-strategy unsafe-best-match \
     --prerelease allow
   ```

3. **Expected behavior**:

   - If tag `v0.4.6a0` exists: Uses that exact version template
   - If tag doesn't exist: Falls back to latest stable release (e.g., `v0.4.5`)
   - User sees clear messages about which version is being used

##### Testing Version Fallback

To test the fallback mechanism:

1. **Upload pre-release to TestPyPI** (without creating git tag)
2. **Install and test**: Package will try to find matching tag, fail, and fall back to latest stable
3. **Create tag later**: Same package will now find and use the matching tag

This allows you to:

- Test pre-release packages on TestPyPI before tagging
- Gradually roll out features by tagging when ready
- Ensure users always get a working template

#### Publish to PyPI (After Testing)

Once you've tested on TestPyPI and are satisfied:

1. **Source environment and publish**:

   ```bash
   # Load environment variables
   source .env

   # Publish to PyPI
   uv publish --token $UV_PUBLISH_TOKEN
   ```

#### Alternative Publishing Methods

##### Method 1: Using .pypirc File (Alternative)

1. **Create/update `.pypirc`** in your home directory:

   ```ini
   [pypi]
   username = __token__
   password = your-pypi-api-token
   ```

2. **Publish using uv**:

   ```bash
   uv publish
   ```

   **Note**: `uv publish` will automatically use `.pypirc` configuration if available.

##### Method 2: Direct Command with Credentials (Alternative)

```bash
uv publish --token your-pypi-api-token
```

**Note**: This method is less secure than using environment variables.

### Complete Publishing Workflow

```bash
# 1. Update version in pyproject.toml
# 2. Load environment variables
source .env

# 3. Publish to PyPI
uv publish --token $UV_PUBLISH_TOKEN

# 4. Verify the upload
# Visit: https://pypi.org/project/fastopp/
```

## Version Management

### Semantic Versioning

Follow semantic versioning (SemVer):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

### Updating Version

1. **Edit `pyproject.toml`**:

   ```toml
   version = "0.2.2"  # Update version number
   ```

2. **Publish**:

   ```bash
   source .env
   uv publish --token $UV_PUBLISH_TOKEN
   ```

## Code Quality

### Linting and Formatting

```bash
# Run linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check . --fix

# Type checking
uv run mypy .
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=fastopp

# Run specific test file
uv run pytest tests/test_specific.py
```

## Pull Request Process

### For Contributors

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Test locally** with `uv add .`
7. **Submit a pull request**

### For Maintainers

1. **Review pull requests**
2. **Test changes** thoroughly
3. **Merge approved changes**
4. **Update version** in `pyproject.toml`
5. **Publish** to PyPI:

   ```bash
   source .env
   uv publish --token $UV_PUBLISH_TOKEN
   ```

#### Monitor PyPI

<https://pypistats.org/packages/fastopp>

### Pull Request Guidelines

- **Clear description** of changes
- **Reference issues** if applicable
- **Include tests** for new features
- **Update documentation** as needed
- **Follow coding standards**

## Troubleshooting

### Common Issues

#### 403 Forbidden Error

- **Cause**: Invalid API token or wrong repository
- **Solution**: Verify your PyPI token and repository URL

#### Build Errors

- **Cause**: Missing dependencies or configuration issues
- **Solution**: Run `uv sync` and check `pyproject.toml`

#### Upload Failures

- **Cause**: Network issues or authentication problems
- **Solution**: Check your internet connection and API token

### Getting Help

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the docs/ directory for more information

## Security

### API Token Security

- **Never commit** API tokens to version control
- **Use environment variables** for credentials
- **Rotate tokens** regularly
- **Use `.gitignore`** to exclude sensitive files

### Access Management

#### Who Can Publish?

- **Project Owners**: Full PyPI access
- **Maintainers**: Can upload releases (if granted access)
- **Contributors**: Submit PRs only (no direct PyPI access)

#### Granting PyPI Access

1. **Go to PyPI project settings**: <https://pypi.org/manage/project/fastopp/collaboration/>
2. **Add team members** with appropriate roles:
   - **Owner**: Full project control
   - **Maintainer**: Can upload releases
3. **Share credentials securely**:
   - Use encrypted communication
   - Never share in public channels
   - Consider using organization accounts for teams

### Best Practices

#### Security & Access Management

- **Limit access** to trusted maintainers only
- **Use separate tokens** for different environments
- **Monitor upload activity** regularly
- **Revoke access** when team members leave

#### Publishing Guidelines

- **Review changes** before publishing
- **Test thoroughly** in development
- **Use semantic versioning**
- **Document breaking changes**

## Release Checklist

Before publishing a new version:

- [ ] **Version updated** in `pyproject.toml`
- [ ] **Tests passing** (`uv run pytest`)
- [ ] **Linting clean** (`uv run ruff check .`)
- [ ] **Documentation updated**
- [ ] **Changelog updated**
- [ ] **Environment variables loaded** (`source .env`)
- [ ] **Ready to publish** to PyPI (`uv publish --token $UV_PUBLISH_TOKEN`)

## Contact

For questions about contributing:

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and discuss ideas
- **Email**: Contact the maintainers directly

Thank you for contributing to FastOpp! 🚀
