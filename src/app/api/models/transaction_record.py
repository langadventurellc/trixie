"""Transaction record model for reverse proxy API."""

from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class TransactionRecord(BaseModel):
    """Model for a single transaction record."""

    id: str = Field(..., description="Unique transaction identifier")
    timestamp: datetime = Field(..., description="When the transaction occurred")
    request: Dict = Field(
        ..., description="Complete request data (method, url, headers, body, etc.)"
    )
    response: Dict = Field(..., description="Complete response data (status, headers, body)")
    proxy_mapping_used: str = Field(
        ..., description="Which path prefix mapping was used for this transaction"
    )
