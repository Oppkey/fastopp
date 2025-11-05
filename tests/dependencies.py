"""
Test dependencies for dependency injection system testing.

This module provides test-specific dependency overrides and mock implementations
for testing the FastAPI dependency injection system.
"""

from typing import AsyncGenerator
from unittest.mock import AsyncMock

from fastapi import FastAPI
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from dependencies.config import Settings, get_settings
from dependencies.database import get_db_session
from dependencies.services import get_chat_service, get_product_service, get_webinar_service


class TestSettings(Settings):
    """Test-specific settings with overrides for testing."""

    def __init__(self, **kwargs):
        # Set test-specific defaults
        test_defaults = {
            "database_url": "sqlite+aiosqlite:///:memory:",
            "secret_key": "test_secret_key",
            "environment": "testing",
            "access_token_expire_minutes": 30,
            "upload_dir": "test_uploads",
            "openrouter_api_key": "test_openrouter_key",
            "openai_api_key": "test_openai_key",
        }
        test_defaults.update(kwargs)
        super().__init__(**test_defaults)


def get_test_settings(**overrides) -> Settings:
    """Get test settings with optional overrides."""
    return TestSettings(**overrides)


async def get_test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Test database session using in-memory SQLite."""
    # Create in-memory test database
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )

    # Create tables
    from models import SQLModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async_session = AsyncSession(engine, expire_on_commit=False)

    try:
        yield async_session
    finally:
        await async_session.close()
        await engine.dispose()


def create_test_database_engine(settings: Settings = None):
    """Create test database engine."""
    if settings is None:
        settings = get_test_settings()

    return create_async_engine(
        settings.database_url,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )


def create_test_session_factory(engine=None):
    """Create test session factory."""
    if engine is None:
        engine = create_test_database_engine()

    from sqlalchemy.ext.asyncio import async_sessionmaker
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )


# Mock service instances for testing
class MockProductService:
    """Mock ProductService for testing."""

    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.settings = settings

    async def get_products_with_stats(self):
        """Mock implementation of get_products_with_stats."""
        return {
            "products": [
                {"id": 1, "name": "Test Product 1", "price": 10.99, "stock": 100},
                {"id": 2, "name": "Test Product 2", "price": 20.99, "stock": 50},
            ],
            "total_products": 2,
            "total_value": 31.98
        }

    async def get_product_by_id(self, product_id: int):
        """Mock implementation of get_product_by_id."""
        return {
            "id": product_id,
            "name": f"Test Product {product_id}",
            "price": 10.99,
            "stock": 100
        }


class MockWebinarService:
    """Mock WebinarService for testing."""

    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.settings = settings

    async def get_webinar_registrants(self):
        """Mock implementation of get_webinar_registrants."""
        return [
            {
                "id": 1,
                "name": "Test User 1",
                "email": "test1@example.com",
                "webinar_title": "Test Webinar",
                "registration_date": "2024-01-01T00:00:00"
            }
        ]

    async def get_webinar_attendees(self):
        """Mock implementation of get_webinar_attendees."""
        return [
            {
                "id": 1,
                "name": "Test User 1",
                "email": "test1@example.com",
                "attendance_status": "attended"
            }
        ]


class MockChatService:
    """Mock ChatService for testing."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def test_connection(self):
        """Mock implementation of test_connection."""
        return {
            "status": "success",
            "message": "Test connection successful",
            "api_key_configured": bool(self.settings.openrouter_api_key)
        }

    async def chat_completion(self, messages: list, stream: bool = False):
        """Mock implementation of chat_completion."""
        if stream:
            # Mock streaming response
            async def stream_generator():
                yield {"role": "assistant", "content": "Test streaming response"}
            return stream_generator()
        else:
            return {
                "role": "assistant",
                "content": "Test chat response",
                "usage": {"total_tokens": 100}
            }


def get_mock_product_service(
    session: AsyncSession = None,
    settings: Settings = None
):
    """Get mock ProductService for testing."""
    if session is None:
        session = AsyncMock(spec=AsyncSession)
    if settings is None:
        settings = get_test_settings()

    return MockProductService(session=session, settings=settings)


def get_mock_webinar_service(
    session: AsyncSession = None,
    settings: Settings = None
):
    """Get mock WebinarService for testing."""
    if session is None:
        session = AsyncMock(spec=AsyncSession)
    if settings is None:
        settings = get_test_settings()

    return MockWebinarService(session=session, settings=settings)


def get_mock_chat_service(settings: Settings = None):
    """Get mock ChatService for testing."""
    if settings is None:
        settings = get_test_settings()

    return MockChatService(settings=settings)


def create_test_app(
    override_dependencies: bool = True,
    test_settings: Settings = None
) -> FastAPI:
    """
    Create test FastAPI application with optional dependency overrides.

    Args:
        override_dependencies: Whether to override dependencies with test versions
        test_settings: Custom test settings to use

    Returns:
        Configured FastAPI test application
    """
    from main import app

    if not override_dependencies:
        return app

    if test_settings is None:
        test_settings = get_test_settings()

    # Override dependencies for testing
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_db_session] = get_test_db_session
    app.dependency_overrides[get_product_service] = get_mock_product_service
    app.dependency_overrides[get_webinar_service] = get_mock_webinar_service
    app.dependency_overrides[get_chat_service] = get_mock_chat_service

    return app


def create_test_app_with_real_db(
    test_settings: Settings = None
) -> FastAPI:
    """
    Create test FastAPI application with real database but mocked services.

    This is useful for integration testing where you want real database
    operations but mocked external services.

    Args:
        test_settings: Custom test settings to use

    Returns:
        Configured FastAPI test application with real database
    """
    from main import app

    if test_settings is None:
        test_settings = get_test_settings()

    # Override only settings and services, keep real database
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_product_service] = get_mock_product_service
    app.dependency_overrides[get_webinar_service] = get_mock_webinar_service
    app.dependency_overrides[get_chat_service] = get_mock_chat_service

    return app


# Pytest fixtures
@pytest.fixture
def test_settings():
    """Pytest fixture for test settings."""
    return get_test_settings()


@pytest.fixture
def test_settings_with_overrides():
    """Pytest fixture for test settings with custom overrides."""
    def _create_settings(**overrides):
        return get_test_settings(**overrides)
    return _create_settings


@pytest.fixture
async def test_db_session():
    """Pytest fixture for test database session."""
    async for session in get_test_db_session():
        yield session


@pytest.fixture
def mock_product_service(test_db_session, test_settings):
    """Pytest fixture for mock ProductService."""
    return get_mock_product_service(session=test_db_session, settings=test_settings)


@pytest.fixture
def mock_webinar_service(test_db_session, test_settings):
    """Pytest fixture for mock WebinarService."""
    return get_mock_webinar_service(session=test_db_session, settings=test_settings)


@pytest.fixture
def mock_chat_service(test_settings):
    """Pytest fixture for mock ChatService."""
    return get_mock_chat_service(settings=test_settings)


@pytest.fixture
def test_app():
    """Pytest fixture for test FastAPI application."""
    return create_test_app()


@pytest.fixture
def test_app_with_real_db():
    """Pytest fixture for test FastAPI application with real database."""
    return create_test_app_with_real_db()


@pytest.fixture
def test_client(test_app):
    """Pytest fixture for test client."""
    from fastapi.testclient import TestClient
    return TestClient(test_app)


@pytest.fixture
def async_test_client(test_app):
    """Pytest fixture for async test client."""
    from httpx import AsyncClient
    return AsyncClient(app=test_app, base_url="http://test")
