from fastapi import APIRouter

from .endpoints import clear_transactions, health_check, proxy_setup, transactions

api_router = APIRouter()

api_router.include_router(health_check.router)
api_router.include_router(proxy_setup.router)
api_router.include_router(transactions.router)
api_router.include_router(clear_transactions.router)
