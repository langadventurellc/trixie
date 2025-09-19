"""Setup request model for reverse proxy API."""

from typing import Dict

from pydantic import BaseModel, Field, field_validator


class SetupRequest(BaseModel):
    """Request model for POST /api/setup endpoint."""

    mappings: Dict[str, str] = Field(
        ...,
        description="Path prefix to target URL mappings",
        examples=[{"/v1/users": "https://api.example.com", "/v2/orders": "https://orders.api.com"}],
    )

    @field_validator("mappings")
    @classmethod
    def validate_mappings(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate path prefixes and target URLs."""
        for prefix, target_url in v.items():
            # Validate path prefix starts with "/"
            if not prefix.startswith("/"):
                raise ValueError(f"Path prefix '{prefix}' must start with '/'")

            # Validate target URL is HTTP/HTTPS
            if not target_url.startswith(("http://", "https://")):
                raise ValueError(f"Target URL '{target_url}' must be a valid HTTP/HTTPS URL")

        return v
