"""Integration tests for complete proxy workflow through main FastAPI app."""

import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from src.app.main import app


class TestCompleteProxyWorkflow:
    """Test complete end-to-end proxy workflow through main FastAPI application."""

    def setup_method(self):
        """Set up test client and clear storage before each test."""
        self.client = TestClient(app)
        # Clear storage before each test
        from src.app.core.storage_data import proxy_configurations, transaction_history

        proxy_configurations.clear()
        transaction_history.clear()

    def test_complete_workflow_setup_proxy_query(self):
        """Test complete workflow: setup → proxy request → query transactions."""
        # Step 1: Setup proxy configuration
        setup_data = {"mappings": {"/api/users": "https://jsonplaceholder.typicode.com"}}

        setup_response = self.client.post("/api/setup", json=setup_data)
        assert setup_response.status_code == 200
        setup_result = setup_response.json()
        assert setup_result["success"] is True
        assert "Configured 1 proxy mappings" in setup_result["message"]

        # Step 2: Make proxy request (with mocked external response)
        mock_response_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}

        with patch("httpx.AsyncClient.request") as mock_request:
            mock_response = AsyncMock(spec=Response)
            mock_response.status_code = 200
            mock_response.headers = {"content-type": "application/json"}
            mock_response.text = json.dumps(mock_response_data)
            mock_response.content = json.dumps(mock_response_data).encode()
            mock_request.return_value = mock_response

            proxy_response = self.client.get("/proxy/api/users/1")
            assert proxy_response.status_code == 200
            assert proxy_response.json() == mock_response_data

        # Step 3: Query transactions to verify capture
        transactions_response = self.client.get("/api/transactions")
        assert transactions_response.status_code == 200
        transactions_data = transactions_response.json()

        assert "transactions" in transactions_data
        assert len(transactions_data["transactions"]) == 1

        transaction = transactions_data["transactions"][0]
        assert transaction["request"]["method"] == "GET"
        assert transaction["request"]["url"] == "https://jsonplaceholder.typicode.com/api/users/1"
        assert transaction["response"]["status_code"] == 200
        assert transaction["response"]["body"] == json.dumps(mock_response_data)

    def test_multiple_proxy_requests_with_different_prefixes(self):
        """Test workflow with multiple proxy configurations and requests."""
        # Setup multiple proxy configurations
        setup_data = {
            "mappings": {
                "/api/users": "https://api1.example.com",
                "/api/posts": "https://api2.example.com",
            }
        }

        setup_response = self.client.post("/api/setup", json=setup_data)
        assert setup_response.status_code == 200

        # Make requests to different proxy endpoints
        with patch("httpx.AsyncClient.request") as mock_request:
            # First request
            mock_response1 = AsyncMock(spec=Response)
            mock_response1.status_code = 200
            mock_response1.headers = {"content-type": "application/json"}
            mock_response1.text = '{"user_id": 1}'
            mock_response1.content = b'{"user_id": 1}'

            # Second request
            mock_response2 = AsyncMock(spec=Response)
            mock_response2.status_code = 201
            mock_response2.headers = {"content-type": "application/json"}
            mock_response2.text = '{"post_id": 123}'
            mock_response2.content = b'{"post_id": 123}'

            mock_request.side_effect = [mock_response1, mock_response2]

            # Make both requests
            response1 = self.client.get("/proxy/api/users/1")
            response2 = self.client.post("/proxy/api/posts", json={"title": "Test"})

            assert response1.status_code == 200
            assert response2.status_code == 201

        # Verify both transactions captured
        transactions_response = self.client.get("/api/transactions")
        transactions_data = transactions_response.json()

        assert len(transactions_data["transactions"]) == 2
        # Should be in reverse chronological order (newest first)
        assert transactions_data["transactions"][0]["request"]["method"] == "POST"
        assert transactions_data["transactions"][1]["request"]["method"] == "GET"

    def test_workflow_with_no_matching_prefix(self):
        """Test proxy request with no matching configuration."""
        # Setup configuration
        setup_data = {"url_mappings": {"/api/users": "https://example.com"}}
        self.client.post("/api/setup", json=setup_data)

        # Try proxy request with non-matching prefix
        response = self.client.get("/proxy/api/posts/1")
        assert response.status_code == 404
        assert "No proxy configuration found" in response.json()["detail"]

        # Verify no transaction was recorded for failed request
        transactions_response = self.client.get("/api/transactions")
        transactions_data = transactions_response.json()
        assert len(transactions_data["transactions"]) == 0

    def test_workflow_with_count_parameter(self):
        """Test transaction querying with count parameter."""
        # Setup and make multiple requests
        setup_data = {"mappings": {"/api/test": "https://example.com"}}
        self.client.post("/api/setup", json=setup_data)

        with patch("httpx.AsyncClient.request") as mock_request:
            mock_response = AsyncMock(spec=Response)
            mock_response.status_code = 200
            mock_response.headers = {}
            mock_response.text = "OK"
            mock_response.content = b"OK"
            mock_request.return_value = mock_response

            # Make 5 requests
            for i in range(5):
                self.client.get(f"/proxy/api/test/{i}")

        # Query with count parameter
        transactions_response = self.client.get("/api/transactions?count=3")
        transactions_data = transactions_response.json()

        assert len(transactions_data["transactions"]) == 3
        # Should get the 3 most recent transactions

    def test_health_check_remains_functional(self):
        """Verify existing health check endpoint still works after router integration."""
        response = self.client.get("/api/health")
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_fastapi_docs_include_all_endpoints(self):
        """Verify FastAPI automatic documentation includes all endpoints."""
        # Test OpenAPI schema generation
        response = self.client.get("/openapi.json")
        assert response.status_code == 200

        openapi_schema = response.json()
        paths = openapi_schema["paths"]

        # Verify all expected endpoints are documented
        assert "/api/health" in paths
        assert "/api/setup" in paths
        assert "/api/transactions" in paths
        assert "/proxy/{path}" in paths

        # Verify methods are correct
        assert "get" in paths["/api/health"]
        assert "post" in paths["/api/setup"]
        assert "get" in paths["/api/transactions"]
        # Proxy handler should support multiple methods
        proxy_methods = list(paths["/proxy/{path}"].keys())
        assert len(proxy_methods) > 1  # Should support multiple HTTP methods

    def test_error_handling_across_endpoints(self):
        """Test error scenarios work correctly across all integrated endpoints."""
        # Test setup with invalid data
        response = self.client.post("/api/setup", json={"invalid": "data"})
        assert response.status_code == 422  # Validation error

        # Test transactions endpoint error handling
        with patch("src.app.api.endpoints.transactions.get_transactions") as mock_get:
            mock_get.side_effect = Exception("Storage error")
            response = self.client.get("/api/transactions")
            assert response.status_code == 500

        # Test proxy with upstream error
        setup_data = {"mappings": {"/api/test": "https://example.com"}}
        self.client.post("/api/setup", json=setup_data)

        with patch("httpx.AsyncClient.request") as mock_request:
            mock_request.side_effect = Exception("Connection error")
            response = self.client.get("/proxy/api/test/1")
            assert response.status_code == 500
