#!/usr/bin/env python3
"""
Server management commands for oppman.py
"""
import os
import subprocess


def run_server():
    """Start the development server with uvicorn"""
    # Simple environment variable configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print("🚀 Starting development server...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"🔧 Admin panel: http://{host}:{port}/admin/")
    print(f"📚 API docs: http://{host}:{port}/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start uvicorn with reload
        subprocess.run([
            "uv", "run", "python", "-m", "uvicorn", "main:app", "--reload", 
            "--host", host, "--port", str(port)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def stop_server():
    """Stop the development server"""
    print("🛑 Stopping development server...")
    
    try:
        # Kill uvicorn processes
        result = subprocess.run([
            "pkill", "-f", "uv run uvicorn main:app"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Development server stopped successfully")
            return True
        else:
            print("ℹ️  No development server found running")
            return True
    except Exception as e:
        print(f"❌ Failed to stop server: {e}")
        return False


def run_production_server():
    """Start the production server with Gunicorn"""
    # Simple environment variable configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print("🚀 Starting FastAPI production server...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"🔧 Admin panel: http://{host}:{port}/admin/")
    print(f"📚 API docs: http://{host}:{port}/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start gunicorn with uvicorn workers
        subprocess.run([
            "uv", "run", "gunicorn",
            "main:app",
            "-w", "4",  # 4 workers
            "-k", "uvicorn.workers.UvicornWorker",
            "--bind", f"{host}:{port}",
            "--timeout", "120",
            "--keep-alive", "5",
            "--max-requests", "1000",
            "--max-requests-jitter", "50"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        print("Make sure asyncpg and gunicorn are installed: uv add asyncpg gunicorn")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
