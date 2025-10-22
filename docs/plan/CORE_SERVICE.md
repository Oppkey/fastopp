# Core Service Flexibility Plan

We recently moved these services into core/services:
- auth
- storage  
- template_context

In the future, we plan to make these services more flexible so that they can be used across a wider range of applications.

FastOpp is a stack around FastAPI. We can assume that SQLite is available for development, same as Django, and that we will ship with SQLAdmin. The goal is to create a Django-like experience for FastAPI.

## 🎯 Current Problems

### 1. **Hard-Coded Dependencies**
- **Database coupling**: `from db import AsyncSessionLocal`
- **Model coupling**: `from models import User`
- **Session coupling**: Assumes specific session structure
- **Environment coupling**: Hard-coded environment variable names

### 2. **Application-Specific Logic**
- **User model assumptions**: Assumes specific user fields (`is_staff`, `is_superuser`)
- **Permission system**: Hard-coded permission checks
- **JWT payload structure**: Specific to this application
- **Auth patterns**: Assumes specific authentication flows

### 3. **Configuration Assumptions**
- **Environment variables**: Hard-coded env var names
- **Database schema**: Assumes specific schema structure
- **Session structure**: Assumes specific session patterns

## 🚀 Flexibility Plan

### Phase 1: Abstract Interfaces (Weeks 1-2)

#### **1.1 Create Abstract Base Classes**

```python
# core/services/interfaces.py
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List
from fastapi import Request

class UserModel(ABC):
    """Abstract user model interface"""
    
    @abstractmethod
    def get_id(self) -> Any:
        pass
    
    @abstractmethod
    def get_email(self) -> str:
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        pass
    
    @abstractmethod
    def has_permission(self, permission: str) -> bool:
        pass

class DatabaseSession(ABC):
    """Abstract database session interface"""
    
    @abstractmethod
    async def execute(self, query) -> Any:
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        pass

class AuthProvider(ABC):
    """Abstract authentication provider"""
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> Optional[UserModel]:
        pass
    
    @abstractmethod
    async def get_user(self, user_id: Any) -> Optional[UserModel]:
        pass
    
    @abstractmethod
    def create_token(self, user: UserModel) -> str:
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        pass
```

#### **1.2 Refactor Auth Service**

```python
# core/services/auth/flexible.py
class FlexibleAuthService:
    """Flexible authentication service with dependency injection"""
    
    def __init__(
        self,
        user_model: Type[UserModel],
        session_factory: Callable[[], DatabaseSession],
        auth_provider: AuthProvider,
        permission_checker: Optional[PermissionChecker] = None
    ):
        self.user_model = user_model
        self.session_factory = session_factory
        self.auth_provider = auth_provider
        self.permission_checker = permission_checker or DefaultPermissionChecker()
    
    async def get_current_user(self, request: Request) -> Optional[UserModel]:
        """Get current user from request"""
        # Implementation using injected dependencies
        pass
    
    async def require_permission(self, permission: str, user: UserModel) -> bool:
        """Check if user has required permission"""
        return self.permission_checker.check_permission(permission, user)
```

### Phase 2: Configuration System (Weeks 3-4)

#### **2.1 Create Configuration Framework**

```python
# core/services/config.py
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AuthConfig(BaseModel):
    """Authentication configuration"""
    secret_key: str
    token_expire_minutes: int = 30
    cookie_name: str = "access_token"
    session_key: str = "token"
    user_attributes: Dict[str, str] = {
        "is_superuser": "is_superuser",
        "is_staff": "is_staff",
        "user_email": "user_email",
        "user_group": "group"
    }

class StorageConfig(BaseModel):
    """Storage configuration"""
    storage_type: str = "filesystem"
    upload_dir: str = "static/uploads"
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_bucket: Optional[str] = None
    s3_endpoint_url: Optional[str] = None

class TemplateContextConfig(BaseModel):
    """Template context configuration"""
    auth_cookie_name: str = "access_token"
    session_token_key: str = "token"
    user_attributes: Dict[str, str] = {
        "is_superuser": "is_superuser",
        "is_staff": "is_staff",
        "user_email": "user_email",
        "user_group": "group"
    }
```

#### **2.2 Environment-Based Configuration**

```python
# core/services/config.py
class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment and config file"""
        # Load from environment variables
        # Load from config file if provided
        # Merge with defaults
        pass
    
    def get_auth_config(self) -> AuthConfig:
        """Get authentication configuration"""
        pass
    
    def get_storage_config(self) -> StorageConfig:
        """Get storage configuration"""
        pass
```

### Phase 3: Dependency Injection (Weeks 5-6)

#### **3.1 Create Service Factory**

```python
# core/services/factory.py
class ServiceFactory:
    """Factory for creating configured services"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def create_auth_service(
        self,
        user_model: Type[UserModel],
        session_factory: Callable[[], DatabaseSession]
    ) -> FlexibleAuthService:
        """Create configured authentication service"""
        auth_config = self.config_manager.get_auth_config()
        auth_provider = self._create_auth_provider(auth_config)
        permission_checker = self._create_permission_checker(auth_config)
        
        return FlexibleAuthService(
            user_model=user_model,
            session_factory=session_factory,
            auth_provider=auth_provider,
            permission_checker=permission_checker
        )
    
    def create_storage_service(self) -> StorageInterface:
        """Create configured storage service"""
        storage_config = self.config_manager.get_storage_config()
        return self._create_storage_backend(storage_config)
    
    def create_template_context_provider(self) -> TemplateContextProvider:
        """Create configured template context provider"""
        template_config = self.config_manager.get_template_context_config()
        return TemplateContextProvider(
            auth_cookie_name=template_config.auth_cookie_name,
            session_token_key=template_config.session_token_key,
            user_attributes=template_config.user_attributes
        )
```

#### **3.2 FastAPI Integration**

```python
# core/services/integration.py
from fastapi import FastAPI, Depends

class FastOppCore:
    """FastOpp core services integration"""
    
    def __init__(self, app: FastAPI, config_manager: ConfigManager):
        self.app = app
        self.config_manager = config_manager
        self.service_factory = ServiceFactory(config_manager)
        self._setup_services()
    
    def _setup_services(self):
        """Setup core services with dependency injection"""
        # Register services with FastAPI dependency injection
        pass
    
    def get_auth_service(self) -> FlexibleAuthService:
        """Get authentication service"""
        pass
    
    def get_storage_service(self) -> StorageInterface:
        """Get storage service"""
        pass
```

### Phase 4: Default Implementations (Weeks 7-8)

#### **4.1 SQLModel Integration**

```python
# core/services/implementations/sqlmodel.py
from sqlmodel import SQLModel
from core.services.interfaces import UserModel, DatabaseSession

class SQLModelUser(UserModel):
    """SQLModel user implementation"""
    
    def __init__(self, user: SQLModel):
        self.user = user
    
    def get_id(self) -> Any:
        return self.user.id
    
    def get_email(self) -> str:
        return self.user.email
    
    def is_active(self) -> bool:
        return self.user.is_active
    
    def has_permission(self, permission: str) -> bool:
        # Implement permission checking logic
        pass

class SQLModelSession(DatabaseSession):
    """SQLModel session implementation"""
    
    def __init__(self, session):
        self.session = session
    
    async def execute(self, query):
        return await self.session.execute(query)
    
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
```

#### **4.2 Default Permission System**

```python
# core/services/implementations/permissions.py
class DefaultPermissionChecker:
    """Default permission checking implementation"""
    
    def check_permission(self, permission: str, user: UserModel) -> bool:
        """Check if user has permission"""
        if permission == "admin":
            return user.has_permission("is_superuser")
        elif permission == "staff":
            return user.has_permission("is_staff") or user.has_permission("is_superuser")
        elif permission == "user":
            return user.is_active()
        return False
```

### Phase 5: Migration Strategy (Weeks 9-10)

#### **5.1 Backward Compatibility**

```python
# core/services/legacy.py
class LegacyAuthService:
    """Legacy authentication service for backward compatibility"""
    
    def __init__(self):
        # Initialize with current hard-coded dependencies
        pass
    
    def create_user_token(self, user: User) -> str:
        """Legacy method for backward compatibility"""
        # Use new flexible service internally
        pass
```

#### **5.2 Gradual Migration**

```python
# core/services/migration.py
class MigrationHelper:
    """Helper for migrating to flexible services"""
    
    @staticmethod
    def create_legacy_compatible_service():
        """Create service compatible with current implementation"""
        # Create flexible service with current app's dependencies
        pass
    
    @staticmethod
    def migrate_auth_service():
        """Migrate authentication service"""
        # Step-by-step migration process
        pass
```

## 📋 Implementation Checklist

### Phase 1: Abstract Interfaces
- [ ] Create abstract base classes for UserModel, DatabaseSession, AuthProvider
- [ ] Refactor auth service to use dependency injection
- [ ] Create flexible authentication service
- [ ] Update template context to use abstract interfaces

### Phase 2: Configuration System
- [ ] Create configuration models (AuthConfig, StorageConfig, TemplateContextConfig)
- [ ] Implement ConfigManager for centralized configuration
- [ ] Add environment variable support
- [ ] Add configuration file support

### Phase 3: Dependency Injection
- [ ] Create ServiceFactory for service creation
- [ ] Implement FastAPI integration
- [ ] Add dependency injection support
- [ ] Create service registration system

### Phase 4: Default Implementations
- [ ] Create SQLModel integration
- [ ] Implement default permission system
- [ ] Add default storage implementations
- [ ] Create default template context provider

### Phase 5: Migration Strategy
- [ ] Implement backward compatibility layer
- [ ] Create migration helpers
- [ ] Update existing applications
- [ ] Test migration process

## 🎯 Expected Outcomes

### **Flexibility Achieved:**
1. **Database Agnostic**: Works with any database backend
2. **Model Agnostic**: Works with any user model
3. **Permission Flexible**: Configurable permission system
4. **Environment Flexible**: Works in any environment
5. **Framework Flexible**: Can be used in any FastAPI application

### **Benefits:**
1. **Reusable**: Core services can be used across different FastOpp applications
2. **Configurable**: Easy to customize for different use cases
3. **Testable**: Easy to mock and test
4. **Maintainable**: Clear separation of concerns
5. **Extensible**: Easy to add new features

### **Usage Examples:**
```python
# Different applications can use different configurations
app1 = FastOppCore(app, ConfigManager("app1_config.yaml"))
app2 = FastOppCore(app, ConfigManager("app2_config.yaml"))

# Different user models
class CustomUser(UserModel):
    # Custom implementation
    pass

# Different permission systems
class CustomPermissionChecker:
    # Custom permission logic
    pass
```

This plan will make the core services truly flexible and reusable across a wide range of FastOpp applications while maintaining backward compatibility.