# PostgreSQL Setup and Database Configuration

This guide covers setting up PostgreSQL for the FastOpp project, including database configuration, environment variables, and the differences between development and production setups. It also includes database error handling and serverless deployment considerations.

## Quick Start

### 🚀 **For Serverless Deployment (Leapcell, Vercel, etc.)**
```bash
# .env (serverless - PostgreSQL required)
DATABASE_URL=postgresql+psycopg://username:password@host:port/database?sslmode=require
SECRET_KEY=your_secure_secret_key
ENVIRONMENT=production
```

### 🖥️ **For Traditional Deployment (Fly, Railway, Digital Ocean)**
```bash
# .env (traditional deployment - SQLite or PostgreSQL)
DATABASE_URL=sqlite+aiosqlite:///./test.db
# OR
DATABASE_URL=postgresql+psycopg://username:password@host:port/database
SECRET_KEY=your_secure_secret_key
ENVIRONMENT=production
```

### 💻 **For Local Development**
```bash
# .env (development)
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your_development_secret_key
ENVIRONMENT=development
```

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
# .env (development - local only)
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=your_development_secret_key_here
ENVIRONMENT=development
```

**⚠️ Important**: SQLite works for local development and traditional deployments (Fly, Railway, Digital Ocean). For serverless deployments (Leapcell, Vercel), you MUST use PostgreSQL with `postgresql+psycopg` driver.

**Note**: The existing `db.py` already handles environment variables automatically.

## Database Configuration

### Development Setup

#### Option A: SQLite (Development and Traditional Deployments)

```bash
# .env (development and traditional deployments)
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

**Benefits:**

- No additional software installation required
- Fast development iteration
- File-based storage
- Perfect for prototyping and development
- Works on Fly, Railway, Digital Ocean droplets

**⚠️ Important**: SQLite does NOT work in serverless environments (Leapcell, Vercel) due to filesystem limitations. Use PostgreSQL for serverless deployments.

**Note**: On Fly and Railway, SQLite files are ephemeral by default. For production, consider using PostgreSQL or configuring Fly Volumes for persistent storage.

#### Option B: PostgreSQL (Recommended for Production)

```bash
# .env
DATABASE_URL=postgresql+psycopg://fastopp_user:your_password@localhost/fastopp_db
```

**Note**: Use `postgresql+psycopg` driver (tested with Leapcell). `asyncpg` and `psycopg2` are not supported.

**Fly.io Managed Postgres**: Fly.io offers [Managed Postgres](https://fly.io/docs/database-storage-guides/) but we haven't tested it yet. If you test it successfully, please submit a pull request to update this documentation.

**Benefits:**

- Production-like environment
- Test PostgreSQL-specific features
- Vector database support with pgvector (no examples provided)
- Better for team development
- Required for serverless deployments
- Better performance for high-traffic applications
- Fly.io Managed Postgres available (untested)

#### Option C: PostgreSQL with SSL (For Serverless Deployments)

```bash
# .env - For serverless providers like Leapcell, Vercel, etc.
DATABASE_URL=postgresql+psycopg://username:password@host:port/database?sslmode=require
```

**Note**: Use `postgresql+psycopg` driver for serverless deployments. Only PostgreSQL has been tested with Leapcell.

**SSL Modes:**

- `sslmode=require` - SSL required (most cloud providers)
- `sslmode=prefer` - SSL preferred but not required
- `sslmode=verify-full` - SSL required with certificate verification
- `sslmode=disable` - SSL disabled (not recommended for production)

### Production Setup

For production, your `.env` file would contain:

```bash
# .env (production)
DATABASE_URL=postgresql+psycopg://fastopp_user:your_secure_password@localhost/fastopp_db
SECRET_KEY=your_very_secure_production_secret_key_here
ENVIRONMENT=production
```

## Environment Variables

### Required Variables

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./test.db` | `postgresql+psycopg://...` | Database connection string |
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
| **Database** | SQLite + aiosqlite | PostgreSQL + psycopg |
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
DATABASE_URL = "postgresql+psycopg://user:password@localhost/fastopp_db"
```

### PostgreSQL with pgvector (AI Features)
```python
DATABASE_URL = "postgresql+psycopg://user:password@localhost/fastopp_db"
# pgvector extension must be enabled separately
```

## Database Error Handling

The application includes comprehensive database error handling for graceful degradation:

### Database Status Page
Visit `/database-status` to check your database connection and get troubleshooting guidance.

### Health Check Endpoint
```bash
# Check database status via API
curl http://localhost:8000/health/database
```

### Serverless Deployment Considerations

#### Leapcell Deployment
- **SQLite Limitations**: SQLite cannot write to filesystem in serverless environments
- **PostgreSQL Required**: Use PostgreSQL with `postgresql+psycopg` driver
- **Tested Configuration**: Only PostgreSQL has been tested with Leapcell

#### Environment Variables for Serverless
```bash
# .env for serverless deployment
DATABASE_URL=postgresql+psycopg://username:password@host:port/database?sslmode=require
SECRET_KEY=your_secure_secret_key
ENVIRONMENT=production
```

#### Database Initialization
```bash
# Initialize database (corrected command)
uv run python oppman.py db
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors
- Verify `DATABASE_URL` format (use `postgresql+psycopg` for serverless)
- Check database service is running
- Ensure proper permissions
- Visit `/database-status` for detailed troubleshooting

#### 2. Environment Variable Issues
- Verify `.env` file exists in project root
- Check variable names match exactly
- Restart application after `.env` changes

#### 3. Migration Issues
- Ensure database is accessible
- Check Alembic configuration
- Verify model imports in `alembic/env.py`
- **Note**: Alembic is configured for async operations with both SQLite and PostgreSQL

#### 4. Serverless Deployment Issues
- **SQLite Errors**: SQLite cannot write to filesystem in serverless environments (Leapcell, Vercel)
- **Solution**: Use PostgreSQL with `postgresql+psycopg` driver
- **Database Status**: Visit `/database-status` for serverless-specific guidance
- **Driver Support**: Only `psycopg` is supported (not `asyncpg` or `psycopg2`)
- **Note**: SQLite works fine on traditional deployments (Fly, Railway, Digital Ocean). On Fly.io, consider using Fly Volumes for persistent SQLite storage.

#### 5. HTMX Loading Issues
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
