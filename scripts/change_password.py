import argparse
import asyncio
import os
import sys

# Add the parent directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi_users.password import PasswordHelper
from sqlmodel import select

from db import AsyncSessionLocal
from models import User


async def change_user_password(email: str, new_password: str) -> bool:
    """Change a user's password by email address"""
    async with AsyncSessionLocal() as session:
        try:
            # Find the user by email
            result = await session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                print(f"❌ User not found: {email}")
                return False
            
            if not user.is_active:
                print(f"⚠️  User is inactive: {email}")
                return False
            
            # Hash the new password
            password_helper = PasswordHelper()
            hashed_password = password_helper.hash(new_password)
            
            # Update the user's password
            user.hashed_password = hashed_password
            await session.commit()
            
            print(f"✅ Password changed successfully for user: {email}")
            return True
            
        except Exception as e:
            print(f"❌ Error changing password: {e}")
            await session.rollback()
            return False


async def change_password_interactive():
    """Interactive password change mode"""
    print("🔐 Interactive Password Change")
    print("=" * 40)
    
    try:
        # Get user email
        email = input("Enter user email: ").strip()
        if not email:
            print("❌ Email cannot be empty")
            return False
        
        # Get new password
        new_password = input("Enter new password: ").strip()
        if not new_password:
            print("❌ Password cannot be empty")
            return False
        
        # Confirm password
        confirm_password = input("Confirm new password: ").strip()
        if new_password != confirm_password:
            print("❌ Passwords do not match")
            return False
        
        # Validate password length
        if len(new_password) < 6:
            print("❌ Password must be at least 6 characters long")
            return False
        
        # Change the password
        return await change_user_password(email, new_password)
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def change_password_by_args(email: str, new_password: str) -> bool:
    """Change password using command line arguments"""
    if not email or not new_password:
        print("❌ Both email and password are required")
        return False
    
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters long")
        return False
    
    return await change_user_password(email, new_password)


async def list_users():
    """List all users for reference"""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            
            if not users:
                print("ℹ️  No users found in database")
                return
            
            print("\n👥 Current Users:")
            print("-" * 60)
            print(f"{'Email':<30} {'Active':<8} {'Superuser':<12} {'Staff':<8}")
            print("-" * 60)
            
            for user in users:
                status = "✅" if user.is_active else "❌"
                superuser = "✅" if user.is_superuser else "❌"
                staff = "✅" if user.is_staff else "❌"
                print(f"{user.email:<30} {status:<8} {superuser:<12} {staff:<8}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error listing users: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Change user password in FastOpp application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  uv run python scripts/change_password.py
  
  # Command line mode
  uv run python scripts/change_password.py --email user@example.com --password newpass123
  
  # List all users
  uv run python scripts/change_password.py --list
  
  # Change password for specific user
  uv run python scripts/change_password.py --email admin@example.com --password admin456
        """
    )
    
    parser.add_argument(
        "--email",
        help="User email address"
    )
    
    parser.add_argument(
        "--password",
        help="New password (minimum 6 characters)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all users"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (default if no arguments provided)"
    )
    
    args = parser.parse_args()
    
    async def run():
        if args.list:
            await list_users()
        elif args.email and args.password:
            await change_password_by_args(args.email, args.password)
        elif args.interactive or (not args.email and not args.password and not args.list):
            await change_password_interactive()
        else:
            parser.print_help()
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
