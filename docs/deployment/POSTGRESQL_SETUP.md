# PostgreSQL Setup and Database Configuration

This guide covers setting up PostgreSQL for the FastOpp project, including database configuration, environment variables, and the differences between development and production setups.

## Quick Start

### 1. Install Dependencies

```bash
# Add environment variable support
uv add python-dotenv

# PostgreSQL support is already included in pyproject.toml
# No additional packages needed - asyncpg is already installed
```

### 2. Environment-Based Database Configuration

Create a `.env` file in your project root:

```bash
# .env (development)
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your_development_secret_key_here
ENVIRONMENT=development
```

Update your `db.py` to use environment variables:

```python
# db.py
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment (defaults to SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # set to False in production
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)
```

## Database Configuration

### Development Setup

#### Option A: SQLite (Default - Recommended for Development)

```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

**Benefits:**
- No additional software installation required
- Fast development iteration
- File-based storage
- Perfect for prototyping and development

#### Option B: PostgreSQL (For Testing PostgreSQL Features)

```bash
# .env
DATABASE_URL=postgresql+asyncpg://fastopp_user:your_password@localhost/fastopp_db
```

**Benefits:**
- Production-like environment
- Test PostgreSQL-specific features
- Vector database support with pgvector
- Better for team development

#### Option C: PostgreSQL with SSL (For Cloud Providers)

```bash
# .env - For cloud providers like Leapcell, Railway, etc.
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database?sslmode=require
```

**SSL Modes:**
- `sslmode=require` - SSL required (most cloud providers)
- `sslmode=prefer` - SSL preferred but not required
- `sslmode=verify-full` - SSL required with certificate verification
- `sslmode=disable` - SSL disabled (not recommended for production)

### Production Setup

For production, your `.env` file would contain:

```bash
# .env (production)
DATABASE_URL=postgresql+asyncpg://fastopp_user:your_secure_password@localhost/fastopp_db
SECRET_KEY=your_very_secure_production_secret_key_here
ENVIRONMENT=production
```

## Environment Variables

### Required Variables

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./test.db` | `postgresql+asyncpg://...` | Database connection string |
| `SECRET_KEY` | `dev_secret_key` | `very_secure_key` | JWT and session encryption |
| `ENVIRONMENT` | `development` | `production` | Environment identifier |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `DEBUG` | `True` | Debug mode (development only) |
| `HOST` | `0.0.0.0` | Server host binding |
| `PORT` | `8000` | Server port |

## Development vs Production Setup

### Quick Reference

| Component | Development | Production |
|-----------|-------------|------------|
| **Database** | SQLite + aiosqlite | PostgreSQL + asyncpg |
| **Server** | uvicorn --reload | Gunicorn + Uvicorn |
| **Process Manager** | None (manual) | Systemd |
| **Reverse Proxy** | None | Nginx |
| **SSL** | None | Let's Encrypt |
| **Logging** | Console | File + rotation |
| **Backups** | Manual | Automated |

### Development Commands

```bash
# Start development server
uv run uvicorn main:app --reload

# Or use oppman.py
python oppman.py runserver

# Initialize database
python oppman.py migrate init
python oppman.py migrate create "Initial migration"
python oppman.py migrate upgrade
python oppman.py init
```

### Production Commands

```bash
# Start production server
python oppman.py production

# Database operations
python oppman.py migrate upgrade
python oppman.py backup

# Environment check
python oppman.py env
```

## Database URLs by Environment

### Development (SQLite)
```python
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
```

### Production (PostgreSQL)
```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/fastopp_db"
```

### PostgreSQL with pgvector (AI Features)
```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/fastopp_db"
# pgvector extension must be enabled separately
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
- Verify `DATABASE_URL` format
- Check database service is running
- Ensure proper permissions

#### 2. Environment Variable Issues
- Verify `.env` file exists in project root
- Check variable names match exactly
- Restart application after `.env` changes

#### 3. Migration Issues
- Ensure database is accessible
- Check Alembic configuration
- Verify model imports in `alembic/env.py`
- **Note**: Alembic is configured for async operations with both SQLite and PostgreSQL

#### 4. HTMX Loading Issues
If you encounter automatic loading problems:

```javascript
// Add JavaScript fallbacks for HTMX
setTimeout(() => {
    const container = document.getElementById('attendeesContainer');
    if (container && container.innerHTML.includes('Loading attendees')) {
        console.log('Manually triggering HTMX request');
        htmx.trigger(container, 'load');
    }
}, 500);
```

## Next Steps

After setting up your environment:

1. **Initialize Database**: Run migrations and create sample data
2. **Start Development Server**: Begin building and testing features
3. **Configure Admin Panel**: Set up user accounts and permissions
4. **Test Features**: Verify file uploads, AI chat, and admin functionality

For more detailed information on specific components, see:
- [DATABASE.md](../DATABASE.md) - Database management and migrations
- [FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md) - Fly.io deployment guide
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture overview
