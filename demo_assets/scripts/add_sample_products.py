# =========================
# add_sample_products.py - Add sample products to database
# =========================
import asyncio

from db import AsyncSessionLocal


async def add_sample_products():
    """Add sample products to the database"""
    from models import Product  # Import inside function to avoid module-level import error
    
    async with AsyncSessionLocal() as session:
        # Sample product data
        sample_products = [
            {
                "name": "MacBook Pro 16-inch",
                "description": "Latest MacBook Pro with M3 chip, 16GB RAM, 512GB SSD",
                "price": 2499.99,
                "category": "Electronics",
                "in_stock": True
            },
            {
                "name": "iPhone 15 Pro",
                "description": "Apple's latest iPhone with titanium design and A17 Pro chip",
                "price": 999.99,
                "category": "Electronics",
                "in_stock": True
            },
            {
                "name": "Nike Air Max 270",
                "description": "Comfortable running shoes with Air Max technology",
                "price": 129.99,
                "category": "Footwear",
                "in_stock": True
            },
            {
                "name": "Starbucks Coffee Mug",
                "description": "Ceramic coffee mug with Starbucks branding",
                "price": 12.99,
                "category": "Home & Kitchen",
                "in_stock": False
            },
            {
                "name": "Python Programming Book",
                "description": "Comprehensive guide to Python programming language",
                "price": 49.99,
                "category": "Books",
                "in_stock": True
            },
            {
                "name": "Wireless Bluetooth Headphones",
                "description": "Noise-cancelling wireless headphones with 30-hour battery",
                "price": 199.99,
                "category": "Electronics",
                "in_stock": True
            },
            {
                "name": "Organic Cotton T-Shirt",
                "description": "Comfortable organic cotton t-shirt in various colors",
                "price": 24.99,
                "category": "Clothing",
                "in_stock": True
            },
            {
                "name": "Yoga Mat",
                "description": "Non-slip yoga mat perfect for home workouts",
                "price": 34.99,
                "category": "Sports & Fitness",
                "in_stock": True
            }
        ]
        
        for product_data in sample_products:
            product = Product(**product_data)
            session.add(product)
        
        await session.commit()
        print("✅ Added sample products to database!")
        print(f"Added {len(sample_products)} products:")
        for product in sample_products:
            print(f"- {product['name']} (${product['price']}) - {product['category']}")


if __name__ == "__main__":
    asyncio.run(add_sample_products()) 