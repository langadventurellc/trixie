"""Clear transactions from storage."""

from pyla_logger import logger

from .storage_data import transaction_history


def clear_transactions() -> int:
    """Clear all transactions from storage.

    Returns:
        int: Number of transactions that were cleared.
    """
    count = len(transaction_history)
    transaction_history.clear()
    logger.info(f"Cleared {count} transactions from storage")
    return count
