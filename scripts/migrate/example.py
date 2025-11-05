#!/usr/bin/env python3
"""
Example: Adding a new model and creating a migration

This script demonstrates how to add a new model to models.py
and create a migration for it.
"""
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from scripts.migrate.core import MigrationManager
except ImportError:
    print("❌ Could not import MigrationManager")
    sys.exit(1)


def add_example_model():
    """Example of adding a new model to models.py"""
    
    models_content = '''
# Add this to your models.py file:

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    total_amount: float = Field(nullable=False)
    status: str = Field(default="pending", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
'''
    
    print("📝 Example: Adding a new model to models.py")
    print("=" * 50)
    print(models_content)
    print("=" * 50)
    print("After adding the model to models.py, run:")
    print("python oppman.py migrate create 'Add Order model'")
    print("python oppman.py migrate upgrade")


def create_example_migration():
    """Example of creating and applying a migration"""
    
    manager = MigrationManager()
    
    print("🔄 Creating example migration...")
    
    # Check if Alembic is initialized
    if not manager.is_initialized():
        print("❌ Alembic not initialized. Run: python oppman.py migrate init")
        return False
    
    # Create migration
    success = manager.create_migration("Add example Order model")
    
    if success:
        print("\n✅ Migration created successfully!")
        print("📋 Next steps:")
        print("1. Review the generated migration file in alembic/versions/")
        print("2. Apply the migration: python oppman.py migrate upgrade")
        print("3. Check status: python oppman.py migrate current")
    else:
        print("❌ Failed to create migration")
    
    return success


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration Examples")
    parser.add_argument(
        "action",
        choices=["show", "create"],
        help="Action to perform"
    )
    
    args = parser.parse_args()
    
    if args.action == "show":
        add_example_model()
    elif args.action == "create":
        create_example_migration()


if __name__ == "__main__":
    main() 