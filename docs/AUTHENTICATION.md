# Authentication System

This FastAPI application includes a **unified authentication system** that provides seamless integration between SQLAdmin and application authentication. The system uses a **single JWT-based approach** that works across all components:

- **Unified JWT Authentication** - Single token system for all authentication
- **SQLAdmin Integration** - Login to admin panel automatically authenticates the entire application
- **Cookie-based Sessions** - Secure httpOnly cookies with JWT tokens
- **Group-based Permissions** - Advanced permission system with role-based access control
- **Seamless User Experience** - Login once, access everything

## JWT vs Cookie-based Authentication

### **Understanding the Difference**

**JWT (JSON Web Token)** is a **token format** - a way to encode data (like user info) into a secure, signed string:
```javascript
// JWT token example
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

**Cookie-based Authentication with JWT** is a **storage mechanism** - using HTTP cookies to store the JWT token:
```javascript
// Cookie storage
document.cookie = "access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...; HttpOnly; Secure; SameSite=Strict"
```

### **Our System Uses Both Approaches**

#### **Cookie-based JWT (Web Applications)**
```python
# Server sets JWT in cookie
response.set_cookie(key="access_token", value=jwt_token, httponly=True)
# Browser automatically sends: Cookie: access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
- ✅ **Automatic**: Browser handles sending cookies
- ✅ **Secure**: HttpOnly cookies prevent XSS attacks
- ✅ **Simple**: No JavaScript needed to manage tokens
- ❌ **Limited**: Only works in browsers, not mobile apps

#### **Header-based JWT (Mobile/API)**
```python
# Client sends JWT in Authorization header
headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
```
- ✅ **Universal**: Works everywhere (mobile, web, API clients)
- ✅ **Flexible**: Client controls when/how to send tokens
- ✅ **Stateless**: No server-side session storage needed
- ❌ **Manual**: Client must manage token storage/sending

### **Key Point: Same JWT Token, Different Storage**

The JWT token itself is identical - we just change **where we store it** and **how we send it** based on the client type:

- **Web clients** → Cookie-based JWT (automatic, secure)
- **Mobile clients** → Header-based JWT (flexible, universal)
- **Same JWT token** → Works for both storage methods!

## Architecture Overview

The authentication system uses a **unified services architecture** with a single authentication service that handles both SQLAdmin and application authentication.

### Structure

```text
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

The system provides a **seamless authentication experience** where logging in through any method automatically authenticates you for the entire application.

### How It Works

1. **Login via form** at `/login` OR **Login to SQLAdmin** at `/admin/`
2. **JWT token created** with your user permissions
3. **Both cookie and session set** for unified authentication
4. **Access protected pages** like `/oppman/`, `/admin/` without additional login
5. **Unified logout** clears authentication across all interfaces

### Access Methods

#### **Method 1: Login Form (Recommended)**
1. **Visit**: http://localhost:8000/login
2. **Login with any staff or superuser account**:
   - Superuser: `admin@example.com` / `admin123`
   - Marketing: `marketing@example.com` / `test123`
   - Sales: `sales@example.com` / `test123`
   - Support: `staff@example.com` / `test123`
3. **Automatic Access** - You're now logged into both SQLAdmin and application routes!

#### **Method 2: Direct SQLAdmin Access**
1. **Visit**: http://localhost:8000/admin/
2. **Login with same credentials** as above
3. **Automatic Application Access** - You're now logged into the entire system!

### Unified Logout

The system provides **unified logout** that works across all interfaces:

- **SQLAdmin Logout**: Custom logout button in top-right corner (replaces non-working default)
- **Application Logout**: Logout button in `/oppman/` interface
- **Direct Logout**: Visit `/logout` to log out of everything
- **Complete Logout**: Clears both session tokens and cookies

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
    get_current_user_from_authorization_header,
    get_current_staff_or_admin_from_authorization_header,
    get_current_superuser_from_authorization_header,
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

### API Authentication for Mobile Apps

The system supports **JWT Authorization header authentication** for mobile applications like Flutter, React Native, or any API client.

#### **API Authentication Methods**

```python
# For API routes that need JWT header authentication
from services.auth import get_current_user_from_authorization_header

@router.get("/api/protected")
async def api_protected_route(request: Request):
    user = await get_current_user_from_authorization_header(request)
    return {"message": f"Hello {user.email}", "user_id": str(user.id)}
```

#### **Mobile App Integration Examples**

##### **Flutter Mobile & Web**
```dart
// Flutter HTTP client with JWT authentication (works for mobile and web)
class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  String? _token;

  // Login and get JWT token
  Future<bool> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _token = data['access_token'];
      
      // Store token securely
      // Mobile: Use flutter_secure_storage
      // Web: Use shared_preferences or localStorage
      await _storeToken(_token!);
      return true;
    }
    return false;
  }

  // Make authenticated API calls
  Future<Map<String, dynamic>> getProtectedData() async {
    final token = await _getStoredToken();
    if (token == null) throw Exception('Not authenticated');
    
    final response = await http.get(
      Uri.parse('$baseUrl/api/protected'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load data');
  }

  // Secure token storage (platform-specific)
  Future<void> _storeToken(String token) async {
    // Mobile: Use flutter_secure_storage
    // Web: Use shared_preferences
    // Implementation depends on your storage preference
  }

  Future<String?> _getStoredToken() async {
    // Retrieve token from secure storage
    // Implementation depends on your storage preference
    return _token;
  }
}
```

##### **React Web Application**
```javascript
// React API service with JWT authentication
class ApiService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
    this.token = localStorage.getItem('access_token');
  }

  // Login and get JWT token
  async login(email, password) {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        this.token = data.access_token;
        localStorage.setItem('access_token', this.token);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }

  // Make authenticated API calls
  async getProtectedData() {
    if (!this.token) {
      throw new Error('Not authenticated');
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/protected`, {
        headers: {
          'Authorization': `Bearer ${this.token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        return await response.json();
      }
      throw new Error('Failed to load data');
    } catch (error) {
      console.error('API call error:', error);
      throw error;
    }
  }

  // Logout (remove token)
  logout() {
    this.token = null;
    localStorage.removeItem('access_token');
  }
}

// React component usage
function App() {
  const [apiService] = useState(new ApiService());
  const [user, setUser] = useState(null);

  const handleLogin = async (email, password) => {
    const success = await apiService.login(email, password);
    if (success) {
      // Get user info
      const userData = await apiService.getProtectedData();
      setUser(userData);
    }
  };

  return (
    <div>
      {user ? (
        <div>Welcome, {user.email}!</div>
      ) : (
        <LoginForm onLogin={handleLogin} />
      )}
    </div>
  );
}
```

##### **React Native**
```javascript
// React Native with AsyncStorage for token persistence
import AsyncStorage from '@react-native-async-storage/async-storage';

class ApiService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
    this.token = null;
  }

  async login(email, password) {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        this.token = data.access_token;
        await AsyncStorage.setItem('access_token', this.token);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }

  async getProtectedData() {
    if (!this.token) {
      this.token = await AsyncStorage.getItem('access_token');
    }
    
    if (!this.token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseUrl}/api/protected`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      return await response.json();
    }
    throw new Error('Failed to load data');
  }
}
```

#### **API Endpoints for Mobile Apps**

You'll need to create API endpoints that return JWT tokens:

```python
# API authentication endpoints
@router.post("/api/auth/login")
async def api_login(email: str, password: str):
    # Validate credentials
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    token = create_user_token(user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": get_token_expire_minutes() * 60,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser
        }
    }

@router.post("/api/auth/logout")
async def api_logout():
    # For JWT tokens, logout is handled client-side
    # (just remove the token from storage)
    return {"message": "Logged out successfully"}

@router.get("/api/auth/me")
async def get_current_user_info(request: Request):
    user = await get_current_user_from_authorization_header(request)
    return {
        "id": str(user.id),
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser
    }
```

#### **Hybrid Authentication Routes**

For routes that support both web (cookies) and API (headers) authentication:

```python
from services.auth import get_current_user_from_cookies, get_current_user_from_authorization_header

async def get_current_user_hybrid(request: Request) -> User:
    """Get current user from either cookies or Authorization header"""
    try:
        # Try Authorization header first (for API clients)
        return await get_current_user_from_authorization_header(request)
    except HTTPException:
        # Fall back to cookies (for web clients)
        return await get_current_user_from_cookies(request)

@router.get("/api/hybrid-protected")
async def hybrid_protected_route(request: Request):
    user = await get_current_user_hybrid(request)
    return {"message": f"Hello {user.email}"}
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

### **For Web Applications**
1. **Unified Authentication**: Single login works across all components
2. **Eliminated Duplication**: No more multiple auth systems to maintain
3. **Better Security**: Consistent JWT tokens across all authentication
4. **Seamless UX**: Login to SQLAdmin automatically authenticates entire app
5. **Easier Maintenance**: Single authentication service to maintain
6. **Flexible Integration**: Works with both direct calls and dependency injection

### **For Mobile & Web Applications**
1. **JWT Token Support**: Standard Authorization header authentication
2. **Stateless Authentication**: No server-side session storage required
3. **Cross-Platform**: Works with Flutter (mobile & web), React (web), React Native (mobile), iOS, Android
4. **Secure Storage**: Tokens stored securely (keychain on mobile, localStorage on web)
5. **Automatic Expiration**: Built-in token expiration for security
6. **Hybrid Support**: Same endpoints work for web, mobile, and API clients
7. **Universal HTTP**: Standard HTTP client libraries work across all platforms

### **For API Development**
1. **RESTful Authentication**: Standard Bearer token authentication
2. **Multiple Client Support**: Web, mobile, and API clients use same system
3. **Flexible Endpoints**: Choose between cookie-based or header-based auth
4. **Easy Integration**: Simple HTTP client implementation
5. **Token Refresh**: Built-in token expiration and refresh patterns
6. **Role-Based Access**: Same permission system across all client types

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

#### **Web Authentication Testing**
1. **Login via Form**: Visit `/login` and login with test credentials
2. **Verify Unified Access**: Visit `/oppman/` and `/admin/` - no additional login needed!
3. **Test SQLAdmin Logout**: Use the red logout button in top-right corner of SQLAdmin
4. **Test Application Logout**: Use the logout button in `/oppman/` interface
5. **Test Direct Logout**: Visit `/logout` to test direct logout
6. **Test Permissions**: Try accessing different sections based on user role
7. **Test JWT Tokens**: Verify JWT tokens work across all components
8. **Test Cookie Integration**: Verify httpOnly cookies are set correctly

#### **API Authentication Testing**
```bash
# Test API login (you'll need to create these endpoints)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Test API authentication with JWT token
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/protected

# Test hybrid authentication (supports both cookies and headers)
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/hybrid-protected
```

#### **Mobile App Testing (Flutter)**
```dart
// Test login
final apiService = ApiService();
bool loggedIn = await apiService.login('admin@example.com', 'admin123');
print('Login successful: $loggedIn');

// Test authenticated API call
try {
  final data = await apiService.getProtectedData();
  print('Protected data: $data');
} catch (e) {
  print('Error: $e');
}
```

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

## Template Context System

The application includes a **flexible template context system** that automatically provides authentication state to all templates. This ensures consistent authentication UI across the application.

### Overview

The template context system (`services/template_context.py`) provides:

- **Automatic authentication state** - Templates always have access to user authentication status
- **Flexible configuration** - Works with different authentication systems
- **Backward compatibility** - Existing code continues to work unchanged
- **Future-proof design** - Easy to adapt to new authentication methods

### Basic Usage

The system automatically provides authentication context to templates:

```python
# In your route
from services.template_context import get_template_context

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    # Get authentication context
    auth_context = get_template_context(request)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Home Page",
        **auth_context  # Merges authentication state
    })
```

### Template Variables

The context system provides these variables to all templates:

```html
<!-- Authentication status -->
{% if is_authenticated %}
    <p>Welcome back!</p>
    <a href="/logout">Logout</a>
{% else %}
    <a href="/login">Login</a>
{% endif %}

<!-- User information -->
{% if user_email %}
    <p>Logged in as: {{ user_email }}</p>
{% endif %}

<!-- Permission checks -->
{% if is_superuser %}
    <a href="/admin">Admin Panel</a>
{% endif %}

{% if is_staff %}
    <a href="/management">Management</a>
{% endif %}
```

### Available Context Variables

| Variable | Type | Description |
|----------|------|-------------|
| `is_authenticated` | boolean | Whether user is logged in |
| `has_access_token` | boolean | Whether access token cookie exists |
| `has_session_token` | boolean | Whether session token exists |
| `current_user` | User object | Current user object (if available) |
| `is_superuser` | boolean | Whether user has superuser privileges |
| `is_staff` | boolean | Whether user has staff privileges |
| `user_email` | string | User's email address |
| `user_group` | string | User's group/role |

### Advanced Configuration

For different authentication systems, you can create custom context providers:

```python
from services.template_context import create_template_context_provider

# Custom provider for different auth system
auth_provider = create_template_context_provider(
    auth_cookie_name="jwt_token",           # Different cookie name
    session_token_key="auth_session",       # Different session key
    user_attributes={                       # Custom user attributes
        "is_admin": "admin",
        "user_name": "username",
        "user_role": "role"
    }
)

# Use in your route
auth_context = auth_provider.get_template_context(request)
```

### Integration with Header Template

The header template (`templates/partials/header.html`) uses the context system:

```html
<!-- Management dropdown - only shows when authenticated -->
{% if is_authenticated %}
<div class="relative group">
    <button onclick="toggleDropdown('management')">
        Management
    </button>
    <div id="management-dropdown" class="dropdown-menu">
        <a href="/admin/">Admin Panel</a>
        <a href="/oppman/">Oppman</a>
        <a href="/oppdemo/">Oppdemo</a>
    </div>
</div>
{% endif %}

<!-- Login/Logout button -->
{% if is_authenticated %}
    <a href="/logout" class="text-red-600">Logout</a>
{% else %}
    <a href="/login" class="text-blue-600">Login</a>
{% endif %}
```

### Benefits

1. **Consistent UI** - All templates have access to authentication state
2. **No manual context passing** - Authentication state is automatically available
3. **Flexible** - Works with different authentication systems
4. **Maintainable** - Centralized authentication context logic
5. **Reusable** - Can be used across multiple applications

### Troubleshooting

If authentication state isn't showing correctly:

1. **Check cookie names** - Ensure the auth system uses the expected cookie names
2. **Verify session data** - Check that session variables are being set correctly
3. **Test context provider** - Use the custom provider for different auth systems
4. **Check template logic** - Ensure templates are using the correct context variables

For more information, see:
- [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) - PostgreSQL setup and database configuration
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
- [FEATURES.md](FEATURES.md) - Application features and usage
