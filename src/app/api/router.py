from fastapi import APIRouter

from .endpoints import health_check

api_router = APIRouter()

api_router.include_router(health_check.router)
