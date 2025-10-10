from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import event
# from urllib.parse import urlparse  # Not needed for minimal config
from .config import Settings, get_settings


def create_database_engine(settings: Settings = Depends(get_settings)):
    """Create database engine from settings with SSL support"""
    # Parse the database URL to extract SSL parameters
    # parsed_url = urlparse(settings.database_url)  # Not needed for minimal config
    # query_params = parse_qs(parsed_url.query)  # Not needed for psycopg3

    # Extract SSL mode from URL parameters (not used in connect_args for psycopg3)
    # ssl_mode = query_params.get('sslmode', ['prefer'])[0]

    # Use the DATABASE_URL as-is (psycopg3 handles sslmode in URL properly)
    clean_url = settings.database_url

    # Create engine with minimal psycopg3 configuration
    connect_args = {}

    engine = create_async_engine(
        clean_url,
        echo=settings.environment == "development",
        future=True,
        connect_args=connect_args,
        pool_size=3,  # Reduced pool size for stability
        max_overflow=5,  # Reduced overflow for stability
        pool_timeout=30,  # Conservative timeout
        pool_recycle=1800,  # 30 minutes recycle
        pool_pre_ping=True
    )

    # Event listener to disable prepared statements for all connections
    @event.listens_for(engine.sync_engine, "do_connect")
    def _set_prepare_threshold(dialect, conn_rec, cargs, cparams):
        # Inject driver-specific args before psycopg3 connects
        cparams["prepare_threshold"] = None

    return engine


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
