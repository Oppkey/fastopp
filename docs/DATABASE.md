# Database Management

This guide covers database setup, migrations, troubleshooting, and best practices for the FastOpp application.

## Overview

Your FastOpp project includes a complete migration management system using **Alembic** (the standard migration tool for SQLAlchemy/SQLModel). This provides Django-like migration functionality with both Django-style and Alembic-style commands:

**Django-style commands (recommended):**

```bash
uv run python oppman.py makemigrations    # Create migrations
uv run python oppman.py migrate           # Apply migrations
uv run python oppman.py sqlmigrate <rev>  # Show SQL for migration
uv run python oppman.py showmigrations    # Show migration status
```

**Alembic-style commands (also available):**

```bash
uv run python oppman.py migrate [command] # Traditional Alembic commands
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
uv run python oppman.py makemigrations
# Enter migration message: Add Order model
```

### 4. Apply the Migration

```bash
uv run python oppman.py migrate
```

## Available Commands

### Django-Style Commands (Recommended)

```bash
# Create a new migration (prompts for message)
uv run python oppman.py makemigrations

# Apply all pending migrations
uv run python oppman.py migrate

# Show SQL statements for a migration
uv run python oppman.py sqlmigrate <revision>

# Show migration status with [X] applied, [ ] pending
uv run python oppman.py showmigrations
```

### Alembic-Style Commands (Also Available)

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
    uv run python oppman.py makemigrations
    # Enter migration message: Add categories table
    ```

3. **Apply migration**:

    ```bash
    uv run python oppman.py migrate
    ```

4. **Verify**:

    ```bash
    uv run python oppman.py showmigrations
    ```

### Modifying Existing Tables

1. **Modify model in `models.py`**:

    ```python
    class User(SQLModel, table=True):
        __tablename__ = "users"
        
        id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
        email: str = Field(unique=True, index=True, nullable=False)
        hashed_password: str = Field(nullable=False)
        is_active: bool = Field(default=True)
        is_superuser: bool = Field(default=False)
        # Add new field
        phone_number: Optional[str] = Field(default=None, max_length=20)
    ```

2. **Create migration**:

    ```bash
    uv run python oppman.py makemigrations
    # Enter migration message: Add phone number to users
    ```

3. **Apply migration**:

    ```bash
    uv run python oppman.py migrate
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

## File Structure

```
fastopp/
├── models.py                    # Your SQLModel models
├── alembic/                     # Generated by migrate init
│   ├── versions/               # Migration files
│   ├── env.py                 # Alembic environment
│   └── script.py.mako         # Migration template
├── alembic.ini                # Alembic configuration
├── scripts/migrate/           # Migration management
│   ├── core.py               # Core functionality
│   ├── cli.py                # Command interface
│   └── README.md             # Detailed documentation
└── oppman.py                 # Main management script
```

## Comparison with Django

| Django Command | FastOpp Django-Style | FastOpp Alembic-Style |
|----------------|---------------------|----------------------|
| `python manage.py migrate` | `python oppman.py migrate` | `python oppman.py migrate upgrade` |
| `python manage.py makemigrations` | `python oppman.py makemigrations` | `python oppman.py migrate create "Description"` |
| `python manage.py showmigrations` | `python oppman.py showmigrations` | `python oppman.py migrate history` |
| `python manage.py sqlmigrate <app> <migration>` | `python oppman.py sqlmigrate <revision>` | `python oppman.py migrate show <revision>` |

## Resetting the Database and Migrations

Sometimes you want to wipe the database and start over with a clean set of migration files. The `delete` command now backs up and removes both the SQLite database and all Alembic migration files under `alembic/versions/`.

### Delete Database and Migration Files

```bash
uv run python oppman.py delete
```

This will:

- Back up the current database to `test.db.YYYYMMDD_HHMMSS`.
- Back up all migration files to `alembic/versions_backup_YYYYMMDD_HHMMSS/`.
- Delete all `alembic/versions/*.py` files and clean `__pycache__`.

### Recreate Migrations

Use this when you have deleted the previous migration history and want to generate a fresh migration that reflects the current state of `models.py` and then apply it.

```bash
# Optional: ensure Alembic config is aligned (DB URL, imports)
uv run python oppman.py migrate setup

# Create a fresh initial migration from current models
uv run python oppman.py migrate create "Initial"

# Apply the migration to the (empty) database
uv run python oppman.py migrate upgrade
```

### How "Recreate Migrations" Differs from `uv run python oppman.py db`

- **Recreate migrations (create + upgrade)**: Uses Alembic to generate a migration file and apply it. This creates a proper migration history you can commit to version control, review, and use for upgrades/downgrades in all environments.
- **`uv run python oppman.py db`**: Directly creates tables via `SQLModel.metadata.create_all` without generating or applying Alembic migrations. This is convenient for quick local setups but does not produce migration files or history.

**Recommended:**

- Use the migration workflow for team/production workflows.
- Use `db` for quick local prototyping when migration history is not required.

## Integration with Existing Commands

The migration system integrates seamlessly with your existing `oppman.py` commands:

```bash
# Database management
uv run python oppman.py db              # Initialize database
uv run python oppman.py backup          # Backup database
uv run python oppman.py delete          # Delete database

# Migration management
uv run python oppman.py migrate init    # Initialize migrations
uv run python oppman.py migrate create  # Create migration
uv run python oppman.py migrate upgrade # Apply migrations

# Server management
uv run python oppman.py runserver       # Start development server
uv run python oppman.py production      # Start production server
```

## Registering a Model in the SQLAdmin Panel

Follow these steps to make a new model appear in the SQLAdmin UI. The examples use the `Partner` model, but the flow is the same for any model. All migration commands are run via your custom `oppman.py` tool.

1. **Define the model in `models.py`**:

   ```python
   # models.py
   class Partner(SQLModel, table=True):
       __tablename__ = "partners"
       id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
       name: str = Field(max_length=100, nullable=False)
       email: str = Field(unique=True, index=True, nullable=False)
   ```

2. **Create a ModelView in `admin/views.py`**:

   ```python
   # admin/views.py
   from sqladmin import ModelView
   from models import Partner

   class PartnerAdmin(ModelView, model=Partner):
       column_list = ["name", "email"]
   ```

3. **Register the view in `admin/setup.py`**:

   ```python
   # admin/setup.py
   from .views import UserAdmin, ProductAdmin, WebinarRegistrantsAdmin, AuditLogAdmin, PartnerAdmin

   def setup_admin(app: FastAPI, secret_key: str):
       admin = Admin(app, async_engine, authentication_backend=AdminAuth(secret_key=secret_key))
       admin.add_view(UserAdmin)
       admin.add_view(ProductAdmin)
       admin.add_view(WebinarRegistrantsAdmin)
       admin.add_view(AuditLogAdmin)
       admin.add_view(PartnerAdmin)  # <- new
       return admin
   ```

4. **Ensure Alembic "sees" the new model, then create and apply a migration using `oppman.py`**:

   ```bash
   # Update Alembic environment/imports (handled by the migrate setup command)
   uv run python oppman.py migrate setup

   # Create a migration for the new table (Django-style)
   uv run python oppman.py makemigrations
   # Enter migration message: Add partners table

   # Apply the migration
   uv run python oppman.py migrate
   ```

   Note: If you prefer to verify manually, ensure `alembic/env.py` imports your new model so that autogenerate includes it (e.g., `from models import Partner`). The `uv run python oppman.py migrate setup` command typically takes care of this.

5. **Restart the server and sign in to `/admin`**:

   - You must log in as a user with `is_staff` or `is_superuser` to see the admin panel.
   - The new model (e.g., "Partner") should now appear in the sidebar.

## Next Steps

After setting up your database:

1. **Run Initial Migrations**: Create and apply your first migration
2. **Add Sample Data**: Use `oppdemo.py` to populate with test data
3. **Test CRUD Operations**: Verify create, read, update, delete functionality
4. **Monitor Performance**: Check query performance and add indexes as needed
