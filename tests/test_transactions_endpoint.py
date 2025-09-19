"""Tests for transactions endpoint."""

from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.app.api.endpoints.transactions import get_transactions_endpoint
from src.app.api.models.transaction_record import TransactionRecord
from src.app.api.models.transactions_response import TransactionsResponse


class TestGetTransactionsEndpoint:
    """Test the get_transactions_endpoint function."""

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_get_all_transactions_no_count(self, mock_get_transactions):
        """Test getting all transactions without count parameter."""
        # Mock data - transaction dicts as returned by storage
        mock_transactions = [
            {
                "id": "txn-001",
                "timestamp": datetime(2024, 1, 1, 12, 0, 0),
                "request": {
                    "method": "GET",
                    "url": "/v1/users/123",
                    "headers": {"User-Agent": "test"},
                    "body": "",
                    "query_params": {},
                },
                "response": {
                    "status_code": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"id": 123, "name": "John"}',
                },
                "proxy_mapping_used": "/v1/users",
            },
            {
                "id": "txn-002",
                "timestamp": datetime(2024, 1, 1, 11, 0, 0),
                "request": {
                    "method": "POST",
                    "url": "/v1/users",
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"name": "Jane"}',
                    "query_params": {},
                },
                "response": {
                    "status_code": 201,
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"id": 124, "name": "Jane"}',
                },
                "proxy_mapping_used": "/v1/users",
            },
        ]
        mock_get_transactions.return_value = mock_transactions

        response = await get_transactions_endpoint()

        mock_get_transactions.assert_called_once()
        assert isinstance(response, TransactionsResponse)
        assert len(response.transactions) == 2
        assert response.count == 2
        assert all(isinstance(txn, TransactionRecord) for txn in response.transactions)
        assert response.transactions[0].id == "txn-001"
        assert response.transactions[1].id == "txn-002"

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_get_transactions_with_count_limit(self, mock_get_transactions):
        """Test getting transactions with count limit."""
        mock_transactions = [
            {
                "id": "txn-001",
                "timestamp": datetime(2024, 1, 1, 12, 0, 0),
                "request": {
                    "method": "GET",
                    "url": "/v1/users/123",
                    "headers": {},
                    "body": "",
                    "query_params": {},
                },
                "response": {"status_code": 200, "headers": {}, "body": "{}"},
                "proxy_mapping_used": "/v1/users",
            }
        ]
        mock_get_transactions.return_value = mock_transactions

        response = await get_transactions_endpoint(count=1)

        mock_get_transactions.assert_called_once_with(1)
        assert isinstance(response, TransactionsResponse)
        assert len(response.transactions) == 1
        assert response.count == 1
        assert response.transactions[0].id == "txn-001"

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_get_transactions_empty_history(self, mock_get_transactions):
        """Test getting transactions when history is empty."""
        mock_get_transactions.return_value = []

        response = await get_transactions_endpoint()

        mock_get_transactions.assert_called_once()
        assert isinstance(response, TransactionsResponse)
        assert len(response.transactions) == 0
        assert response.count == 0

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_get_transactions_with_count_five(self, mock_get_transactions):
        """Test getting transactions with count=5."""
        mock_transactions = [
            {
                "id": f"txn-{i:03d}",
                "timestamp": datetime(2024, 1, 1, 12, i, 0),
                "request": {
                    "method": "GET",
                    "url": f"/v1/users/{i}",
                    "headers": {},
                    "body": "",
                    "query_params": {},
                },
                "response": {"status_code": 200, "headers": {}, "body": "{}"},
                "proxy_mapping_used": "/v1/users",
            }
            for i in range(5)
        ]
        mock_get_transactions.return_value = mock_transactions

        response = await get_transactions_endpoint(count=5)

        mock_get_transactions.assert_called_once_with(5)
        assert isinstance(response, TransactionsResponse)
        assert len(response.transactions) == 5
        assert response.count == 5

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_get_transactions_storage_error(self, mock_get_transactions):
        """Test handling of storage function failure."""
        mock_get_transactions.side_effect = Exception("Storage error")

        with pytest.raises(HTTPException) as exc_info:
            await get_transactions_endpoint()

        assert exc_info.value.status_code == 500
        assert "Internal server error" in exc_info.value.detail

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_transaction_record_transformation(self, mock_get_transactions):
        """Test that transaction dicts are properly transformed to TransactionRecord models."""
        mock_transaction = {
            "id": "test-id",
            "timestamp": datetime(2024, 1, 1, 12, 0, 0),
            "request": {
                "method": "PUT",
                "url": "/v1/users/123",
                "headers": {"Authorization": "Bearer token"},
                "body": '{"name": "Updated"}',
                "query_params": {"include": "profile"},
            },
            "response": {
                "status_code": 200,
                "headers": {"Content-Type": "application/json"},
                "body": '{"id": 123, "name": "Updated"}',
            },
            "proxy_mapping_used": "/v1/users",
        }
        mock_get_transactions.return_value = [mock_transaction]

        response = await get_transactions_endpoint()

        assert len(response.transactions) == 1
        txn = response.transactions[0]
        assert isinstance(txn, TransactionRecord)
        assert txn.id == "test-id"
        assert txn.timestamp == datetime(2024, 1, 1, 12, 0, 0)
        assert txn.request["method"] == "PUT"
        assert txn.request["url"] == "/v1/users/123"
        assert txn.response["status_code"] == 200
        assert txn.proxy_mapping_used == "/v1/users"

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_response_model_format(self, mock_get_transactions):
        """Test that response matches TransactionsResponse model format."""
        mock_get_transactions.return_value = []

        response = await get_transactions_endpoint()

        assert isinstance(response, TransactionsResponse)
        assert hasattr(response, "transactions")
        assert hasattr(response, "count")
        assert isinstance(response.transactions, list)
        assert isinstance(response.count, int)

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_count_parameter_validation_handled_by_fastapi(self, mock_get_transactions):
        """Test that FastAPI Query validation handles invalid count parameters.

        Note: This test verifies the endpoint works with valid count.
        Invalid count values (0, negative) are handled by FastAPI Query validation
        and will return 422 Unprocessable Entity before reaching our endpoint.
        """
        mock_get_transactions.return_value = []

        # Test with minimum valid count
        response = await get_transactions_endpoint(count=1)

        mock_get_transactions.assert_called_once_with(1)
        assert isinstance(response, TransactionsResponse)
        assert response.count == 0

    @patch("src.app.api.endpoints.transactions.get_transactions")
    @pytest.mark.asyncio
    async def test_large_transaction_count(self, mock_get_transactions):
        """Test handling large transaction counts."""
        # Create 100 mock transactions
        mock_transactions = [
            {
                "id": f"txn-{i:03d}",
                "timestamp": datetime(2024, 1, 1, 12, i % 60, 0),
                "request": {
                    "method": "GET",
                    "url": f"/v1/resource/{i}",
                    "headers": {},
                    "body": "",
                    "query_params": {},
                },
                "response": {"status_code": 200, "headers": {}, "body": "{}"},
                "proxy_mapping_used": "/v1/resource",
            }
            for i in range(100)
        ]
        mock_get_transactions.return_value = mock_transactions

        response = await get_transactions_endpoint(count=100)

        mock_get_transactions.assert_called_once_with(100)
        assert len(response.transactions) == 100
        assert response.count == 100
        assert all(isinstance(txn, TransactionRecord) for txn in response.transactions)
