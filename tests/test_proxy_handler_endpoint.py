from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from src.app.main import app


class TestProxyHandler:
    """Test suite for proxy handler endpoint functionality."""

    def setup_method(self):
        """Set up test client and common test data."""
        self.client = TestClient(app)
        self.test_target_url = "https://api.example.com"
        self.test_path = "v1/users/123"

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_successful_proxy_get_request(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test successful GET request forwarding."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.content = b'{"id": 123, "name": "test"}'
        mock_response.text = '{"id": 123, "name": "test"}'
        mock_httpx.return_value = mock_response

        # Make request
        response = self.client.get(f"/proxy/{self.test_path}")

        # Verify response
        assert response.status_code == 200
        assert response.json() == {"id": 123, "name": "test"}

        # Verify proxy config was called
        mock_get_config.assert_called_once_with(self.test_path)

        # Verify httpx request was made correctly
        mock_httpx.assert_called_once()
        call_args = mock_httpx.call_args
        assert call_args[1]["method"] == "GET"
        assert call_args[1]["url"] == f"{self.test_target_url}/{self.test_path}"

        # Verify transaction was recorded
        mock_add_transaction.assert_called_once()
        transaction_data = mock_add_transaction.call_args[0][0]
        assert transaction_data["request"]["method"] == "GET"
        assert transaction_data["response"]["status_code"] == 200

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_successful_proxy_post_request(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test successful POST request with body forwarding."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 201
        mock_response.headers = {"content-type": "application/json"}
        mock_response.content = b'{"id": 456, "created": true}'
        mock_response.text = '{"id": 456, "created": true}'
        mock_httpx.return_value = mock_response

        # Test data
        test_data = {"name": "new user", "email": "test@example.com"}

        # Make request
        response = self.client.post(f"/proxy/{self.test_path}", json=test_data)

        # Verify response
        assert response.status_code == 201
        assert response.json() == {"id": 456, "created": True}

        # Verify httpx request included body
        mock_httpx.assert_called_once()
        call_args = mock_httpx.call_args
        assert call_args[1]["method"] == "POST"
        assert call_args[1]["content"] is not None

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_all_http_methods_supported(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test that all HTTP methods are supported."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.content = b"success"
        mock_response.text = "success"
        mock_httpx.return_value = mock_response

        # Test each HTTP method
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        for method in methods:
            response = self.client.request(method, f"/proxy/{self.test_path}")
            assert response.status_code == 200, f"Method {method} failed"

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_headers_forwarding(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test that headers are properly forwarded (except host)."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.content = b"success"
        mock_response.text = "success"
        mock_httpx.return_value = mock_response

        # Custom headers
        custom_headers = {
            "Authorization": "Bearer token123",
            "Content-Type": "application/json",
            "X-Custom-Header": "custom-value",
        }

        # Make request with custom headers
        self.client.get(f"/proxy/{self.test_path}", headers=custom_headers)

        # Verify httpx was called with headers (minus host)
        call_args = mock_httpx.call_args
        forwarded_headers = call_args[1]["headers"]

        # Verify custom headers were forwarded (headers are lowercase in httpx)
        assert "authorization" in forwarded_headers
        assert "content-type" in forwarded_headers
        assert "x-custom-header" in forwarded_headers

        # Verify host header was removed
        assert "host" not in forwarded_headers

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_query_parameters_forwarding(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test that query parameters are properly forwarded."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.content = b"success"
        mock_response.text = "success"
        mock_httpx.return_value = mock_response

        # Make request with query parameters
        self.client.get(f"/proxy/{self.test_path}?limit=10&offset=20")

        # Verify query parameters were forwarded
        call_args = mock_httpx.call_args
        assert call_args[1]["params"]["limit"] == "10"
        assert call_args[1]["params"]["offset"] == "20"

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    def test_no_proxy_config_returns_404(self, mock_get_config):
        """Test that 404 is returned when no proxy config matches path."""
        # Setup mock to return None (no config found)
        mock_get_config.return_value = None

        # Make request
        response = self.client.get("/proxy/unknown/path")

        # Verify 404 response
        assert response.status_code == 404
        assert "No proxy configuration found" in response.json()["detail"]

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("httpx.AsyncClient.request")
    def test_upstream_server_error_returns_502(self, mock_httpx, mock_get_config):
        """Test that 502 is returned for upstream connection failures."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_httpx.side_effect = httpx.ConnectError("Connection failed")

        # Make request
        response = self.client.get(f"/proxy/{self.test_path}")

        # Verify 502 response
        assert response.status_code == 502
        assert "Failed to connect to target server" in response.json()["detail"]

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("httpx.AsyncClient.request")
    def test_upstream_timeout_returns_504(self, mock_httpx, mock_get_config):
        """Test that 504 is returned for upstream timeouts."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_httpx.side_effect = httpx.TimeoutException("Request timeout")

        # Make request
        response = self.client.get(f"/proxy/{self.test_path}")

        # Verify 504 response
        assert response.status_code == 504
        assert "Timeout connecting to target server" in response.json()["detail"]

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_transaction_recording(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test that transaction data is properly recorded."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.content = b'{"result": "success"}'
        mock_response.text = '{"result": "success"}'
        mock_httpx.return_value = mock_response

        # Make request
        self.client.get(f"/proxy/{self.test_path}?test=true")

        # Verify transaction was recorded
        mock_add_transaction.assert_called_once()
        transaction_data = mock_add_transaction.call_args[0][0]

        # Check transaction structure
        assert "id" in transaction_data
        assert "timestamp" in transaction_data
        assert "request" in transaction_data
        assert "response" in transaction_data
        assert "proxy_mapping_used" in transaction_data

        # Check request data
        request_data = transaction_data["request"]
        assert request_data["method"] == "GET"
        assert request_data["url"] == f"{self.test_target_url}/{self.test_path}"
        assert request_data["query_params"]["test"] == "true"

        # Check response data
        response_data = transaction_data["response"]
        assert response_data["status_code"] == 200
        assert response_data["body"] == '{"result": "success"}'

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_response_headers_preserved(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test that response headers from upstream are preserved."""
        # Setup mocks
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {
            "content-type": "application/json",
            "x-custom-header": "custom-value",
            "cache-control": "no-cache",
        }
        mock_response.content = b'{"data": "test"}'
        mock_response.text = '{"data": "test"}'
        mock_httpx.return_value = mock_response

        # Make request
        response = self.client.get(f"/proxy/{self.test_path}")

        # Verify response headers are preserved
        assert response.headers["content-type"] == "application/json"
        assert response.headers["x-custom-header"] == "custom-value"
        assert response.headers["cache-control"] == "no-cache"

    @patch("src.app.api.endpoints.proxy_handler.get_proxy_config")
    @patch("src.app.api.endpoints.proxy_handler.add_transaction")
    @patch("httpx.AsyncClient.request")
    def test_longest_prefix_matching(self, mock_httpx, mock_add_transaction, mock_get_config):
        """Test that longest prefix matching works correctly."""
        # Setup mocks - get_proxy_config already implements longest-prefix matching
        mock_get_config.return_value = self.test_target_url
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.content = b"success"
        mock_response.text = "success"
        mock_httpx.return_value = mock_response

        # Test various paths
        test_paths = ["v1/users/123", "v1/users/456/profile", "v1/users/456/profile/settings"]

        for path in test_paths:
            response = self.client.get(f"/proxy/{path}")
            assert response.status_code == 200

            # Verify get_proxy_config was called with the full path
            mock_get_config.assert_called_with(path)
