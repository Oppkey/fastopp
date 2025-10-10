import asyncio
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the local db module
from db import async_engine


async def test_connection():
    try:
        from sqlalchemy import text
        async with async_engine.begin() as conn:
            result = await conn.execute(text('SELECT version()'))
            print('✅ Database connection successful!')
            print(f'PostgreSQL version: {result.fetchone()[0]}')
    except Exception as e:
        print(f'❌ Connection failed: {e}')

asyncio.run(test_connection())
