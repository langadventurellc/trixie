"""Clear transactions endpoint for reverse proxy API."""

from fastapi import APIRouter, HTTPException
from pyla_logger import logger

from ...core.clear_transactions import clear_transactions

router = APIRouter()


@router.delete("/transactions")
async def clear_transactions_endpoint() -> dict[str, int]:
    """Clear all transactions from storage.

    Returns:
        dict: Response containing the number of transactions that were cleared.

    Raises:
        HTTPException: 500 for storage errors.
    """
    try:
        cleared_count = clear_transactions()
        logger.info(f"Successfully cleared {cleared_count} transactions via API")
        return {"cleared_count": cleared_count}

    except Exception as e:
        logger.error(f"Failed to clear transactions: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while clearing transactions"
        )
