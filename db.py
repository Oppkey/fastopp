# db.py - Simple database setup for base_assets
import os

# from urllib.parse import urlparse  # Not needed for minimal config
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Load environment variables
load_dotenv()

# Get database URL from environment (defaults to SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Parse the database URL to extract SSL parameters
# parsed_url = urlparse(DATABASE_URL)  # Not needed for minimal config
# query_params = parse_qs(parsed_url.query)  # Not needed for psycopg3

# Extract SSL mode from URL parameters (not used in connect_args for psycopg3)
# ssl_mode = query_params.get('sslmode', ['prefer'])[0]

# Use the DATABASE_URL as-is (psycopg3 handles sslmode in URL properly)
clean_url = DATABASE_URL

# Create engine with minimal psycopg3 configuration
connect_args = {}

# Create async engine with conservative settings
async_engine = create_async_engine(
    clean_url,
    echo=True,  # set to False in production
    future=True,
    connect_args=connect_args,
    pool_size=3,  # Reduced pool size for stability
    max_overflow=5,  # Reduced overflow for stability
    pool_timeout=30,  # Conservative timeout
    pool_recycle=1800,  # 30 minutes recycle
    pool_pre_ping=True
)

# Event listener to disable prepared statements for PostgreSQL connections only
@event.listens_for(async_engine.sync_engine, "do_connect")
def _set_prepare_threshold(dialect, conn_rec, cargs, cparams):
    # Only inject prepare_threshold for PostgreSQL connections
    if "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
        cparams["prepare_threshold"] = None

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Export async_engine for admin setup
async_engine = async_engine
