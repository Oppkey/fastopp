# Authentication System

This FastAPI application includes a **unified authentication system** that provides seamless integration between SQLAdmin and application authentication. The system uses a **single JWT-based approach** that works across all components:

- **Unified JWT Authentication** - Single token system for all authentication
- **SQLAdmin Integration** - Login to admin panel automatically authenticates the entire application
- **Cookie-based Sessions** - Secure httpOnly cookies with JWT tokens
- **Group-based Permissions** - Advanced permission system with role-based access control
- **Seamless User Experience** - Login once, access everything

## Architecture Overview

The authentication system uses a **unified services architecture** with a single authentication service that handles both SQLAdmin and application authentication.

### Structure

```
services/auth/
├── __init__.py          # Unified auth exports
├── core.py              # JWT token creation/verification
├── admin.py             # SQLAdmin authentication backend
└── dependencies.py     # FastAPI dependencies (for demo mode)
```

## Components

### `services/auth/core.py`
Contains the unified JWT-based authentication logic:

- `create_user_token()` - Create JWT tokens with user permissions
- `verify_token()` - Verify JWT tokens with secret key
- `get_current_user_from_cookies()` - Get authenticated user from cookies
- `get_current_staff_or_admin_from_cookies()` - Get staff/admin from cookies
- `get_current_superuser_from_cookies()` - Get superuser from cookies
- `get_secret_key()` - Get secret key from environment
- `get_token_expire_minutes()` - Get token expiration time

### `services/auth/admin.py`
Manages SQLAdmin authentication with unified JWT integration:

- `AdminAuth` - SQLAdmin authentication backend
- **Unified Login** - Creates JWT token on SQLAdmin login
- **Cookie Integration** - Sets application cookie for seamless access
- **Permission Verification** - Validates user permissions for admin access

### `services/auth/dependencies.py`
Provides FastAPI dependency injection support:

- `get_current_user()` - FastAPI dependency for user authentication
- `get_current_staff_or_admin()` - FastAPI dependency for staff/admin
- `get_current_superuser()` - FastAPI dependency for superuser

## Unified Authentication Experience

The system provides a **seamless authentication experience** where logging into SQLAdmin automatically authenticates you for the entire application.

### How It Works

1. **Login to SQLAdmin** at `/admin/`
2. **JWT token created** with your user permissions
3. **Cookie set** for application authentication
4. **Access protected pages** like `/oppman/`, `/protected/` without additional login

### Access Admin Panel

1. **Visit**: http://localhost:8000/admin/
2. **Login with any staff or superuser account**:
   - Superuser: `admin@example.com` / `admin123`
   - Marketing: `marketing@example.com` / `test123`
   - Sales: `sales@example.com` / `test123`
   - Support: `staff@example.com` / `test123`
3. **Automatic Application Access** - You're now logged into the entire system!

### Advanced Permission System

The system implements a **group-based permission system** with multiple permission levels:

#### **Permission Levels**

| Group | Products | Webinars | Users | Audit Logs | Description |
|-------|----------|----------|-------|------------|-------------|
| **Superuser** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | Complete admin access |
| **Marketing** | ✅ Full | ✅ Full | ❌ None | ❌ None | Can manage products and webinars |
| **Sales** | ✅ Full | ✅ Assigned | ❌ None | ❌ None | Can manage products, view assigned webinars |
| **Support** | ✅ Full | ❌ None | ❌ None | ❌ None | Can only manage products |
| **Regular Users** | ❌ None | ❌ None | ❌ None | ❌ None | No admin access |

#### **Action-Based Permissions**

- **Create**: Only superusers can create products, marketing can create webinars
- **Edit**: Marketing can edit all webinars, sales can edit assigned webinars
- **Delete**: Only superusers can delete products
- **View**: Group-based data filtering (sales see only assigned webinars)

#### **Data Filtering by Group**

- **Marketing users**: See all webinar registrants
- **Sales users**: See only their assigned registrants
- **Support users**: See only public registrants
- **Superusers**: See all registrants

### Features

- ✅ **Session-based authentication**
- ✅ **Secure password verification**
- ✅ **Group-based permission system**
- ✅ **Model-specific access control**
- ✅ **Action-based permissions (CRUD)**
- ✅ **Data filtering by user group**
- ✅ **Database user lookup**
- ✅ **User management interface**
- ✅ **Audit trail (superuser only)**

## JWT Token System

The application uses **unified JWT tokens** that work across all authentication scenarios.

### Token Features

- **Cryptographic Security** - Signed with secret key
- **Automatic Expiration** - Configurable token lifetime
- **Rich Payload** - Contains user permissions and metadata
- **Cookie Integration** - Stored in secure httpOnly cookies
- **Cross-Component** - Works for SQLAdmin and application routes

### Token Configuration

Set these environment variables in your `.env` file:

```env
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Token Payload

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "is_staff": true,
  "is_superuser": false,
  "exp": 1234567890
}
```

## Usage

### Importing Authentication Components

```python
# Unified authentication system
from services.auth import (
    create_user_token,
    get_current_user_from_cookies,
    get_current_staff_or_admin_from_cookies,
    get_current_superuser_from_cookies,
    AdminAuth
)

# For FastAPI dependency injection (demo mode)
from services.auth.dependencies import (
    get_current_user,
    get_current_staff_or_admin,
    get_current_superuser
)
```

### Route Protection

#### Base Assets Mode (Direct Function Calls)

```python
from services.auth import get_current_staff_or_admin_from_cookies

@router.get("/protected")
async def protected_route(request: Request):
    user = await get_current_staff_or_admin_from_cookies(request)
    return {"message": f"Hello {user.email}"}
```

#### Demo Mode (Dependency Injection)

```python
from fastapi import Depends
from services.auth.dependencies import get_current_staff_or_admin

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_staff_or_admin)):
    return {"message": f"Hello {current_user.email}"}
```

## Migration to Unified System

The authentication system has been completely restructured to provide a unified experience:

### Old Structure (Multiple Systems)
- `auth/` - Separate auth system
- `base_assets/auth/` - Base assets auth system  
- `demo_assets/auth/` - Demo assets auth system
- `demo_assets/dependencies/auth.py` - Dependency injection auth

### New Structure (Unified System)
- `services/auth/` - Single unified authentication service
- **SQLAdmin Integration** - Automatic JWT token creation on admin login
- **Seamless Experience** - Login once, access everything

## Benefits

1. **Unified Authentication**: Single login works across all components
2. **Eliminated Duplication**: No more multiple auth systems to maintain
3. **Better Security**: Consistent JWT tokens across all authentication
4. **Seamless UX**: Login to SQLAdmin automatically authenticates entire app
5. **Easier Maintenance**: Single authentication service to maintain
6. **Flexible Integration**: Works with both direct calls and dependency injection

## Test Data

The application comes with pre-loaded test data for authentication testing:

### Users

#### **Superusers (Full Access)**

- `admin@example.com` / `admin123`
- `admin2@example.com` / `test123`

#### **Marketing Users (Products + Webinars)**

- `marketing@example.com` / `test123`
- `marketing2@example.com` / `test123`

#### **Sales Users (Products + Assigned Webinars)**

- `sales@example.com` / `test123`
- `sales2@example.com` / `test123`

#### **Support Users (Products Only)**

- `staff@example.com` / `test123`
- `support@example.com` / `test123`

#### **Regular Users (No Admin Access)**

- `user@example.com` / `test123`
- `demo@example.com` / `test123`

## Testing

To test the unified authentication system:

```bash
uv run python -c "from services.auth import *; print('Unified auth system works')"
```

### Test Authentication Flow

1. **Login to SQLAdmin**: Visit `/admin/` and login with test credentials
2. **Verify Unified Access**: Visit `/oppman/` or `/protected/` - no additional login needed!
3. **Test Permissions**: Try accessing different sections based on user role
4. **Test JWT Tokens**: Verify JWT tokens work across all components
5. **Test Cookie Integration**: Verify httpOnly cookies are set correctly

## Security Features

### Unified Security

- **JWT Tokens**: Cryptographically signed tokens with secret key
- **HttpOnly Cookies**: Secure cookie storage prevents XSS attacks
- **Automatic Expiration**: Configurable token lifetime
- **Permission Validation**: Server-side permission checks
- **Cross-Component Security**: Same security model across all components

### Best Practices

- Use strong, unique SECRET_KEY for production
- Set appropriate ACCESS_TOKEN_EXPIRE_MINUTES
- Use HTTPS in production (secure cookie flag)
- Implement rate limiting for login attempts
- Log authentication events for audit purposes
- Regular security updates and token rotation

## Implementation Details

### Unified JWT Authentication

The system uses a single JWT-based approach for:

- **SQLAdmin Authentication**: Creates JWT token on admin login
- **Application Authentication**: Uses same JWT token for all routes
- **Cookie Integration**: Stores JWT in secure httpOnly cookies
- **Permission System**: JWT payload contains user permissions
- **Cross-Component**: Works seamlessly across all components

### SQLAdmin Integration

The SQLAdmin authentication backend:

- **Validates credentials** against database
- **Creates JWT token** with user permissions
- **Sets application cookie** for seamless access
- **Verifies permissions** for admin panel access
- **Handles logout** by clearing JWT token

### Cookie-Based Sessions

The system uses secure cookies for:

- **HttpOnly storage** - Prevents XSS attacks
- **Automatic expiration** - Configurable token lifetime
- **Cross-route access** - Same token works everywhere
- **Permission persistence** - User permissions in JWT payload

### Permission System

The permission system implements:

- **Group-based access control**: Users belong to groups with different permissions
- **Model-specific permissions**: Different models have different access rules
- **Action-based permissions**: Create, read, update, delete permissions
- **Data filtering**: Users see different data based on their group
- **Audit trail**: Audit logs for tracking changes (superuser only)
- **Session-based permissions**: Permissions stored in session for performance

### Database Models

#### **User Model**

```python
class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    group: Optional[str] = Field(default=None)  # marketing, sales, support, etc.
```

#### **WebinarRegistrants Model**

```python
class WebinarRegistrants(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    company: Optional[str] = Field(max_length=100, default=None, nullable=True)
    webinar_title: str = Field(max_length=200, nullable=False)
    webinar_date: datetime = Field(nullable=False)
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="registered")  # registered, attended, cancelled, no_show
    assigned_sales_rep: Optional[str] = Field(default=None, nullable=True)
    group: Optional[str] = Field(default=None)  # marketing, sales, support
    is_public: bool = Field(default=True)  # Whether this registration is visible to all
    notes: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### **AuditLog Model**

```python
class AuditLog(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    action: str = Field(max_length=50)  # create, update, delete, view
    model_name: str = Field(max_length=50)  # products, webinar_registrants, users
    record_id: str = Field(max_length=50)
    changes: Optional[str] = Field(default=None, nullable=True)  # JSON of changes
    ip_address: Optional[str] = Field(default=None, nullable=True)
    user_agent: Optional[str] = Field(default=None, nullable=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## Extension Ideas

The permission system can be easily extended with:

1. **Role-Based Permissions**: Add roles like "webinar_manager", "product_editor"
2. **Permission Groups**: Create permission groups for different departments
3. **Time-Based Permissions**: Permissions that expire
4. **API Permissions**: Decorators for API endpoint permissions
5. **Dynamic Permissions**: Load permissions from database
6. **Hierarchical Permissions**: Permission inheritance system

## Next Steps

After setting up authentication:

1. **Configure User Groups**: Set up appropriate permission levels
2. **Test Permissions**: Verify access control works correctly
3. **Customize UI**: Adapt admin interface for your needs
4. **Add Audit Logging**: Track user actions and changes

For more information, see:
- [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) - PostgreSQL setup and database configuration
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
- [FEATURES.md](FEATURES.md) - Application features and usage
