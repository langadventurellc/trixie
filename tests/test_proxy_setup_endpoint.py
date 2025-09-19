"""Tests for proxy setup endpoint."""

from unittest.mock import patch

import pytest
from fastapi import HTTPException

from src.app.api.endpoints.proxy_setup import configure_proxy_mappings
from src.app.api.models.setup_request import SetupRequest
from src.app.api.models.setup_response import SetupResponse


class TestConfigureProxyMappings:
    """Test the configure_proxy_mappings endpoint function."""

    @patch("src.app.api.endpoints.proxy_setup.clear_proxy_configs")
    @patch("src.app.api.endpoints.proxy_setup.add_proxy_config")
    @pytest.mark.asyncio
    async def test_configure_single_mapping(self, mock_add, mock_clear):
        """Test configuring a single proxy mapping."""
        request = SetupRequest(mappings={"/v1/users": "https://api.example.com"})

        response = await configure_proxy_mappings(request)

        mock_clear.assert_called_once()
        mock_add.assert_called_once_with("/v1/users", "https://api.example.com")

        assert response.success is True
        assert response.configured_mappings == {"/v1/users": "https://api.example.com"}
        assert response.message == "Configured 1 proxy mappings"

    @patch("src.app.api.endpoints.proxy_setup.clear_proxy_configs")
    @patch("src.app.api.endpoints.proxy_setup.add_proxy_config")
    @pytest.mark.asyncio
    async def test_configure_multiple_mappings(self, mock_add, mock_clear):
        """Test configuring multiple proxy mappings."""
        mappings = {
            "/v1/users": "https://api.example.com",
            "/v2/orders": "https://orders.service.com",
            "/v1/products": "https://products.api.com",
        }
        request = SetupRequest(mappings=mappings)

        response = await configure_proxy_mappings(request)

        mock_clear.assert_called_once()
        assert mock_add.call_count == 3
        mock_add.assert_any_call("/v1/users", "https://api.example.com")
        mock_add.assert_any_call("/v2/orders", "https://orders.service.com")
        mock_add.assert_any_call("/v1/products", "https://products.api.com")

        assert response.success is True
        assert response.configured_mappings == mappings
        assert response.message == "Configured 3 proxy mappings"

    @patch("src.app.api.endpoints.proxy_setup.clear_proxy_configs")
    @patch("src.app.api.endpoints.proxy_setup.add_proxy_config")
    @pytest.mark.asyncio
    async def test_configure_empty_mappings(self, mock_add, mock_clear):
        """Test configuring with empty mappings."""
        request = SetupRequest(mappings={})

        response = await configure_proxy_mappings(request)

        mock_clear.assert_called_once()
        mock_add.assert_not_called()

        assert response.success is True
        assert response.configured_mappings == {}
        assert response.message == "Configured 0 proxy mappings"

    @patch("src.app.api.endpoints.proxy_setup.clear_proxy_configs")
    @patch("src.app.api.endpoints.proxy_setup.add_proxy_config")
    @pytest.mark.asyncio
    async def test_clear_configs_failure(self, mock_add, mock_clear):
        """Test handling of clear_proxy_configs failure."""
        mock_clear.side_effect = Exception("Storage error")
        request = SetupRequest(mappings={"/v1/test": "https://test.com"})

        with pytest.raises(HTTPException) as exc_info:
            await configure_proxy_mappings(request)

        assert exc_info.value.status_code == 500
        assert "Internal server error" in exc_info.value.detail
        mock_add.assert_not_called()

    @patch("src.app.api.endpoints.proxy_setup.clear_proxy_configs")
    @patch("src.app.api.endpoints.proxy_setup.add_proxy_config")
    @pytest.mark.asyncio
    async def test_add_config_failure(self, mock_add, mock_clear):
        """Test handling of add_proxy_config failure."""
        mock_add.side_effect = Exception("Storage error")
        request = SetupRequest(mappings={"/v1/test": "https://test.com"})

        with pytest.raises(HTTPException) as exc_info:
            await configure_proxy_mappings(request)

        assert exc_info.value.status_code == 500
        assert "Internal server error" in exc_info.value.detail
        mock_clear.assert_called_once()

    @patch("src.app.api.endpoints.proxy_setup.clear_proxy_configs")
    @patch("src.app.api.endpoints.proxy_setup.add_proxy_config")
    @pytest.mark.asyncio
    async def test_response_model_format(self, mock_add, mock_clear):
        """Test that response matches SetupResponse model format."""
        request = SetupRequest(mappings={"/api/test": "https://example.com"})

        response = await configure_proxy_mappings(request)

        # Ensure response is proper SetupResponse instance
        assert isinstance(response, SetupResponse)
        assert hasattr(response, "success")
        assert hasattr(response, "configured_mappings")
        assert hasattr(response, "message")
        assert isinstance(response.success, bool)
        assert isinstance(response.configured_mappings, dict)
        assert isinstance(response.message, str)
