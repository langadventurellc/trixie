"""Tests for SetupResponse model."""

from src.app.api.models.setup_response import SetupResponse


def test_setup_response_valid_data():
    """Test SetupResponse with valid data."""
    data = {
        "success": True,
        "configured_mappings": {"/v1/users": "https://api.example.com"},
        "message": "Configuration updated successfully",
    }
    response = SetupResponse(**data)
    assert response.success is True
    assert response.configured_mappings == {"/v1/users": "https://api.example.com"}
    assert response.message == "Configuration updated successfully"


def test_setup_response_failure():
    """Test SetupResponse for failure case."""
    data = {
        "success": False,
        "configured_mappings": {},
        "message": "Configuration failed due to invalid URLs",
    }
    response = SetupResponse(**data)
    assert response.success is False
    assert response.configured_mappings == {}
    assert response.message == "Configuration failed due to invalid URLs"
