#!/usr/bin/env python3
"""
Simple Production Startup Script
Runs FastAPI with Gunicorn without Nginx
"""
import os
import subprocess
import sys


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import asyncpg  # noqa: F401
        import gunicorn  # noqa: F401
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: uv add asyncpg gunicorn")
        return False


def check_database_url():
    """Check if database URL is configured"""
    try:
        from db import DATABASE_URL
        if "postgresql+asyncpg" in DATABASE_URL:
            print("✅ PostgreSQL URL configured")
            return True
        else:
            print("⚠️  Using SQLite (development mode)")
            print("For production, update DATABASE_URL in db.py")
            return False
    except Exception as e:
        print(f"❌ Database configuration error: {e}")
        return False


def start_production_server():
    """Start the production server"""
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", "8000")
    
    print("🚀 Starting FastAPI production server...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"🔧 Admin panel: http://{host}:{port}/admin/")
    print(f"📚 API docs: http://{host}:{port}/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    # Gunicorn command for production
    cmd = [
        "uv", "run", "gunicorn",
        "main:app",
        "-w", "4",  # 4 workers
        "-k", "uvicorn.workers.UvicornWorker",
        "--bind", f"{host}:{port}",
        "--timeout", "120",
        "--keep-alive", "5",
        "--max-requests", "1000",
        "--max-requests-jitter", "50"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main entry point"""
    print("FastAPI Production Server")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check database configuration
    check_database_url()
    
    # Start server
    start_production_server()


if __name__ == "__main__":
    main() 