"""Tests for SetupRequest model."""

import pytest
from pydantic import ValidationError

from src.app.api.models.setup_request import SetupRequest


def test_setup_request_valid_mappings():
    """Test SetupRequest with valid path mappings."""
    valid_data = {
        "mappings": {
            "/v1/users": "https://api.example.com",
            "/v2/orders": "http://orders.api.com",
            "/api/products": "https://products.example.org",
        }
    }
    request = SetupRequest(**valid_data)
    assert request.mappings == valid_data["mappings"]


def test_setup_request_invalid_path_prefix():
    """Test SetupRequest with invalid path prefix (missing leading slash)."""
    invalid_data = {"mappings": {"v1/users": "https://api.example.com"}}
    with pytest.raises(ValidationError, match="Path prefix 'v1/users' must start with '/'"):
        SetupRequest(**invalid_data)


def test_setup_request_invalid_url_scheme():
    """Test SetupRequest with invalid URL scheme."""
    invalid_data = {"mappings": {"/v1/users": "ftp://api.example.com"}}
    with pytest.raises(
        ValidationError, match="Target URL 'ftp://api.example.com' must be a valid HTTP/HTTPS URL"
    ):
        SetupRequest(**invalid_data)


def test_setup_request_empty_mappings():
    """Test SetupRequest with empty mappings."""
    request = SetupRequest(mappings={})
    assert request.mappings == {}


def test_setup_request_multiple_invalid_entries():
    """Test SetupRequest with multiple invalid entries."""
    invalid_data = {
        "mappings": {
            "no-slash": "https://api.example.com",  # Invalid prefix
            "/v1/users": "ftp://api.example.com",  # Invalid URL
        }
    }
    with pytest.raises(ValidationError):
        SetupRequest(**invalid_data)
