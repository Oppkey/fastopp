"""
Health check routes
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/kaithhealthcheck")  # leapcell (correct spelling)
@router.get("/kaithheathcheck")   # leapcell (misspelled - for compatibility)
@router.get("/health")  # generic
@router.get("/healthz")  # kubernetes
async def healthcheck():
    return {"status": "ok"}
