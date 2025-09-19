from fastapi import APIRouter

from .endpoints import health_check, proxy_setup

api_router = APIRouter()

api_router.include_router(health_check.router)
api_router.include_router(proxy_setup.router)
