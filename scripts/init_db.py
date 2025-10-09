# =========================
# init_db.py - Database initialization script
# =========================
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from urllib.parse import urlparse, parse_qs
from db import DATABASE_URL
from sqlmodel import SQLModel


async def init_db():
    """Initialize the database by creating all tables."""
    try:
        print(f"🔍 Initializing database with URL: {DATABASE_URL}")
        
        # Parse the database URL to extract SSL parameters
        parsed_url = urlparse(DATABASE_URL)
        query_params = parse_qs(parsed_url.query)

        # Extract SSL mode from URL parameters
        ssl_mode = query_params.get('sslmode', ['prefer'])[0]
        print(f"🔍 SSL Mode: {ssl_mode}")

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
        
        print(f"🔍 Clean URL: {clean_url}")

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
        
        print(f"🔍 Connect args: {connect_args}")

        engine = create_async_engine(
            clean_url, 
            echo=True, 
            connect_args=connect_args,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True
        )

        print("🔍 Testing database connection...")
        async with engine.begin() as conn:
            # Test connection with a simple query
            result = await conn.execute("SELECT 1 as test")
            row = result.fetchone()
            print(f"🔍 Connection test successful: {row[0]}")
            
            # Create all tables
            print("🔍 Creating database tables...")
            await conn.run_sync(SQLModel.metadata.create_all)

        await engine.dispose()
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        import traceback
        print(f"❌ Error initializing database: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Full traceback:")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(init_db())
