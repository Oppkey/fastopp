from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from urllib.parse import urlparse, parse_qs
from .config import Settings, get_settings


def create_database_engine(settings: Settings = Depends(get_settings)):
    """Create database engine from settings with SSL support"""
    # Parse the database URL to extract SSL parameters
    parsed_url = urlparse(settings.database_url)
    query_params = parse_qs(parsed_url.query)

    # Extract SSL mode from URL parameters
    ssl_mode = query_params.get('sslmode', ['prefer'])[0]

    # Remove sslmode from URL to avoid passing it to asyncpg
    clean_query_params = {k: v for k, v in query_params.items() if k != 'sslmode'}
    clean_url = settings.database_url
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

    return create_async_engine(
        clean_url,
        echo=settings.environment == "development",
        future=True,
        connect_args=connect_args,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=3600,
        pool_pre_ping=True
    )


def create_session_factory(engine=Depends(create_database_engine)):
    """Create session factory from engine"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )


async def get_db_session(
    session_factory: async_sessionmaker = Depends(create_session_factory)
) -> AsyncSession:
    """Dependency to get database session"""
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
