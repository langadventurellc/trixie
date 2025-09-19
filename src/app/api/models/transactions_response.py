"""Transactions response model for reverse proxy API."""

from typing import List

from pydantic import BaseModel, Field

from .transaction_record import TransactionRecord


class TransactionsResponse(BaseModel):
    """Response model for GET /api/transactions endpoint."""

    transactions: List[TransactionRecord] = Field(..., description="List of transaction records")
    count: int = Field(..., description="Number of transactions returned")
