# Core Services Flexibility Implementation Roadmap

## 🎯 **Goal**
Transform the current tightly-coupled core services into flexible, reusable components that can be used across different FastOpp applications while maintaining backward compatibility.

## 📋 **Implementation Strategy**

### **Incremental Approach**
- **Phase-by-phase implementation** to avoid breaking existing functionality
- **Backward compatibility** maintained throughout the process
- **Gradual migration** allowing testing at each step
- **Real-world validation** with actual FastOpp applications

## 🚀 **Phase 1: Abstract Interfaces (Week 1-2)**

### **1.1 Create Abstract Base Classes**

**File: `core/services/interfaces.py`**
```python
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List
from fastapi import Request

class UserModel(ABC):
    """Abstract user model interface"""
    
    @abstractmethod
    def get_id(self) -> Any:
        """Get user ID"""
        pass
    
    @abstractmethod
    def get_email(self) -> str:
        """Get user email"""
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """Check if user is active"""
        pass
    
    @abstractmethod
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        pass

class DatabaseSession(ABC):
    """Abstract database session interface"""
    
    @abstractmethod
    async def execute(self, query) -> Any:
        """Execute database query"""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction"""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transaction"""
        pass

class AuthProvider(ABC):
    """Abstract authentication provider"""
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> Optional[UserModel]:
        """Authenticate user with credentials"""
        pass
    
    @abstractmethod
    async def get_user(self, user_id: Any) -> Optional[UserModel]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def create_token(self, user: UserModel) -> str:
        """Create authentication token"""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify authentication token"""
        pass

class PermissionChecker(ABC):
    """Abstract permission checker"""
    
    @abstractmethod
    def check_permission(self, permission: str, user: UserModel) -> bool:
        """Check if user has permission"""
        pass
```

### **1.2 Create Flexible Auth Service**

**File: `core/services/auth/flexible.py`**
```python
from typing import Type, Callable, Optional
from fastapi import Request, HTTPException, status
from ..interfaces import UserModel, DatabaseSession, AuthProvider, PermissionChecker

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
    
    async def get_current_user(self, request: Request) -> UserModel:
        """Get current user from request"""
        # Implementation using injected dependencies
        pass
    
    async def require_permission(self, permission: str, user: UserModel) -> bool:
        """Check if user has required permission"""
        return self.permission_checker.check_permission(permission, user)
```

### **1.3 Create Default Permission Checker**

**File: `core/services/auth/permissions.py`**
```python
from ..interfaces import UserModel, PermissionChecker

class DefaultPermissionChecker(PermissionChecker):
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

## 🚀 **Phase 2: Configuration System (Week 3-4)**

### **2.1 Create Configuration Models**

**File: `core/services/config.py`**
```python
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

class CoreConfig(BaseModel):
    """Core services configuration"""
    auth: AuthConfig
    storage: StorageConfig
    template_context: TemplateContextConfig
```

### **2.2 Create Configuration Manager**

**File: `core/services/config_manager.py`**
```python
import os
from typing import Optional
from .config import CoreConfig, AuthConfig, StorageConfig, TemplateContextConfig

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> CoreConfig:
        """Load configuration from environment and config file"""
        # Load from environment variables
        auth_config = AuthConfig(
            secret_key=os.getenv("SECRET_KEY", "dev_secret_key_change_in_production"),
            token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            cookie_name=os.getenv("AUTH_COOKIE_NAME", "access_token"),
            session_key=os.getenv("SESSION_TOKEN_KEY", "token")
        )
        
        storage_config = StorageConfig(
            storage_type=os.getenv("STORAGE_TYPE", "filesystem"),
            upload_dir=os.getenv("UPLOAD_DIR", "static/uploads"),
            s3_access_key=os.getenv("S3_ACCESS_KEY"),
            s3_secret_key=os.getenv("S3_SECRET_KEY"),
            s3_bucket=os.getenv("S3_BUCKET"),
            s3_endpoint_url=os.getenv("S3_ENDPOINT_URL")
        )
        
        template_config = TemplateContextConfig(
            auth_cookie_name=os.getenv("AUTH_COOKIE_NAME", "access_token"),
            session_token_key=os.getenv("SESSION_TOKEN_KEY", "token")
        )
        
        return CoreConfig(
            auth=auth_config,
            storage=storage_config,
            template_context=template_config
        )
    
    def get_auth_config(self) -> AuthConfig:
        """Get authentication configuration"""
        return self._config.auth
    
    def get_storage_config(self) -> StorageConfig:
        """Get storage configuration"""
        return self._config.storage
    
    def get_template_context_config(self) -> TemplateContextConfig:
        """Get template context configuration"""
        return self._config.template_context
```

## 🚀 **Phase 3: Service Factory (Week 5-6)**

### **3.1 Create Service Factory**

**File: `core/services/factory.py`**
```python
from typing import Type, Callable
from .config_manager import ConfigManager
from .interfaces import UserModel, DatabaseSession, AuthProvider, PermissionChecker
from .auth.flexible import FlexibleAuthService
from .auth.permissions import DefaultPermissionChecker
from .storage.factory import get_storage
from .template_context import TemplateContextProvider

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
    
    def create_storage_service(self):
        """Create configured storage service"""
        storage_config = self.config_manager.get_storage_config()
        return get_storage()  # Use existing storage factory
    
    def create_template_context_provider(self) -> TemplateContextProvider:
        """Create configured template context provider"""
        template_config = self.config_manager.get_template_context_config()
        return TemplateContextProvider(
            auth_cookie_name=template_config.auth_cookie_name,
            session_token_key=template_config.session_token_key,
            user_attributes=template_config.user_attributes
        )
    
    def _create_auth_provider(self, auth_config: AuthConfig) -> AuthProvider:
        """Create authentication provider"""
        # Implementation for creating auth provider
        pass
    
    def _create_permission_checker(self, auth_config: AuthConfig) -> PermissionChecker:
        """Create permission checker"""
        return DefaultPermissionChecker()
```

### **3.2 Create FastAPI Integration**

**File: `core/services/integration.py`**
```python
from fastapi import FastAPI, Depends
from .factory import ServiceFactory
from .config_manager import ConfigManager

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
    
    def get_auth_service(self):
        """Get authentication service"""
        return self.service_factory.create_auth_service(
            user_model=self._get_user_model(),
            session_factory=self._get_session_factory()
        )
    
    def get_storage_service(self):
        """Get storage service"""
        return self.service_factory.create_storage_service()
    
    def _get_user_model(self):
        """Get user model - to be implemented by application"""
        pass
    
    def _get_session_factory(self):
        """Get session factory - to be implemented by application"""
        pass
```

## 🚀 **Phase 4: Default Implementations (Week 7-8)**

### **4.1 SQLModel Integration**

**File: `core/services/implementations/sqlmodel.py`**
```python
from sqlmodel import SQLModel
from ..interfaces import UserModel, DatabaseSession

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
        # Implement permission checking logic based on user model
        if permission == "is_superuser":
            return getattr(self.user, "is_superuser", False)
        elif permission == "is_staff":
            return getattr(self.user, "is_staff", False)
        return False

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

### **4.2 Default Auth Provider**

**File: `core/services/implementations/auth_provider.py`**
```python
from typing import Optional, Dict, Any
from ..interfaces import UserModel, AuthProvider
from ..config import AuthConfig

class DefaultAuthProvider(AuthProvider):
    """Default authentication provider implementation"""
    
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
    
    async def authenticate(self, credentials: Dict[str, Any]) -> Optional[UserModel]:
        """Authenticate user with credentials"""
        # Implementation for authentication
        pass
    
    async def get_user(self, user_id: Any) -> Optional[UserModel]:
        """Get user by ID"""
        # Implementation for getting user
        pass
    
    def create_token(self, user: UserModel) -> str:
        """Create authentication token"""
        # Implementation for token creation
        pass
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify authentication token"""
        # Implementation for token verification
        pass
```

## 🚀 **Phase 5: Migration Strategy (Week 9-10)**

### **5.1 Backward Compatibility Layer**

**File: `core/services/legacy.py`**
```python
from ..auth.core import create_user_token, verify_token, get_current_user_from_cookies
from ..storage.factory import get_storage
from ..template_context import TemplateContextProvider

class LegacyAuthService:
    """Legacy authentication service for backward compatibility"""
    
    def __init__(self):
        # Initialize with current hard-coded dependencies
        pass
    
    def create_user_token(self, user) -> str:
        """Legacy method for backward compatibility"""
        return create_user_token(user)
    
    def verify_token(self, token: str):
        """Legacy method for backward compatibility"""
        return verify_token(token)
    
    async def get_current_user_from_cookies(self, request):
        """Legacy method for backward compatibility"""
        return await get_current_user_from_cookies(request)

class LegacyStorageService:
    """Legacy storage service for backward compatibility"""
    
    def __init__(self):
        self.storage = get_storage()
    
    def save_file(self, file_path: str, content: bytes):
        """Legacy method for backward compatibility"""
        return self.storage.save_file(file_path, content)
    
    def get_file_url(self, file_path: str):
        """Legacy method for backward compatibility"""
        return self.storage.get_file_url(file_path)

class LegacyTemplateContextProvider:
    """Legacy template context provider for backward compatibility"""
    
    def __init__(self):
        self.provider = TemplateContextProvider()
    
    def get_template_context(self, request):
        """Legacy method for backward compatibility"""
        return self.provider.get_template_context(request)
```

### **5.2 Migration Helper**

**File: `core/services/migration.py`**
```python
from .legacy import LegacyAuthService, LegacyStorageService, LegacyTemplateContextProvider
from .factory import ServiceFactory
from .config_manager import ConfigManager

class MigrationHelper:
    """Helper for migrating to flexible services"""
    
    @staticmethod
    def create_legacy_compatible_service():
        """Create service compatible with current implementation"""
        return {
            "auth": LegacyAuthService(),
            "storage": LegacyStorageService(),
            "template_context": LegacyTemplateContextProvider()
        }
    
    @staticmethod
    def migrate_auth_service():
        """Migrate authentication service"""
        # Step-by-step migration process
        pass
    
    @staticmethod
    def migrate_storage_service():
        """Migrate storage service"""
        # Step-by-step migration process
        pass
    
    @staticmethod
    def migrate_template_context_service():
        """Migrate template context service"""
        # Step-by-step migration process
        pass
```

## 📋 **Implementation Checklist**

### **Phase 1: Abstract Interfaces**
- [ ] Create `core/services/interfaces.py` with abstract base classes
- [ ] Create `core/services/auth/flexible.py` with FlexibleAuthService
- [ ] Create `core/services/auth/permissions.py` with DefaultPermissionChecker
- [ ] Test abstract interfaces with current implementation

### **Phase 2: Configuration System**
- [ ] Create `core/services/config.py` with configuration models
- [ ] Create `core/services/config_manager.py` with ConfigManager
- [ ] Test configuration loading from environment variables
- [ ] Test configuration loading from config files

### **Phase 3: Service Factory**
- [ ] Create `core/services/factory.py` with ServiceFactory
- [ ] Create `core/services/integration.py` with FastOppCore
- [ ] Test service creation with dependency injection
- [ ] Test FastAPI integration

### **Phase 4: Default Implementations**
- [ ] Create `core/services/implementations/sqlmodel.py` with SQLModel integration
- [ ] Create `core/services/implementations/auth_provider.py` with DefaultAuthProvider
- [ ] Test default implementations with current models
- [ ] Test default implementations with different models

### **Phase 5: Migration Strategy**
- [ ] Create `core/services/legacy.py` with backward compatibility layer
- [ ] Create `core/services/migration.py` with migration helpers
- [ ] Test backward compatibility with current application
- [ ] Test migration process with new applications

## 🎯 **Expected Outcomes**

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

This roadmap provides a clear, incremental path to transform your core services into flexible, reusable components while maintaining backward compatibility throughout the process.
