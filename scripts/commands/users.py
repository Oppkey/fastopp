#!/usr/bin/env python3
"""
User management commands for oppman.py
"""
import asyncio

from scripts.change_password import change_password_interactive, list_users
from scripts.check_users import check_users
from scripts.create_superuser import create_superuser
from scripts.emergency_access import main as emergency_access_main
from scripts.init_db import init_db
from scripts.test_auth import test_auth


async def run_init():
    """Initialize a new database"""
    print("🔄 Initializing database...")
    await init_db()
    print("✅ Database initialization complete")


async def run_superuser():
    """Create superuser"""
    print("🔄 Creating superuser...")
    await create_superuser()
    print("✅ Superuser creation complete")


async def run_check_users():
    """Check existing users and their permissions"""
    print("🔄 Checking users...")
    await check_users()
    print("✅ User check complete")


async def run_test_auth():
    """Test the authentication system"""
    print("🔄 Testing authentication system...")
    await test_auth()
    print("✅ Authentication test complete")


async def run_change_password():
    """Change user password interactively"""
    print("🔐 Changing user password...")
    await change_password_interactive()


async def run_list_users():
    """List all users"""
    print("👥 Listing users...")
    await list_users()


def run_emergency_access():
    """Generate emergency access token"""
    print("🚨 Generating emergency access token...")
    emergency_access_main()
