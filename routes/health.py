"""
Health check routes
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/kaithhealthcheck") # leapcell
@router.get("/health") # generic
@router.get("/healthz")  # kubernetes
async def healthcheck():
    return {"status": "ok"}
