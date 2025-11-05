import asyncio
from logging.config import fileConfig
import os

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models here
from models import SQLModel

# Set target metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    # Convert async URLs to regular URLs for offline migrations
    if url and "aiosqlite" in url:
        url = url.replace("sqlite+aiosqlite://", "sqlite://")
    elif url and "asyncpg" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    database_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    # Ensure database_url is not None before setting it
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_sync_migrations() -> None:
    """Run migrations in synchronous mode for SQLite."""
    from sqlalchemy import create_engine

    database_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    # Convert async URLs to regular URLs for SQLite
    if database_url and "aiosqlite" in database_url:
        database_url = database_url.replace("sqlite+aiosqlite://", "sqlite://")
    elif database_url and "asyncpg" in database_url:
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    # Ensure database_url is not None before setting it
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    database_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

    # Use synchronous migrations for SQLite, async for others
    if database_url and ("sqlite" in database_url or "aiosqlite" in database_url):
        run_sync_migrations()
    else:
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
