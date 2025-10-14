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

        # Use the DATABASE_URL as-is (psycopg3 handles sslmode in URL properly)
        clean_url = DATABASE_URL
        print(f"🔍 Clean URL: {clean_url}")

        # Create engine with database-specific configuration
        connect_args = {}
        
        # Only add prepare_threshold for PostgreSQL connections
        if "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
            connect_args["prepare_threshold"] = None
        
        print(f"🔍 Connect args: {connect_args}")

        engine = create_async_engine(
            clean_url, 
            echo=True, 
            connect_args=connect_args,
            pool_size=3,  # Reduced pool size for stability
            max_overflow=5,  # Reduced overflow for stability
            pool_timeout=30,  # Conservative timeout
            pool_recycle=1800,  # 30 minutes recycle
            pool_pre_ping=True
        )

        print("🔍 Testing database connection...")
        async with engine.begin() as conn:
            # Test connection with a simple query
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1 as test"))
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
