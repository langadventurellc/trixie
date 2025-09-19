"""Tests for storage functions."""

import pytest

from src.app.core.add_proxy_config import add_proxy_config
from src.app.core.add_transaction import add_transaction
from src.app.core.clear_proxy_configs import clear_proxy_configs
from src.app.core.get_proxy_config import get_proxy_config
from src.app.core.get_transactions import get_transactions
from src.app.core.storage_data import proxy_configurations, transaction_history


@pytest.fixture(autouse=True)
def clean_storage():
    """Clean storage before each test."""
    proxy_configurations.clear()
    transaction_history.clear()


def test_add_and_get_proxy_config():
    """Test adding and retrieving proxy configurations."""
    add_proxy_config("/v1/users", "https://api.example.com")
    add_proxy_config("/v2/orders", "https://orders.example.com")

    assert get_proxy_config("/v1/users/123") == "https://api.example.com"
    assert get_proxy_config("/v2/orders/456") == "https://orders.example.com"


def test_prefix_matching_longest_first():
    """Test that longest matching prefix is returned."""
    add_proxy_config("/v1", "https://api-v1.example.com")
    add_proxy_config("/v1/users", "https://users.example.com")

    # Should match the longer prefix
    assert get_proxy_config("/v1/users/123") == "https://users.example.com"
    # Should match the shorter prefix when longer doesn't match
    assert get_proxy_config("/v1/products") == "https://api-v1.example.com"


def test_get_proxy_config_no_match():
    """Test get_proxy_config when no prefix matches."""
    add_proxy_config("/v1/users", "https://api.example.com")

    assert get_proxy_config("/v2/orders") is None
    assert get_proxy_config("/api/products") is None


def test_get_proxy_config_empty_storage():
    """Test get_proxy_config with empty storage."""
    assert get_proxy_config("/any/path") is None


def test_clear_proxy_configs():
    """Test clearing proxy configurations."""
    add_proxy_config("/v1/users", "https://api.example.com")
    add_proxy_config("/v2/orders", "https://orders.example.com")

    clear_proxy_configs()

    assert get_proxy_config("/v1/users") is None
    assert get_proxy_config("/v2/orders") is None


def test_add_and_get_transactions():
    """Test adding and retrieving transactions."""
    transaction1 = {
        "id": "txn-1",
        "timestamp": "2023-01-01T00:00:00",
        "request": {"method": "GET", "url": "/v1/users"},
        "response": {"status_code": 200},
    }
    transaction2 = {
        "id": "txn-2",
        "timestamp": "2023-01-01T01:00:00",
        "request": {"method": "POST", "url": "/v2/orders"},
        "response": {"status_code": 201},
    }

    add_transaction(transaction1)
    add_transaction(transaction2)

    # Should return in reverse chronological order (newest first)
    transactions = get_transactions()
    assert len(transactions) == 2
    assert transactions[0]["id"] == "txn-2"  # Most recent first
    assert transactions[1]["id"] == "txn-1"


def test_get_transactions_with_count_limit():
    """Test get_transactions with count limit."""
    for i in range(5):
        add_transaction({"id": f"txn-{i}", "timestamp": f"2023-01-01T0{i}:00:00"})

    # Get only the 2 most recent transactions
    transactions = get_transactions(count=2)
    assert len(transactions) == 2
    assert transactions[0]["id"] == "txn-4"  # Most recent
    assert transactions[1]["id"] == "txn-3"


def test_get_transactions_empty_storage():
    """Test get_transactions with empty storage."""
    assert get_transactions() == []
    assert get_transactions(count=5) == []


def test_get_transactions_count_zero():
    """Test get_transactions with count=0."""
    add_transaction({"id": "txn-1"})

    transactions = get_transactions(count=0)
    assert transactions == []
