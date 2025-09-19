"""Setup response model for reverse proxy API."""

from typing import Dict

from pydantic import BaseModel, Field


class SetupResponse(BaseModel):
    """Response model for POST /api/setup endpoint."""

    success: bool = Field(..., description="Whether the setup was successful")
    configured_mappings: Dict[str, str] = Field(
        ..., description="The mappings that were configured"
    )
    message: str = Field(..., description="Human-readable status message")
