"""
Product service for handling product-related business logic
"""
from sqlmodel import select, func
from sqlalchemy import case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError, DatabaseError
from models import Product
from dependencies.config import Settings
from dependencies.database_health import get_fallback_data


class ProductService:
    """Service for product-related operations"""
    
    def __init__(self, session: AsyncSession, settings: Settings):
        self.session = session
        self.settings = settings
    
    async def get_products_with_stats(self):
        """Get all products with statistics, with graceful database failure handling"""
        try:
            # Get all products
            result = await self.session.execute(select(Product))
            products = result.scalars().all()

            # Get category statistics
            category_stats = await self.session.execute(
                select(Product.category, func.count(Product.id).label('count'))  # type: ignore
                .group_by(Product.category)
            )
            categories = category_stats.all()

            # Get price statistics
            price_stats = await self.session.execute(
                select(
                    func.avg(Product.price).label('avg_price'),
                    func.min(Product.price).label('min_price'),
                    func.max(Product.price).label('max_price'),
                    func.count(Product.id).label('total_products')  # type: ignore
                )
            )
            stats = price_stats.first()

            # Get stock statistics
            stock_stats = await self.session.execute(
                select(
                    func.count(Product.id).label('total'),  # type: ignore
                    func.sum(case(
                        (Product.in_stock.is_(True), 1),  # type: ignore
                        else_=0)).label('in_stock'),
                    func.sum(case(
                        (Product.in_stock.is_(False), 1),  # type: ignore
                        else_=0)).label('out_of_stock')  # type: ignore
                )
            )
            stock = stock_stats.first()
            
            # Handle potential None values safely
            stats_data = {
                "avg_price": float(stats.avg_price) if stats and stats.avg_price is not None else 0,
                "min_price": float(stats.min_price) if stats and stats.min_price is not None else 0,
                "max_price": float(stats.max_price) if stats and stats.max_price is not None else 0,
                "total_products": stats.total_products if stats else 0
            }

            stock_data = {
                "total": stock.total if stock else 0,
                "in_stock": stock.in_stock if stock else 0,
                "out_of_stock": stock.out_of_stock if stock else 0
            }

            return {
                "products": [
                    {
                        "id": str(product.id),
                        "name": product.name,
                        "description": product.description,
                        "price": product.price,
                        "category": product.category,
                        "in_stock": product.in_stock,
                        "created_at": product.created_at.isoformat()
                    }
                    for product in products
                ],
                "categories": [
                    {"category": cat.category, "count": cat.count}
                    for cat in categories if cat.category
                ],
                "stats": stats_data,
                "stock": stock_data,
                "database_available": True
            }
            
        except (OperationalError, DatabaseError, Exception) as e:
            print(f"Database error in ProductService: {e}")
            # Return fallback data when database is unavailable
            fallback_data = get_fallback_data()
            fallback_data["error"] = f"Database unavailable: {str(e)}"
            return fallback_data