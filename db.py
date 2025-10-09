# db.py - Simple database setup for base_assets
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment (defaults to SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Parse the database URL to extract SSL parameters
parsed_url = urlparse(DATABASE_URL)
query_params = parse_qs(parsed_url.query)

# Extract SSL mode from URL parameters
ssl_mode = query_params.get('sslmode', ['prefer'])[0]

# Remove sslmode from URL to avoid passing it to asyncpg
clean_url = DATABASE_URL
if 'sslmode=' in clean_url:
    # Remove sslmode parameter from URL
    if '?' in clean_url and 'sslmode=' in clean_url:
        base_url, query_string = clean_url.split('?', 1)
        query_parts = query_string.split('&')
        filtered_parts = [part for part in query_parts if not part.startswith('sslmode=')]
        if filtered_parts:
            clean_url = f"{base_url}?{'&'.join(filtered_parts)}"
        else:
            clean_url = base_url

# Create engine with SSL configuration
connect_args = {}
if parsed_url.scheme.startswith('postgresql'):
    # Configure SSL for PostgreSQL connections
    if ssl_mode == 'require':
        connect_args['ssl'] = 'require'
    elif ssl_mode == 'prefer':
        connect_args['ssl'] = 'prefer'
    elif ssl_mode == 'disable':
        connect_args['ssl'] = False
    elif ssl_mode == 'allow':
        connect_args['ssl'] = 'allow'
    elif ssl_mode == 'verify-ca':
        connect_args['ssl'] = 'verify-ca'
    elif ssl_mode == 'verify-full':
        connect_args['ssl'] = 'verify-full'
    
    # Add connection timeout settings for cloud providers
    connect_args['command_timeout'] = 10
    connect_args['server_settings'] = {
        'application_name': 'fastopp',
        'tcp_keepalives_idle': '600',
        'tcp_keepalives_interval': '30',
        'tcp_keepalives_count': '3'
    }

# Create async engine
async_engine = create_async_engine(
    clean_url,
    echo=True,  # set to False in production
    future=True,
    connect_args=connect_args,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)

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
