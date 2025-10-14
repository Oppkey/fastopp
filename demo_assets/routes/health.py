"""
Health check routes
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dependencies.database_health import get_database_status

router = APIRouter()


@router.get("/kaithhealthcheck")  # leapcell (correct spelling)
@router.get("/kaithheathcheck")   # leapcell (misspelled - for compatibility)
@router.get("/health")  # generic
@router.get("/healthz")  # kubernetes
async def healthcheck():
    return {"status": "ok"}


@router.get("/health/database")
async def database_health_check():
    """Database health check endpoint"""
    status = await get_database_status()
    return JSONResponse(status)
