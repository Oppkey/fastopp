#!/usr/bin/env python3
"""
FastOpp Base Assets
A minimal FastAPI application with authentication and protected content
"""
import os
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin.setup import setup_admin
from base_assets.routes.auth import router as auth_router
from base_assets.routes.pages import router as pages_router
try:
    from base_assets.routes.oppman import router as oppman_router
except Exception:
    oppman_router = None  # Optional during partial restores

app = FastAPI(
    title="FastOpp Base Assets",
    description="A minimal FastAPI application with authentication and protected content",
    version="1.0.0"
)

"""Configure authentication/session for SQLAdmin login and user authentication"""
# Load environment variables and secret key
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")

# Enable sessions (required by sqladmin authentication backend)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# SQLAdmin automatically handles static file serving at /admin/statics/
# No manual mounting required - SQLAdmin does this internally

# Mount SQLAdmin with authentication backend
setup_admin(app, SECRET_KEY)

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

# Add middleware to inject FontAwesome CDN CSS automatically
@app.middleware("http")
async def inject_fontawesome_cdn_auto(request, call_next):
    """Automatically inject FontAwesome CDN CSS for SQLAdmin pages"""
    response = await call_next(request)
    
    # Only inject for SQLAdmin pages with HTML content
    if (request.url.path.startswith("/admin") and 
        response.headers.get("content-type", "").startswith("text/html")):
        
        try:
            # Get HTML content - handle different response types
            html = None
            if hasattr(response, 'body') and response.body:
                html = response.body.decode("utf-8")
            elif hasattr(response, 'content') and response.content:
                html = response.content.decode("utf-8")
            elif hasattr(response, 'text'):
                html = response.text
            else:
                return response
                
            # Check if FontAwesome CDN is already present
            if html and "cdnjs.cloudflare.com" not in html and "font-awesome" not in html.lower():
                # Inject FontAwesome CDN CSS with font override
                cdn_css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">
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
</style>'''
                
                # Find the head tag and inject CSS
                if "<head>" in html:
                    html = html.replace("<head>", f"<head>{cdn_css}")
                elif "<head " in html:
                    html = html.replace("<head ", f"<head {cdn_css} ")
                
                # Update response - handle different response types
                if hasattr(response, 'body'):
                    response.body = html.encode("utf-8")
                elif hasattr(response, 'content'):
                    response.content = html.encode("utf-8")
                elif hasattr(response, 'text'):
                    response.text = html
                else:
                    # Create new response for other types
                    from fastapi.responses import HTMLResponse
                    return HTMLResponse(content=html, status_code=response.status_code, headers=dict(response.headers))
                    
        except Exception as e:
            # If there's any error, just pass through
            print(f"CDN injection error: {e}")
            pass
    
    return response

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth_router)
app.include_router(pages_router)
if oppman_router:
    app.include_router(oppman_router, prefix="/oppman")

# Add exception handler for authentication


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and redirect to login if authentication fails"""
    if exc.status_code in [401, 403]:
        return RedirectResponse(url="/login", status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "FastOpp Base Assets app is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
