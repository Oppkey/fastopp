---
layout: post
title: "Architectural Consistency When Working with a PostgreSQL Async Database"
date: 2025-10-07
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/2025_10/run.jpg
excerpt: "How I learned that async databases need async migrations, and why the 'quick fix' approach doesn't scale"
---

## PostgreSQL Failing with Async in Production Although SQLite Works on my Mac

Last week, I was working on our FastOpp project and ran into a classic developer problem: "It works on my machine, but not in production." Specifically, our FastAPI application worked perfectly with SQLite during development, but when I tried to switch to PostgreSQL in production on Leapcell using the Leapcell PostgreSQL service,
database access broke.

## Converting Database Connection to Sync Led to More Problems

My first instinct was the same as many developers: find a workaround. I discovered that our
migration tool (Alembic) was trying to use synchronous database operations while our
FastAPI app was using asynchronous ones.

The "solution" I found online was to convert the database URL from async to sync during migrations:

```python
# The "quick fix" approach - BEFORE
def run_migrations_online() -> None:
    database_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    
    # Convert async URLs to regular URLs for migrations
    if database_url and "aiosqlite" in database_url:
        database_url = database_url.replace("sqlite+aiosqlite://", "sqlite://")
    elif database_url and "asyncpg" in database_url:
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    connectable = engine_from_config(...)  # SYNC engine
    with connectable.connect() as connection:  # SYNC connection
        context.configure(connection=connection, ...)
```

I committed the solution after only testing it on SQLite locally and unfortunately forgot
to test it on PostgreSQL.  Several months passed and my laziness came back to bite
me and cost me many hours. As I am new to Alembic, I didn't think about
async Alembic patterns. The logic of using synchronous calls for migrations seemed fine
to me as migrations _felt_ synchronous.  I didn't think about this mismatch in architectures
too deeply, shrugging it off as "the way things are."

## The Real Problem: Architectural Mismatch

Here's what I learned: when you build an async application, try to keep as much of your code
as possible async. Although it is possible to "convert" async to sync in the middle of your stack,
it may cause problems in the future when you have to maintain your own code.

The issue wasn't with the database or the migration tool. The issue was that I was trying to mix two different paradigms:

- **My FastAPI app**: Async throughout (using `asyncpg` for PostgreSQL)
- **My migrations**: Sync operations (using sync database drivers)

## The Right Solution: Go All-In on Async

Instead of trying to convert between async and sync, I updated our migration system to be async from the ground up. Here's the transformation:

## The Solution: Pure Async Approach

The key was updating `alembic/env.py` to use async patterns throughout:

```python
# The RIGHT approach - AFTER
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(...)  # ASYNC engine
    async with connectable.connect() as connection:  # ASYNC connection
        await connection.run_sync(do_run_migrations)  # Magic happens here!
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())
```

### Technical Implementation Details

- **Added async imports**: `asyncio`, `Connection`, `async_engine_from_config`
- **Replaced sync patterns** with async alembic template approach
- **Added `do_run_migrations()`** function for connection handling
- **Added `run_async_migrations()`** function for async engine management
- **Updated `run_migrations_online()`** to use `asyncio.run()`

The key insight was this line:

```python
await connection.run_sync(do_run_migrations)
```

This allows you to run synchronous migration code within an async database connection.

## The Results: What Actually Happened

After implementing the async approach, here's what we achieved:

### **Single Driver Architecture**

- **Before**: Needed both `asyncpg` (app) + `psycopg2` (migrations)
- **After**: Only `asyncpg` for everything - no driver conflicts

### **Consistent Database URLs**

- **Before**: App used `postgresql+asyncpg://` but migrations converted to `postgresql://`
- **After**: Both use `postgresql+asyncpg://` - same driver throughout

### **Works with Both Databases**

```bash
# SQLite (development)
export DATABASE_URL="sqlite+aiosqlite:///./test.db"
uv run python oppman.py migrate upgrade  # ✅ Works
uv run python oppman.py runserver  # ✅ Works

# PostgreSQL (production)  
export DATABASE_URL="postgresql+asyncpg://user@localhost:5432/fastopp"
uv run python oppman.py migrate upgrade  # ✅ Works
uv run python oppman.py runserver  # ✅ Works
```

### **Database Verification Results**

```bash
# PostgreSQL tables created successfully
psql -d fastopp_test -c "\dt"
# Result: users, products, webinar_registrants, audit_logs, alembic_version

# Health check verification
curl -s http://localhost:8000/health
# Result: {"status":"healthy","message":"FastOpp Demo app is running"}
```

## Benefits of the Async Approach

### Performance Benefits

- **Async operations** throughout the application
- **No sync/async context switching** overhead
- **Better concurrency** for database operations

### Developer Experience

- **Single driver approach** - no psycopg2 conflicts
- **Environment-based switching** between SQLite and PostgreSQL
- **Modern async patterns** following SQLAlchemy 2.0 best practices

### Production Ready

- **PostgreSQL support** for production deployments
- **Async alembic migrations** work with both databases
- **No breaking changes** to existing SQLite development workflow

## Why This Matters for Students

If you're learning web development, here's the takeaway: **consistency is more important than clever workarounds**.

When you're building modern web applications:

- Choose your architecture (sync or async) and stick with it
- Don't try to mix paradigms just because it seems easier
- The "quick fix" often becomes the "long-term problem"

## Async Database Access May Not Be Justified

Standardizing on synchronous database access for everything is simpler and will
work for most apps.  Asynchronous operations are needed only for heavy
SQL joins where the response takes many seconds or minutes and need to be run
in real-time.  In most cases, people will run the operation in the background
with Celery.  

However, even if I don't see the need for asynchronous database connections,
other people might.  FastOpp is a learning tool and I want to provide
asynchronous connectivity to support the creativity of others.

## The Business Lesson

As a manager, I've seen this pattern play out in many projects. The "quick fix"
that saves 30 minutes today often costs hours or days later. In this case, spending the extra time to properly implement async migrations saved us from a maintenance nightmare. The "quick fix"
was also forgotten because there is no real-world impact in using synchronous migrations.

The modern approach - using async patterns throughout - is not just technically correct, it's also more maintainable and scalable.

## What's Next

Our FastOpp project now supports both SQLite (for development) and PostgreSQL (for production) with a single, consistent async architecture. No more driver conflicts, no more sync/async mixing, and no more "it works on my machine" problems.

It appears that [psycopg3](https://www.psycopg.org/psycopg3/) supports both async and sync. I don't think it's as popular
as asyncpg.  However, I hope to try it out next.

## Migration Guide for Existing Users

### **No Action Required**

- **SQLite development** continues to work exactly as before
- **Optional**: Update `.env` to use `sqlite+aiosqlite://` for consistency
- **For PostgreSQL testing**: Set `DATABASE_URL=postgresql+asyncpg://...`

### **For New Deployments**

1. **Development**: Use `DATABASE_URL=sqlite+aiosqlite:///./test.db`
2. **Production**: Use `DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db`
3. **Run migrations**: `uv run python oppman.py migrate upgrade`

## Files Changed

- `alembic/env.py` - Updated to async patterns
- `example.env` - Added PostgreSQL configuration examples
- `docs/deployment/POSTGRESQL_SETUP.md` - Updated installation instructions
- `docs/DATABASE.md` - Updated troubleshooting with async patterns

## Breaking Changes

**None** - This is a backward-compatible enhancement that adds PostgreSQL support while maintaining full SQLite compatibility.

## Additional Information

[Pull request with extensive description of changes](https://github.com/Oppkey/fastopp/pull/140).
