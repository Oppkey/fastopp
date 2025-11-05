#!/usr/bin/env python3
"""
Environment Configuration Checker
Shows current environment variables and configuration.
"""
import os

from dotenv import load_dotenv


def check_environment():
    """Check and display environment configuration"""
    print("🔍 Environment Configuration Check")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        return
    
    # Display environment variables
    print("\n📋 Environment Variables:")
    print("-" * 30)
    
    env_vars = {
        'DATABASE_URL': 'Database connection string',
        'SECRET_KEY': 'Application secret key',
        'ENVIRONMENT': 'Current environment'
    }
    
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            # Mask secret key for security
            if var == 'SECRET_KEY':
                display_value = value[:20] + "..." if len(value) > 20 else value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
            print(f"   Description: {description}")
        else:
            print(f"❌ {var}: Not set")
            print(f"   Description: {description}")
    
    # Check database configuration
    print("\n🗄️  Database Configuration:")
    print("-" * 30)
    
    db_url = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./test.db')
    if 'sqlite' in db_url:
        print("✅ Database: SQLite (Development)")
    elif 'postgresql' in db_url:
        print("✅ Database: PostgreSQL (Production)")
    else:
        print("⚠️  Database: Unknown type")
    
    print(f"   URL: {db_url}")
    
    # Check environment
    env = os.getenv('ENVIRONMENT', 'development')
    print(f"\n🌍 Environment: {env}")
    
    # Security recommendations
    print("\n🔒 Security Recommendations:")
    print("-" * 30)
    
    secret_key = os.getenv('SECRET_KEY')
    if secret_key:
        if len(secret_key) < 32:
            print("⚠️  Secret key is too short (should be at least 32 characters)")
        elif 'dev_secret_key' in secret_key:
            print("⚠️  Using development secret key (change for production)")
        else:
            print("✅ Secret key looks secure")
    else:
        print("❌ No secret key set")
    
    if env == 'development':
        print("✅ Development environment detected")
        print("   - Using SQLite for easy development")
        print("   - Debug mode enabled")
    elif env == 'production':
        print("✅ Production environment detected")
        print("   - Using PostgreSQL for performance")
        print("   - Debug mode disabled")
    else:
        print("⚠️  Unknown environment")
    
    print("\n" + "=" * 50)
    print("✅ Environment check complete!")


if __name__ == "__main__":
    check_environment() 