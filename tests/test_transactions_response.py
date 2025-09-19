"""Tests for TransactionsResponse model."""

from datetime import datetime

from src.app.api.models.transaction_record import TransactionRecord
from src.app.api.models.transactions_response import TransactionsResponse


def test_transactions_response_valid_data():
    """Test TransactionsResponse with valid data."""
    now = datetime.now()
    transaction = TransactionRecord(
        id="txn-123",
        timestamp=now,
        request={"method": "GET", "url": "/v1/users", "headers": {}, "body": None},
        response={"status_code": 200, "headers": {}, "body": {}},
        proxy_mapping_used="/v1/users",
    )

    data = {"transactions": [transaction], "count": 1}
    response = TransactionsResponse(**data)
    assert len(response.transactions) == 1
    assert response.count == 1
    assert response.transactions[0].id == "txn-123"


def test_transactions_response_empty():
    """Test TransactionsResponse with empty transactions."""
    data = {"transactions": [], "count": 0}
    response = TransactionsResponse(**data)
    assert response.transactions == []
    assert response.count == 0
