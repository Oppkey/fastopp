from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db_session
from .config import Settings, get_settings


def get_product_service(
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
):
    """Dependency to get ProductService instance - PROOF OF CONCEPT"""
    from services.product_service import ProductService
    return ProductService(session=session, settings=settings)


# Note: Other services will be added in Phase 1B
