from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pyla_logger import logger

from ...core.add_transaction import add_transaction
from ...core.get_proxy_config import get_proxy_config

router = APIRouter()


@router.get("/proxy/{path:path}", operation_id="proxy_request_get")
@router.post("/proxy/{path:path}", operation_id="proxy_request_post")
@router.put("/proxy/{path:path}", operation_id="proxy_request_put")
@router.delete("/proxy/{path:path}", operation_id="proxy_request_delete")
@router.patch("/proxy/{path:path}", operation_id="proxy_request_patch")
@router.head("/proxy/{path:path}", operation_id="proxy_request_head")
@router.options("/proxy/{path:path}", operation_id="proxy_request_options")
async def proxy_request(request: Request, path: str) -> StreamingResponse:
    """Forward HTTP requests to configured target URLs based on path prefix matching.

    Captures complete request/response data for later querying by test fixtures.

    Args:
        request: The incoming FastAPI request object
        path: The path portion after /proxy/ (captured by {path:path})

    Returns:
        Response object with exact data from target server

    Raises:
        HTTPException: 404 if no proxy config matches path
        HTTPException: 502 if upstream server unreachable
        HTTPException: 500 for unexpected errors
    """
    # Find target URL using longest-prefix matching
    # Add leading slash to path since configurations are stored with leading slash
    normalized_path = f"/{path}" if not path.startswith("/") else path
    target_url = get_proxy_config(normalized_path)
    if target_url is None:
        logger.warning(f"No proxy configuration found for path: {path}")
        raise HTTPException(
            status_code=404, detail=f"No proxy configuration found for path: {path}"
        )

    # Construct full target URL
    full_target_url = f"{target_url.rstrip('/')}/{normalized_path.lstrip('/')}"

    # Prepare request data for forwarding
    request_headers = dict(request.headers)
    # Remove host header to avoid conflicts with target server
    request_headers.pop("host", None)

    request_body = await request.body()
    query_params = dict(request.query_params)

    # Generate transaction ID for tracking
    transaction_id = str(uuid4())
    transaction_timestamp = datetime.now(timezone.utc).isoformat()

    try:
        # Forward request to target server
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=full_target_url,
                headers=request_headers,
                params=query_params,
                content=request_body,
            )

        # Read the response content once
        response_body = await response.aread()
        response_chunks = [response_body] if response_body else []

        # Prepare transaction data for storage
        transaction_data: dict[str, Any] = {
            "id": transaction_id,
            "timestamp": transaction_timestamp,
            "request": {
                "method": request.method,
                "url": full_target_url,
                "headers": dict(request.headers),
                "query_params": query_params,
                "body": request_body.decode("utf-8", errors="replace") if request_body else "",
            },
            "response": {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response_body.decode("utf-8", errors="replace"),
            },
            "proxy_mapping_used": f"{normalized_path} -> {target_url}",
        }

        # Store transaction data
        add_transaction(transaction_data)

        # Create async generator to stream the captured chunks
        async def generate_response():
            for chunk in response_chunks:
                yield chunk

        # In proxy_handler.py
        headers = dict(response.headers)

        # Remove/replace conflicting headers that FastAPI will add
        headers.pop("server", None)  # Let FastAPI set this
        headers.pop("date", None)  # Let FastAPI set this

        return StreamingResponse(
            generate_response(),
            status_code=response.status_code,
            headers=headers,  # Now clean headers
        )

    except httpx.ConnectError as e:
        logger.error(f"Failed to connect to target server {full_target_url}: {e}")
        raise HTTPException(
            status_code=502, detail=f"Failed to connect to target server: {target_url}"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to target server {full_target_url}: {e}")
        raise HTTPException(
            status_code=504, detail=f"Timeout connecting to target server: {target_url}"
        )
    except Exception as e:
        logger.error(f"Unexpected error proxying request to {full_target_url}: {e}")
        raise HTTPException(status_code=500, detail="Internal proxy error")
