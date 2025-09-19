"""Add transaction function."""

from .storage_data import transaction_history


def add_transaction(transaction_data: dict) -> None:
    """Add a transaction to the history.

    Args:
        transaction_data: Complete transaction data including request/response info
    """
    transaction_history.append(transaction_data)
