from fastapi import APIRouter
from pyla_logger import logger

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    logger.info("Health check successful.")

    return {"status": "ok"}
