"""Transactions endpoint for reverse proxy API."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pyla_logger import logger

from ...core.get_transactions import get_transactions
from ..models.transaction_record import TransactionRecord
from ..models.transactions_response import TransactionsResponse

router = APIRouter()


@router.get("/transactions", response_model=TransactionsResponse)
async def get_transactions_endpoint(
    count: Optional[int] = Query(None, ge=1, description="Limit number of transactions returned")
) -> TransactionsResponse:
    """Get transaction history in reverse chronological order (newest first).

    Args:
        count: Optional limit on number of transactions to return.
               Must be positive integer (≥ 1) if specified.

    Returns:
        TransactionsResponse containing list of transactions and count.

    Raises:
        HTTPException: 400 for invalid count parameter, 500 for storage errors.
    """
    try:
        # Get transactions from storage
        transaction_dicts = get_transactions(count)
        logger.debug(f"Retrieved {len(transaction_dicts)} transactions from storage")

        # Transform dict data to TransactionRecord models
        transactions = [TransactionRecord(**transaction) for transaction in transaction_dicts]

        logger.info(f"Returning {len(transactions)} transactions (count limit: {count})")

        return TransactionsResponse(transactions=transactions, count=len(transactions))

    except Exception as e:
        logger.error(f"Failed to retrieve transactions: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while retrieving transactions"
        )
