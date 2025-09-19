"""Get transactions function."""

from typing import Optional

from .storage_data import transaction_history


def get_transactions(count: Optional[int] = None) -> list[dict]:
    """Get transaction history in reverse chronological order (newest first).

    Args:
        count: Optional limit on number of transactions to return

    Returns:
        List of transaction data dictionaries
    """
    # Return transactions in reverse chronological order (newest first)
    transactions = transaction_history[::-1]

    if count is not None:
        return transactions[:count] if count > 0 else []

    return transactions
