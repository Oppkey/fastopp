# Database Management

This guide covers database setup, migrations, troubleshooting, and best practices for the FastOpp application.

## Overview

Your FastAPI project includes a complete migration management system using **Alembic** (the standard migration tool for SQLAlchemy/SQLModel). This provides Django-like migration functionality with the syntax:

```bash
uv run python oppman.py migrate [command]
```

## Quick Start

### 1. Initialize Migrations (First Time Only)

```bash
uv run python oppman.py migrate init
```

This will:

- Initialize Alembic in your project
- Create `alembic/` directory and `alembic.ini`
- Configure the database URL for SQLite
- Set up model imports in `alembic/env.py`

### 2. Add New Models to `models.py`

Edit your `models.py` file to add new models:

```python
class Order(SQLModel, table=True):
    __tablename__ = "orders"
    
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    total_amount: float = Field(nullable=False)
    status: str = Field(default="pending", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 3. Create a Migration

```bash
uv run python oppman.py migrate create "Add Order model"
```

### 4. Apply the Migration

```bash
uv run python oppman.py migrate upgrade
```

## Available Commands

### Basic Commands

```bash
# Initialize Alembic (first time only)
uv run python oppman.py migrate init

# Create a new migration
uv run python oppman.py migrate create "Description of changes"

# Apply all pending migrations
uv run python oppman.py migrate upgrade

# Check current status
uv run python oppman.py migrate current

# View migration history
uv run python oppman.py migrate history
```

### Advanced Commands

```bash
# Downgrade to previous revision
uv run python oppman.py migrate downgrade <revision>

# Show details of a migration
uv run python oppman.py migrate show <revision>

# Mark database as up to date without running migrations
uv run python oppman.py migrate stamp head

# Check if database is up to date
uv run python oppman.py migrate check

# Update configuration files
uv run python oppman.py migrate setup
```

## Workflow Examples

### Adding a New Table

1. **Add model to `models.py`**:

    ```python
    class Category(SQLModel, table=True):
        __tablename__ = "categories"
        
        id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
        name: str = Field(max_length=100, nullable=False)
        description: Optional[str] = Field(max_length=500)
        created_at: datetime = Field(default_factory=datetime.utcnow)
    ```

2. **Create migration**:

    ```bash
    uv run python oppman.py migrate create "Add Category model"
    ```

3. **Apply migration**

    ```bash
    uv run python oppman.py migrate upgrade
    ```

### Modifying Existing Tables

1. **Update model in `models.py`**

    ```python
    class Product(SQLModel, table=True):
        # ... existing fields ...
        category_id: Optional[uuid.UUID] = Field(foreign_key="categories.id", nullable=True)
    ```

2. **Create migration**

    ```bash
    uv run python oppman.py migrate create "Add category_id to Product"
    ```

3. **Apply migration**

    ```bash
    uv run python oppman.py migrate upgrade
    ```

## Database Configuration

### Environment Variables

Set your database URL in a `.env` file:

```bash
# Development (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./test.db

# Production (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@localhost/fastopp_db
```

### Database URLs by Environment

| Environment | URL Format | Driver | Use Case |
|-------------|------------|--------|----------|
| **Development** | `sqlite+aiosqlite:///./test.db` | aiosqlite | Local development |
| **Production** | `postgresql+asyncpg://...` | asyncpg | Production deployment |
| **Testing** | `sqlite+aiosqlite:///./test_test.db` | aiosqlite | Unit tests |

## Migration Files

### Structure

```text
alembic/
├── env.py              # Migration environment configuration
├── script.py.mako      # Migration template
├── alembic.ini        # Alembic configuration
└── versions/           # Migration files
    ├── 8e825dae1884_initial_migration.py
    ├── 6ec04a33369d_add_is_staff_field_to_user_model.py
    ├── fca21b76a184_add_photo_url_to_webinar_registrants.py
    ├── 0333e16b1b9d_add_notes_field_to_webinar_registrants.py
    └── 714ef079d138_merge_heads.py
```

### Migration File Example

```python
# alembic/versions/8e825dae1884_initial_migration.py
"""Initial migration

Revision ID: 8e825dae1884
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = '8e825dae1884'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_staff', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

## Troubleshooting

### Common Issues

#### 1. HTMX Automatic Loading Issues

**Problem**: The webinar demo page was not displaying attendees automatically. The page showed "No attendees found" even though there were sample attendees in the database.

**Root Cause**: The issue was with HTMX's `hx-trigger="load"` not firing reliably. The automatic trigger was failing due to timing issues:

1. **HTMX initialization timing**: HTMX might not be fully ready when the element loads
2. **Browser rendering timing**: The trigger could fire before HTMX is ready to handle it
3. **DOM loading sequence**: Element loads before HTMX is initialized

**Solution**: Add JavaScript fallbacks for HTMX:

```html
<div id="attendeesContainer" 
     hx-get="/api/webinar-attendees" 
     hx-trigger="load"
     hx-target="this"
     hx-swap="innerHTML">
    <div class="text-center py-8">
        <p class="text-gray-500">Loading attendees...</p>
    </div>
</div>
```

Plus JavaScript fallbacks:

```javascript
// Alpine.js component fallback
setTimeout(() => {
    const container = document.getElementById('attendeesContainer');
    if (container && container.innerHTML.includes('Loading attendees')) {
        console.log('Manually triggering HTMX request');
        htmx.trigger(container, 'load');
    }
}, 500);

// DOM ready fallback
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        const container = document.getElementById('attendeesContainer');
        if (container && container.innerHTML.includes('Loading attendees')) {
            console.log('DOM ready - triggering HTMX request');
            htmx.trigger(container, 'load');
        }
    }, 1000);
});
```

#### 2. Migration Errors

**Problem**: `sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place?`

**Root Cause**: 
- App uses async SQLAlchemy: `sqlite+aiosqlite:////data/test.db`
- Alembic was using sync operations during migrations
- Async context errors when mixing sync/async operations

**Solution**: Updated `alembic/env.py` to use async patterns:

```python
# Updated alembic/env.py uses async patterns
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())
```

#### 3. Database Connection Issues

**Symptoms**:
- Migration commands fail
- Application can't connect to database
- Permission denied errors

**Solutions**:
1. Verify `DATABASE_URL` format
2. Check database service is running
3. Ensure proper file permissions (SQLite) or user permissions (PostgreSQL)
4. Test connection manually

#### 4. Model Import Errors

**Symptoms**:
- `ModuleNotFoundError` during migrations
- Models not found in migration files

**Solutions**:
1. Check `alembic/env.py` imports
2. Verify model file paths
3. Ensure all dependencies are installed
4. Check for circular imports

## Best Practices

### 1. Migration Naming

Use descriptive names for migrations:

```bash
# Good
uv run python oppman.py migrate create "Add user profile fields"
uv run python oppman.py migrate create "Create product categories table"
uv run python oppman.py migrate create "Add email verification to users"

# Avoid
uv run python oppman.py migrate create "update"
uv run python oppman.py migrate create "fix"
uv run python oppman.py migrate create "changes"
```

### 2. Migration Order

- Always run migrations in order
- Don't skip migrations
- Test migrations on development data first
- Backup production database before major migrations

### 3. Model Changes

- Add new fields as nullable first, then make required
- Use foreign keys for relationships
- Include indexes for frequently queried fields
- Add proper constraints and validations

### 4. Testing Migrations

```bash
# Test migration creation
uv run python oppman.py migrate create "Test migration"

# Test migration upgrade
uv run python oppman.py migrate upgrade

# Test migration downgrade
uv run python oppman.py migrate downgrade -1

# Check migration status
uv run python oppman.py migrate current
```

## Database Operations

### Backup and Restore

#### SQLite

```bash
# Backup
cp test.db test_backup_$(date +%Y%m%d_%H%M%S).db

# Restore
cp test_backup_20240115_143022.db test.db
```

#### PostgreSQL

```bash
# Backup
pg_dump fastopp_db > fastopp_backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql fastopp_db < fastopp_backup_20240115_143022.sql
```

### Using oppman.py

```bash
# Backup database
python oppman.py backup

# Delete database
python oppman.py delete

# Check database status
python oppman.py env
```

## Advanced Features

### Vector Database Support

For AI applications, enable pgvector extension in PostgreSQL:

```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add vector field to model
class Document(SQLModel, table=True):
    __tablename__ = "documents"
    
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    content: str = Field(nullable=False)
    embedding: Optional[List[float]] = Field(default=None)  # Vector field
```

### Database Views

Create database views for complex queries:

```sql
-- Create view for user statistics
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.email,
    COUNT(w.id) as webinar_count,
    COUNT(wr.id) as registration_count
FROM users u
LEFT JOIN webinars w ON u.id = w.user_id
LEFT JOIN webinar_registrants wr ON w.id = wr.webinar_id
GROUP BY u.id, u.email;
```

## Next Steps

After setting up your database:

1. **Run Initial Migrations**: Create and apply your first migration
2. **Add Sample Data**: Use `oppdemo.py` to populate with test data
3. **Test CRUD Operations**: Verify create, read, update, delete functionality
4. **Monitor Performance**: Check query performance and add indexes as needed
