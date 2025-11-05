"""
Simple FastAPI Dependency Injection Tests

This test suite demonstrates basic FastAPI dependency injection concepts
for educational purposes. It focuses on core functionality without
complex edge cases or performance testing.
"""

from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

from dependencies.config import Settings, get_settings
from dependencies.database import create_database_engine, create_session_factory, get_db_session
from dependencies.services import get_chat_service, get_product_service, get_webinar_service
from main import app as main_app
from tests.dependencies import (
    MockChatService,
    MockProductService,
    MockWebinarService,
    create_test_app,
    get_test_db_session,
    get_test_settings,
)


class TestDependencyInjection:
    """Test core dependency injection functionality."""
    
    def test_settings_dependency(self):
        """Test that settings dependency works correctly."""
        settings = get_test_settings()
        assert settings is not None
        assert settings.database_url == "sqlite+aiosqlite:///:memory:"
        assert settings.environment == "testing"
    
    def test_database_session_dependency(self):
        """Test that database session dependency works correctly."""
        # This test verifies the dependency function exists and is callable
        from dependencies.database import get_db_session
        assert callable(get_db_session)

    def test_service_dependencies_exist(self):
        """Test that service dependency functions exist and are callable."""
        assert callable(get_product_service)
        assert callable(get_webinar_service)
        assert callable(get_chat_service)


class TestAPIEndpoints:
    """Test essential API endpoints."""

    @pytest.fixture(scope="class")
    def client(self):
        with TestClient(main_app) as c:
            yield c

    def test_products_endpoint(self, client):
        """Test the /api/products endpoint."""
        response = client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert isinstance(data["products"], list)

    def test_webinar_attendees_endpoint(self, client):
        """Test the /api/webinar-attendees endpoint."""
        response = client.get("/api/webinar-attendees")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert "name" in data[0]

    def test_chat_test_endpoint(self, client):
        """Test the /chat/test endpoint."""
        response = client.get("/chat/test")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


class TestDependencyOverrides:
    """Test dependency override mechanism."""

    def test_app_creation_with_overrides(self):
        """Test that the test app is created with dependency overrides."""
        test_app = create_test_app()
        assert test_app is not None
        assert get_settings in test_app.dependency_overrides
        assert get_db_session in test_app.dependency_overrides
        assert get_product_service in test_app.dependency_overrides


class TestMockServices:
    """Test mock service implementations."""
    
    async def test_mock_product_service(self):
        """Test mock product service functionality."""
        from tests.dependencies import MockProductService, get_test_settings
        
        settings = get_test_settings()
        # MockProductService needs both session and settings
        service = MockProductService(session=None, settings=settings)
        
        # Test basic functionality
        products = await service.get_products_with_stats()
        assert isinstance(products, dict)
        assert "products" in products
        assert "total_products" in products
    
    async def test_mock_webinar_service(self):
        """Test mock webinar service functionality."""
        from tests.dependencies import MockWebinarService, get_test_settings
        
        settings = get_test_settings()
        # MockWebinarService needs both session and settings
        service = MockWebinarService(session=None, settings=settings)
        
        # Test basic functionality
        registrants = await service.get_webinar_registrants()
        assert isinstance(registrants, list)
    
    async def test_mock_chat_service(self):
        """Test mock chat service functionality."""
        from tests.dependencies import MockChatService, get_test_settings
        
        settings = get_test_settings()
        service = MockChatService(settings=settings)
        
        # Test basic functionality
        result = await service.test_connection()
        assert isinstance(result, dict)
        assert "status" in result


class TestConfiguration:
    """Test configuration and settings."""
    
    def test_test_settings_defaults(self):
        """Test that test settings have correct defaults."""
        settings = get_test_settings()
        
        assert settings.database_url == "sqlite+aiosqlite:///:memory:"
        assert settings.environment == "testing"
        assert settings.secret_key == "test_secret_key"
        assert settings.upload_dir == "test_uploads"
    
    def test_settings_validation(self):
        """Test that settings validation works."""
        from dependencies.config import Settings
        
        # Test valid settings
        settings = Settings(
            database_url="sqlite:///test.db",
            secret_key="test_key",
            environment="test"
        )
        assert settings.database_url == "sqlite:///test.db"
        assert settings.secret_key == "test_key"
        assert settings.environment == "test"


class TestDatabaseDependencies:
    """Test database dependency functions."""
    
    def test_create_database_engine(self):
        """Test database engine creation."""
        from dependencies.config import Settings
        from dependencies.database import create_database_engine
        
        settings = Settings(
            database_url="sqlite+aiosqlite:///:memory:",
            secret_key="test_key",
            environment="test"
        )
        
        engine = create_database_engine(settings)
        assert engine is not None
    
    def test_create_session_factory(self):
        """Test session factory creation."""
        from dependencies.config import Settings
        from dependencies.database import create_database_engine, create_session_factory
        
        settings = Settings(
            database_url="sqlite+aiosqlite:///:memory:",
            secret_key="test_key",
            environment="test"
        )
        
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)
        assert session_factory is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
