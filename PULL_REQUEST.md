# Pull Request: Environment Configuration & Unified Authentication System

## 🎯 **Summary**

This PR enhances the application's configuration system by adding environment variable support for key settings, improving debug functionality, and implementing a unified JWT-based authentication system that works seamlessly across SQLAdmin and application routes.

## 🚀 **Key Features Added**

### **1. Unified Authentication System**
- **JWT-Based Authentication**: Single authentication system for both SQLAdmin and application routes
- **Seamless Integration**: Login to SQLAdmin automatically authenticates for protected application pages
- **Cookie-Based Tokens**: Secure JWT tokens stored in HTTP cookies
- **Role-Based Access**: Support for user, staff, and superuser roles
- **Unified Logout**: Single logout clears authentication across all interfaces

### **2. LLM Model Configuration**
- **Environment Variable**: `OPENROUTER_LLM_MODEL` 
- **Default**: `meta-llama/llama-3.3-70b-instruct:free`
- **Usage**: Set in `.env` file to switch between different AI models
- **Examples**:
  ```bash
  OPENROUTER_LLM_MODEL=anthropic/claude-3.5-sonnet:free
  OPENROUTER_LLM_MODEL=openai/gpt-4o-mini:free
  OPENROUTER_LLM_MODEL=google/gemini-pro:free
  ```

### **3. Conditional Debug System**
- **Environment Variable**: `DEBUG` (default: `true`)
- **Smart Debug Output**: Debug print statements now respect the DEBUG setting
- **Performance**: No debug overhead when `DEBUG=false`
- **Services Updated**: Chat service and S3 storage now use conditional debug statements

### **4. Host and Port Configuration**
- **Environment Variables**: `HOST` and `PORT`
- **Defaults**: `HOST=0.0.0.0`, `PORT=8000`
- **Deployment Ready**: Works with cloud platforms (Heroku, Railway, Fly.io, etc.)
- **Files Updated**: `oppman.py`, `base_assets/main.py`, `scripts/production_start.py`

### **5. Enhanced Database Documentation**
- **SQLite Examples**: Added clear examples for SQLite configuration
- **Filename Customization**: Documentation on changing database filenames
- **Removed Untested**: Removed MySQL driver examples (not tested)
- **Better Guidance**: Clearer instructions for different database setups

## 📁 **Files Modified**

### **Authentication System**
- `services/auth/__init__.py` - Unified authentication exports
- `services/auth/core.py` - JWT authentication core functions
- `services/auth/admin.py` - SQLAdmin authentication backend
- `services/auth/dependencies.py` - FastAPI dependency injection
- `base_assets/routes/oppman.py` - Updated to use unified auth
- `base_assets/routes/auth.py` - Updated to use unified auth
- `admin/setup.py` - Updated to use unified auth backend

### **Templates & UI**
- `templates/index.html` - Updated home page with Oppman Panel and emergency access
- `templates/oppman.html` - Added logout button and fixed template errors
- `docs/AUTHENTICATION.md` - Comprehensive authentication documentation

### **Configuration Files**
- `dependencies/config.py` - Added HOST, PORT, debug settings
- `example.env` - Enhanced with new environment variables and examples

### **Service Files**
- `services/chat_service.py` - Added conditional debug statements and LLM model env var
- `services/storage/s3.py` - Added conditional debug statements

### **Server Files**
- `oppman.py` - Updated to use HOST/PORT environment variables
- `base_assets/main.py` - Updated to use HOST/PORT environment variables  
- `scripts/production_start.py` - Updated to use HOST/PORT environment variables

## 🔧 **Technical Details**

### **Unified Authentication System**
```python
# JWT Token Creation
def create_user_token(user: User) -> str:
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes)
    }
    return jwt.encode(token_data, secret_key, algorithm="HS256")

# SQLAdmin Integration
class AdminAuth:
    async def login(self, request: Request, form_data: OAuth2PasswordRequestForm):
        # ... authentication logic ...
        token = create_user_token(user)
        response.set_cookie(key="access_token", value=token, httponly=True)
        return response
```

### **Environment Variable Support**
```python
# New settings in dependencies/config.py
host: str = "0.0.0.0"
port: int = 8000
debug: bool = True
```

### **Conditional Debug Implementation**
```python
# Before (always prints)
print(f"DEBUG: Testing connection with API key: {api_key[:10]}...")

# After (conditional)
if settings.debug:
    print(f"DEBUG: Testing connection with API key: {api_key[:10]}...")
```

### **LLM Model Configuration**
```python
# Before (hardcoded)
LLM_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# After (environment variable with fallback)
LLM_MODEL = os.getenv("OPENROUTER_LLM_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
```

## 🎯 **Benefits**

### **For Authentication**
- **Single Sign-On**: Login once to SQLAdmin, access all protected routes
- **Unified Experience**: Seamless navigation between admin panel and application
- **Secure Tokens**: JWT-based authentication with proper expiration
- **Role-Based Access**: Granular permissions for different user types
- **Easy Logout**: Single logout clears authentication across all interfaces

### **For Developers**
- **Easy Model Switching**: Change AI models via environment variable
- **Debug Control**: Turn debug output on/off as needed
- **Port Flexibility**: Avoid port conflicts in development
- **Simplified Auth**: Single authentication system instead of multiple implementations

### **For Production**
- **Cloud Platform Ready**: Works with Heroku, Railway, Fly.io, etc.
- **Performance**: No debug overhead in production
- **Security**: Can bind to specific hosts for security
- **Unified Security**: Consistent authentication across all application components

### **For Documentation**
- **Clear Examples**: Better SQLite configuration examples
- **Database Flexibility**: Easy database filename changes
- **Removed Confusion**: Removed untested MySQL examples
- **Auth Documentation**: Comprehensive authentication system documentation

## 🧪 **Testing**

### **Authentication Testing**
```bash
# Test unified authentication
curl -c cookies.txt -b cookies.txt http://localhost:8000/login
# Login via form, then test protected routes
curl -b cookies.txt http://localhost:8000/oppman/
curl -b cookies.txt http://localhost:8000/admin/

# Test logout
curl -b cookies.txt http://localhost:8000/logout
curl -b cookies.txt http://localhost:8000/oppman/  # Should redirect to login
```

### **Environment Variable Testing**
```bash
# Test default values
uv run python -c "from dependencies.config import get_settings; print(get_settings().debug)"

# Test custom values
DEBUG=false uv run python -c "from dependencies.config import get_settings; print(get_settings().debug)"

# Test LLM model
OPENROUTER_LLM_MODEL=anthropic/claude-3.5-sonnet:free uv run python -c "from services.chat_service import LLM_MODEL; print(LLM_MODEL)"
```

### **Deployment Testing**
```bash
# Test different ports
PORT=9000 uv run python main.py

# Test different hosts
HOST=127.0.0.1 uv run python main.py
```

## 📋 **Migration Guide**

### **For Existing Users**
1. **No Breaking Changes**: All existing functionality preserved
2. **New Defaults**: Debug is now enabled by default (better for development)
3. **Optional**: All new features are optional environment variables

### **For New Deployments**
1. **Copy example.env**: `cp example.env .env`
2. **Set API Key**: Add your `OPENROUTER_API_KEY`
3. **Customize**: Set `DEBUG=false` for production
4. **Deploy**: Use `PORT=$PORT` for cloud platforms

## 🔄 **Backward Compatibility**

- ✅ **All existing code works unchanged**
- ✅ **Default values maintain current behavior**
- ✅ **No breaking changes to APIs**
- ✅ **Base assets remain simple (no dependency injection)**
- ✅ **Authentication system is backward compatible**
- ✅ **Existing login/logout flows preserved**
- ✅ **SQLAdmin integration seamless**

## 🎉 **Ready for Production**

This PR makes the application more flexible and production-ready while maintaining simplicity for development use cases.
