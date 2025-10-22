# =========================
# main.py
# =========================
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from admin.setup import setup_admin
from routes.chat import router as chat_router
from routes.api import router as api_router
from routes.health import router as health_router
try:
    from routes.auth import router as auth_router
except Exception:
    auth_router = None  # Optional during partial restores
from routes.pages import router as pages_router
try:
    from routes.webinar import router as webinar_router
except Exception:
    webinar_router = None  # Optional during partial restores
try:
    from routes.oppman import router as oppman_router
except Exception:
    oppman_router = None  # Optional during partial restores
try:
    from routes.oppdemo import router as oppdemo_router
except Exception:
    oppdemo_router = None  # Optional during partial restores

# Import dependency injection modules
from dependencies.database import create_database_engine, create_session_factory
from dependencies.config import get_settings

# Load environment variables
load_dotenv()

# Get settings using dependency injection
settings = get_settings()

# Initialize storage system (handles directory creation gracefully)
try:
    from core.services.storage import get_storage
    storage = get_storage()
    # Ensure required directories exist
    storage.ensure_directories("photos", "sample_photos")
except Exception as e:
    print(f"Warning: Storage initialization failed: {e}")
    print("Application will continue but file uploads may not work.")

# from users import fastapi_users, auth_backend  # type: ignore

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


# Add proxy headers middleware for production deployments
@app.middleware("http")
async def proxy_headers_middleware(request: Request, call_next):
    """Middleware to handle proxy headers for production deployments"""
    # Check if we're behind a proxy (Railway, Fly, etc.)
    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"

    # Don't modify scope["type"] - it should remain "http" for HTTP requests

    response = await call_next(request)
    return response


# Setup dependencies
def setup_dependencies(app: FastAPI):
    """Setup application dependencies"""
    # Create database engine and session factory
    engine = create_database_engine(settings)
    session_factory = create_session_factory(engine)

    # Store in app state for dependency injection
    app.state.db_engine = engine
    app.state.session_factory = session_factory
    app.state.settings = settings

    print(f"✅ Dependencies setup complete - session_factory: {session_factory}")
    print(f"✅ App state after setup: {list(app.state.__dict__.keys())}")


# Setup dependencies immediately
setup_dependencies(app)

# Mount uploads directory based on environment (MUST come before /static mount)
if settings.upload_dir != "static/uploads":
    # In production environments, mount the uploads directory separately
    # Only mount if the directory exists (serverless environments may not have writable directories)
    upload_path = Path(settings.upload_dir)
    if upload_path.exists():
        app.mount("/static/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
    else:
        print(f"Warning: Upload directory '{settings.upload_dir}' does not exist. Skipping static file mounting.")

# Mount static files (MUST come after /static/uploads to avoid conflicts)
app.mount("/static", StaticFiles(directory="static"), name="static")

# SQLAdmin automatically handles static file serving at /admin/statics/
# No manual mounting required - SQLAdmin does this internally

templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


# Setup admin interface
setup_admin(app, settings.secret_key)

# Add custom routes to handle missing FontAwesome font files
@app.get("/admin/statics/webfonts/{font_file}")
async def serve_font_files(font_file: str):
    """Redirect all font requests to CDN to prevent 404 errors and font loading issues"""
    try:
        from fastapi.responses import RedirectResponse
        
        # Map all possible font files to CDN equivalents
        font_mapping = {
            "fa-solid-900.woff2": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2",
            "fa-solid-900.woff": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff",
            "fa-solid-900.ttf": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.ttf",
            "fa-solid-900.eot": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.eot",
            "fa-regular-400.woff2": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.woff2",
            "fa-regular-400.woff": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.woff",
            "fa-regular-400.ttf": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.ttf",
            "fa-regular-400.eot": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.eot",
        }
        
        if font_file in font_mapping:
            return RedirectResponse(url=font_mapping[font_file], status_code=302)
        else:
            # For any other font file, redirect to solid font as fallback
            return RedirectResponse(
                url="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2",
                status_code=302
            )
    except Exception as e:
        # If anything fails, redirect to CDN anyway
        return RedirectResponse(
            url="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2",
            status_code=302
        )

# Add favicon route to prevent 404 errors
@app.get("/favicon.ico")
async def favicon():
    """Return a simple favicon to prevent 404 errors"""
    from fastapi.responses import Response
    # Return a minimal 1x1 transparent PNG
    favicon_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
    return Response(content=favicon_data, media_type="image/png")

# Add CSS file redirects to prevent 404 errors for missing SQLAdmin CSS
@app.get("/admin/statics/css/fontawesome.min.css")
async def fontawesome_css_redirect():
    """Redirect FontAwesome CSS to CDN to prevent 404 errors"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        url="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
        status_code=302
    )

# Middleware to inject FontAwesome CDN CSS and customize SQLAdmin logout
@app.middleware("http")
async def inject_fontawesome_cdn(request: Request, call_next):
    """Inject FontAwesome CDN CSS and customize SQLAdmin logout into admin pages"""
    response = await call_next(request)
    
    # Only process admin HTML pages (not static assets)
    if (request.url.path.startswith("/admin/") and 
        not request.url.path.startswith("/admin/statics/") and
        not request.url.path.startswith("/admin/static/") and
        not request.url.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot'))):
        try:
            # Get response body
            body = b""
            if hasattr(response, 'body'):
                body = response.body
            elif hasattr(response, 'content'):
                body = response.content
            elif hasattr(response, 'text'):
                body = response.text.encode('utf-8')
            elif hasattr(response, 'body_iterator'):
                # Handle streaming responses
                async for chunk in response.body_iterator:
                    body += chunk
            
            if body:
                html = body.decode('utf-8')
                
                # Check if this is an HTML page
                if "<html" in html.lower():
                    
                    # Inject FontAwesome CDN CSS and logout customization
                    custom_js = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
    <style>
        /* Override SQLAdmin's font loading with CDN fonts */
        @font-face {
            font-family: "Font Awesome 6 Free";
            font-style: normal;
            font-weight: 900;
            font-display: block;
            src: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2") format("woff2");
        }
        @font-face {
            font-family: "Font Awesome 5 Free";
            font-style: normal;
            font-weight: 900;
            font-display: block;
            src: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2") format("woff2");
        }
        @font-face {
            font-family: "Font Awesome 6 Free";
            font-style: normal;
            font-weight: 400;
            font-display: block;
            src: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.woff2") format("woff2");
        }
        /* Ensure FontAwesome icons use CDN fonts */
        .fa, .fas, .far, .fal, .fab {
            font-family: "Font Awesome 6 Free" !important;
        }
        
        /* Hide SQLAdmin logout button */
        .navbar .navbar-nav .nav-item:has(a[href*="logout"]) {
            display: none !important;
        }
        
        /* Style for our custom logout button */
        .custom-logout-btn {
            color: #dc3545 !important;
            text-decoration: none !important;
            margin-left: 10px;
            display: inline-block !important;
            padding: 8px 12px !important;
            background-color: rgba(220, 53, 69, 0.1) !important;
            border-radius: 4px !important;
            border: 1px solid #dc3545 !important;
        }
        
        .custom-logout-btn:hover {
            color: #c82333 !important;
            background-color: rgba(220, 53, 69, 0.2) !important;
        }
        
        /* Make sure our logout button is visible */
        .nav-item .custom-logout-btn {
            display: inline-block !important;
            visibility: visible !important;
        }
    </style>
    <script>
        // Hide SQLAdmin logout button and add our own
        document.addEventListener('DOMContentLoaded', function() {
            console.log('SQLAdmin customization script loaded');
            
            // Find and hide the original logout button
            const logoutLinks = document.querySelectorAll('a[href*="logout"]');
            console.log('Found logout links:', logoutLinks.length);
            logoutLinks.forEach(link => {
                link.style.display = 'none';
                console.log('Hidden logout link:', link.href);
            });
            
            // Add our custom logout button to the top-right corner
            const fallbackButton = document.createElement('div');
            fallbackButton.style.position = 'fixed';
            fallbackButton.style.top = '10px';
            fallbackButton.style.right = '10px';
            fallbackButton.style.zIndex = '10000';
            fallbackButton.style.backgroundColor = '#dc3545';
            fallbackButton.style.color = 'white';
            fallbackButton.style.padding = '10px 15px';
            fallbackButton.style.borderRadius = '5px';
            fallbackButton.style.cursor = 'pointer';
            fallbackButton.style.fontWeight = 'bold';
            fallbackButton.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
            fallbackButton.innerHTML = '<i class="fas fa-sign-out-alt"></i> Logout';
            fallbackButton.onclick = () => window.location.href = '/logout';
            document.body.appendChild(fallbackButton);
            console.log('Added custom logout button to top-right corner');
        });
    </script>'''
                    
                    # Inject early in head, right after opening head tag
                    if "<head>" in html:
                        html = html.replace("<head>", f"<head>{custom_js}")
                    elif "</head>" in html:
                        html = html.replace("</head>", f"{custom_js}</head>")
                    else:
                        html = html.replace("</body>", f"{custom_js}</body>")
                    
                    # Return new response with proper headers (no Content-Length)
                    from fastapi.responses import HTMLResponse
                    new_headers = dict(response.headers)
                    # Remove Content-Length to let FastAPI calculate it
                    new_headers.pop('content-length', None)
                    return HTMLResponse(content=html, status_code=response.status_code, headers=new_headers)
        
        except Exception as e:
            print(f"SQLAdmin customization error: {e}")
    
    return response

# Include routers
app.include_router(health_router)
app.include_router(chat_router, prefix="/api")
app.include_router(api_router, prefix="/api")
if auth_router:
    app.include_router(auth_router)
app.include_router(pages_router)
if webinar_router:
    app.include_router(webinar_router)
if oppman_router:
    app.include_router(oppman_router, prefix="/oppman")
if oppdemo_router:
    app.include_router(oppdemo_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and redirect to login if authentication fails"""
    if exc.status_code in [401, 403]:
        # Preserve the original URL as a redirect parameter
        original_url = str(request.url)
        login_url = f"/login?next={original_url}"
        return RedirectResponse(url=login_url, status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle global exceptions, especially database connection errors"""
    from dependencies.database_health import is_database_available
    
    # Check if this is a database-related error
    if "database" in str(exc).lower() or "sqlite" in str(exc).lower() or "operational" in str(exc).lower():
        # Check if database is available
        db_available = await is_database_available()
        
        if not db_available:
            # Redirect to database status page for database issues
            return RedirectResponse(url="/database-status", status_code=302)
    
    # For other exceptions, return a generic error
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )
