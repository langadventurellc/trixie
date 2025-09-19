"""Tests for TransactionRecord model."""

from datetime import datetime

from src.app.api.models.transaction_record import TransactionRecord


def test_transaction_record_valid_data():
    """Test TransactionRecord with valid data."""
    now = datetime.now()
    data = {
        "id": "txn-123",
        "timestamp": now,
        "request": {
            "method": "GET",
            "url": "/v1/users/123",
            "headers": {"authorization": "Bearer token"},
            "body": None,
        },
        "response": {
            "status_code": 200,
            "headers": {"content-type": "application/json"},
            "body": {},
        },
        "proxy_mapping_used": "/v1/users",
    }
    record = TransactionRecord(**data)
    assert record.id == "txn-123"
    assert record.timestamp == now
    assert record.request == data["request"]
    assert record.response == data["response"]
    assert record.proxy_mapping_used == "/v1/users"


def test_transaction_record_serialization():
    """Test TransactionRecord serialization/deserialization."""
    now = datetime.now()
    data = {
        "id": "txn-456",
        "timestamp": now,
        "request": {"method": "POST", "url": "/v2/orders", "headers": {}, "body": {"item": "test"}},
        "response": {"status_code": 201, "headers": {}, "body": {"id": "order-123"}},
        "proxy_mapping_used": "/v2/orders",
    }
    record = TransactionRecord(**data)

    # Test model dump
    dumped = record.model_dump()
    assert dumped["id"] == "txn-456"
    assert dumped["timestamp"] == now

    # Test recreation from dumped data
    new_record = TransactionRecord(**dumped)
    assert new_record.id == record.id
    assert new_record.timestamp == record.timestamp
