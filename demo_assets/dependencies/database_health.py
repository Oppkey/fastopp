"""
Database health check and graceful degradation utilities
"""
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError
from .config import Settings, get_settings


class DatabaseHealthChecker:
    """Utility class for checking database connectivity and health"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self._engine = None
        self._is_healthy = None
        self._last_check = None
    
    async def get_engine(self):
        """Get or create database engine"""
        if self._engine is None:
            try:
                self._engine = create_async_engine(
                    self.settings.database_url,
                    echo=False,
                    future=True,
                    pool_size=1,
                    max_overflow=0,
                    pool_timeout=5,
                    pool_recycle=300,
                    pool_pre_ping=True
                )
            except Exception as e:
                print(f"Failed to create database engine: {e}")
                return None
        return self._engine
    
    async def is_database_available(self) -> bool:
        """Check if database is available and accessible"""
        try:
            engine = await self.get_engine()
            if engine is None:
                return False
            
            # Test connection with a simple query
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except (OperationalError, DatabaseError, Exception) as e:
            print(f"Database health check failed: {e}")
            return False
    
    async def get_database_status(self) -> Dict[str, Any]:
        """Get comprehensive database status information"""
        try:
            is_available = await self.is_database_available()
            
            return {
                "available": is_available,
                "database_url": self.settings.database_url,
                "database_type": self._get_database_type(),
                "error": None if is_available else "Database connection failed"
            }
        except Exception as e:
            return {
                "available": False,
                "database_url": self.settings.database_url,
                "database_type": self._get_database_type(),
                "error": str(e)
            }
    
    def _get_database_type(self) -> str:
        """Get database type from URL"""
        url = self.settings.database_url.lower()
        if "postgresql" in url or "postgres" in url:
            return "PostgreSQL"
        elif "sqlite" in url:
            return "SQLite"
        elif "mysql" in url:
            return "MySQL"
        else:
            return "Unknown"
    
    async def close(self):
        """Close database engine"""
        if self._engine:
            await self._engine.dispose()
            self._engine = None


# Global health checker instance
_health_checker: Optional[DatabaseHealthChecker] = None


async def get_database_health_checker() -> DatabaseHealthChecker:
    """Get or create database health checker"""
    global _health_checker
    if _health_checker is None:
        settings = get_settings()
        _health_checker = DatabaseHealthChecker(settings)
    return _health_checker


async def is_database_available() -> bool:
    """Quick check if database is available"""
    checker = await get_database_health_checker()
    return await checker.is_database_available()


async def get_database_status() -> Dict[str, Any]:
    """Get database status information"""
    checker = await get_database_health_checker()
    return await checker.get_database_status()


def get_fallback_data() -> Dict[str, Any]:
    """Get fallback data when database is unavailable"""
    return {
        "products": [],
        "categories": [],
        "stats": {
            "avg_price": 0,
            "min_price": 0,
            "max_price": 0,
            "total_products": 0
        },
        "stock": {
            "total": 0,
            "in_stock": 0,
            "out_of_stock": 0
        },
        "database_available": False,
        "fallback_message": "Database is currently unavailable. Please check your database configuration."
    }


def get_fallback_registrants() -> list:
    """Get fallback registrants data when database is unavailable"""
    return []


def get_fallback_attendees() -> list:
    """Get fallback attendees data when database is unavailable"""
    return []
