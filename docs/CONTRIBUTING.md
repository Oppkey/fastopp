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
   uv run python main.py
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
   version = "0.2.2"  # Increment version number
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

## Publishing Changes to PyPI

### Prerequisites for Publishing

#### For Maintainers (Project Owners)

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **API Token**: Generate an API token from your PyPI account settings
3. **Environment Variables**: Set up your credentials

#### For Contributors

**Important**: Only maintainers with PyPI access can publish releases. Contributors should:

1. **Submit Pull Requests** with their changes
2. **Let maintainers handle publishing** to PyPI
3. **Test locally** using `uv add .` to verify their changes work

#### Sharing PyPI Access (For Maintainers Only)

If you need to grant PyPI access to trusted contributors:

1. **Go to PyPI project settings**: https://pypi.org/manage/project/fastopp/collaboration/
2. **Add collaborators** with appropriate permissions:
   - **Owner**: Full access (can add/remove other collaborators)
   - **Maintainer**: Can upload new releases
3. **Share credentials securely**:
   - Use secure communication (encrypted email, secure messaging)
   - Never share credentials in public channels
   - Consider using team API tokens if available

### Publishing Process

#### Method 1: Using Environment Variables (Recommended)

1. **Set environment variables**:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=your-pypi-api-token
   ```

2. **Remove old build and build new package**:
   ```bash
   rm -rf dist/*
   uv build
   ```

3. **Upload to PyPI**:
   ```bash
   uv run twine upload dist/*
   ```

#### Method 2: Using .pypirc File

1. **Create/update `.pypirc`** in your home directory:
   ```ini
   [pypi]
   username = __token__
   password = your-pypi-api-token
   ```

2. **Build and upload**:
   ```bash
   uv build
   uv run twine upload dist/*
   ```

#### Method 3: Direct Command with Credentials

```bash
TWINE_USERNAME=__token__ TWINE_PASSWORD=your-token uv run twine upload dist/*
```

### Testing Before Publishing

#### Test on TestPyPI (Optional)

1. **Create TestPyPI account** at https://test.pypi.org/
2. **Get TestPyPI token** from your TestPyPI account
3. **Upload to TestPyPI first**:
   ```bash
   TWINE_USERNAME=__token__ TWINE_PASSWORD=your-testpypi-token uv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```
4. **Test installation from TestPyPI**:
   ```bash
   uv add --index-url https://test.pypi.org/simple/ fastopp
   ```

### Complete Publishing Workflow

```bash
# 1. Update version in pyproject.toml
# 2. Build the package
uv build

# 3. Upload to PyPI
```text
TWINE_USERNAME=__token__ 
TWINE_PASSWORD=your-token 
uv run twine upload dist/*
```

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

2. **Rebuild and publish**:
   ```bash
   uv build
   TWINE_USERNAME=__token__ TWINE_PASSWORD=your-token uv run twine upload dist/*
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
5. **Build and publish** to PyPI:
   ```bash
   uv build
   TWINE_USERNAME=__token__ TWINE_PASSWORD=your-token uv run twine upload dist/*
   ```

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

1. **Go to PyPI project settings**: https://pypi.org/manage/project/fastopp/collaboration/
2. **Add team members** with appropriate roles:
   - **Owner**: Full project control
   - **Maintainer**: Can upload releases
3. **Share credentials securely**:
   - Use encrypted communication
   - Never share in public channels
   - Consider using organization accounts for teams

#### Best Practices

- **Limit access** to trusted maintainers only
- **Use separate tokens** for different environments
- **Monitor upload activity** regularly
- **Revoke access** when team members leave

### Best Practices

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
- [ ] **Package builds** (`uv build`)
- [ ] **Ready to publish** to PyPI

## Contact

For questions about contributing:
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and discuss ideas
- **Email**: Contact the maintainers directly

Thank you for contributing to FastOpp! 🚀
