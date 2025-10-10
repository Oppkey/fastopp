# =========================
# main.py
# =========================
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
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

# Create upload directories
UPLOAD_DIR = Path(settings.upload_dir)
UPLOAD_DIR.mkdir(exist_ok=True)
PHOTOS_DIR = UPLOAD_DIR / "photos"
PHOTOS_DIR.mkdir(exist_ok=True)

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
    app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

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
    """Serve FontAwesome font files with proper headers to prevent 404 errors"""
    try:
        # Redirect to CDN font files instead of serving locally
        from fastapi.responses import RedirectResponse
        
        if font_file == "fa-solid-900.woff2":
            return RedirectResponse(
                url="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.woff2",
                status_code=302
            )
        elif font_file == "fa-solid-900.ttf":
            return RedirectResponse(
                url="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-solid-900.ttf",
                status_code=302
            )
        elif font_file == "fa-regular-400.woff2":
            return RedirectResponse(
                url="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/webfonts/fa-regular-400.woff2",
                status_code=302
            )
        else:
            raise HTTPException(status_code=404, detail="Font file not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Font file error: {str(e)}")

# Middleware to inject FontAwesome CDN CSS
@app.middleware("http")
async def inject_fontawesome_cdn(request: Request, call_next):
    """Inject FontAwesome CDN CSS into admin pages"""
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
                
                # Check if this is an HTML page and doesn't already have FontAwesome CDN
                if ("<html" in html.lower() and 
                    "font-awesome" not in html.lower() and 
                    "cdnjs.cloudflare.com" not in html):
                    
                    # Inject FontAwesome CDN CSS
                    cdn_css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
    <style>
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
    </style>'''
                    
                    # Inject before closing head tag
                    if "</head>" in html:
                        html = html.replace("</head>", f"{cdn_css}</head>")
                    elif "<head>" in html:
                        html = html.replace("<head>", f"<head>{cdn_css}")
                    else:
                        html = html.replace("</body>", f"{cdn_css}</body>")
                    
                    # Return new response with proper headers (no Content-Length)
                    from fastapi.responses import HTMLResponse
                    new_headers = dict(response.headers)
                    # Remove Content-Length to let FastAPI calculate it
                    new_headers.pop('content-length', None)
                    return HTMLResponse(content=html, status_code=response.status_code, headers=new_headers)
        
        except Exception as e:
            print(f"FontAwesome injection error: {e}")
    
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
