#!/usr/bin/env python3
"""
Emergency Access Token Generator
Generates emergency access tokens using the SECRET_KEY for password recovery.
"""
import hashlib
import os
import sys
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import from dependencies (demo mode), fall back to direct import (minimal mode)
try:
    from dependencies.config import get_settings
    USE_DEPENDENCY_INJECTION = True
except ImportError:
    # Fallback for minimal mode - direct environment variable access
    USE_DEPENDENCY_INJECTION = False


def generate_emergency_token(secret_key: str) -> str:
    """Generate emergency access token from SECRET_KEY"""
    return hashlib.sha256(f"emergency_access_{secret_key}".encode()).hexdigest()


def main():
    """Main function to generate emergency access token"""
    print("🚨 Emergency Access Token Generator")
    print("=" * 50)
    
    try:
        # Get settings based on mode
        if USE_DEPENDENCY_INJECTION:
            settings = get_settings()
            secret_key = settings.secret_key
        else:
            # Minimal mode - direct environment variable access
            secret_key = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")
        
        if not secret_key or secret_key == "dev_secret_key_change_in_production":
            print("⚠️  WARNING: Using default SECRET_KEY!")
            print("   This is not secure for production use.")
            print("   Please set a proper SECRET_KEY in your environment.")
            print()
        
        # Generate token
        token = generate_emergency_token(secret_key)
        
        print(f"🔑 SECRET_KEY: {secret_key}")
        print(f"🎫 Emergency Token: {token}")
        print()
        print("📋 Instructions:")
        print("1. Enable emergency access: export EMERGENCY_ACCESS_ENABLED=true")
        print("2. Visit: http://localhost:8000/oppman/emergency")
        print("3. Enter your SECRET_KEY (not the token) in the form")
        print("4. Reset your admin password")
        print("5. Disable emergency access: export EMERGENCY_ACCESS_ENABLED=false")
        print()
        print("⚠️  Security Notes:")
        print("- Emergency access is disabled by default")
        print("- Only enable it when you need to recover access")
        print("- Disable it immediately after use")
        print("- Keep your SECRET_KEY secure")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
