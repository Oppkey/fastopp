#!/usr/bin/env python3
"""
Test script for SQLAdmin CDN FontAwesome fix
Run this to test the CDN approach locally before deployment
"""

import asyncio
import sys
from fastapi.testclient import TestClient

def test_cdn_approach():
    """Test the CDN approach locally"""
    print("🧪 Testing SQLAdmin CDN FontAwesome Fix")
    print("=" * 50)
    
    try:
        # Import the app
        from main import app
        client = TestClient(app)
        
        print("✅ Application loaded successfully")
        
        # Test admin access
        print("\n📋 Testing admin interface...")
        response = client.get('/admin/')
        print(f"   Admin page: {response.status_code}")
        
        login_response = client.get('/admin/login')
        print(f"   Login page: {login_response.status_code}")
        
        if login_response.status_code == 200:
            html = login_response.text
            print(f"   HTML content: {len(html)} characters")
            
            # Check for SQLAdmin elements
            if 'sqladmin' in html.lower():
                print("   ✅ SQLAdmin interface detected")
            else:
                print("   ❌ SQLAdmin interface not found")
                
            # Check for existing FontAwesome
            if 'font-awesome' in html.lower():
                print("   ✅ FontAwesome references found")
            else:
                print("   ℹ️  No FontAwesome references (expected)")
                
        print("\n🎯 CDN Testing Instructions:")
        print("=" * 50)
        print("1. Start the server:")
        print("   uv run uvicorn main:app --reload")
        print()
        print("2. Open browser to: http://localhost:8000/admin/")
        print()
        print("3. Open Developer Tools (F12)")
        print("4. Go to Console tab")
        print("5. Run this JavaScript:")
        print()
        print("   // Inject FontAwesome CDN CSS")
        print("   const link = document.createElement('link');")
        print("   link.rel = 'stylesheet';")
        print("   link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css';")
        print("   link.integrity = 'sha512-Avb2QiuDEEvB4bZJYdft2mNjVShBftLdPG8FJ0V7irTLQ8Uo0qcPxh4Plq7G5tGm0rU+1SPhVotteLpBERwTkw==';")
        print("   link.crossOrigin = 'anonymous';")
        print("   document.head.appendChild(link);")
        print()
        print("6. Check if icons now display correctly")
        print("7. Look for any console errors")
        print()
        print("✅ If icons display correctly, the CDN approach works!")
        print("✅ You can then deploy to LeapCell with confidence")
        
    except Exception as e:
        print(f"❌ Error testing application: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = test_cdn_approach()
    sys.exit(0 if success else 1)
