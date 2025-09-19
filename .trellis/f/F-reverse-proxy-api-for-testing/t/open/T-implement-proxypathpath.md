---
id: T-implement-proxypathpath
title: Implement /proxy/{path:path} handler with request forwarding
status: open
priority: high
parent: F-reverse-proxy-api-for-testing
prerequisites:
  - T-create-data-models-and-in
affectedFiles: {}
log: []
schema: v1.0
childrenIds: []
created: 2025-09-19T11:55:38.250Z
updated: 2025-09-19T11:55:38.250Z
---

# Implement /proxy/{path:path} Handler with Request Forwarding

## Context
This task implements the core proxy handler that forwards incoming requests to configured target URLs based on path prefix matching. It captures all request/response data for later querying by test fixtures.

**Related Feature**: F-reverse-proxy-api-for-testing - Reverse Proxy API for Testing
**Prerequisites**: T-create-data-models-and-in (data models and storage)

## Specific Implementation Requirements

### 1. Create Proxy Handler Module
Create `src/app/api/endpoints/proxy_handler.py` with the following structure:

- Import FastAPI, Request, Response, HTTPException
- Import httpx for outbound requests
- Import storage functions for config lookup and transaction recording
- Create APIRouter instance

### 2. Proxy Endpoint Implementation
```python
@router.api_route("/proxy/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy_request(request: Request, path: str) -> Response:
```

**Core Functionality**:
- Extract full path from request (everything after `/proxy/`)
- Use storage module to find matching prefix configuration
- Forward request to target URL using httpx
- Capture complete request/response data
- Return original response to caller

### 3. Request Processing Logic

**Path Matching**:
- Use `get_proxy_config(path)` from storage to find target URL
- Handle case where no prefix matches (return 404)
- Construct target URL: `{target_url}/{path}`

**Request Forwarding**:
- Preserve HTTP method from original request
- Forward all headers (clean up `host` header appropriately) 
- Forward query parameters using `request.query_params`
- Forward request body using `await request.body()`
- Use httpx.AsyncClient for outbound request

**Response Handling**:
- Capture response status, headers, and body
- Return FastAPI Response with exact status and headers
- Store transaction data before returning response

### 4. Transaction Data Capture
Before returning response, store complete transaction:
- Generate unique transaction ID (UUID)
- Record timestamp
- Capture request data: method, URL, headers, body, query params
- Capture response data: status code, headers, body
- Store which proxy mapping was used
- Use `add_transaction()` from storage module

### 5. Error Handling
- **404 Not Found**: No configured prefix matches the requested path
- **502 Bad Gateway**: Target server unreachable or connection failed
- **504 Gateway Timeout**: Target server response timeout
- **500 Internal Server Error**: Unexpected proxy failures

### 6. Integration with Router
Update `src/app/api/router.py` to include proxy handler routes

## Technical Approach

### Implementation Steps
1. Create proxy_handler.py following existing endpoint patterns
2. Implement async httpx client for outbound requests
3. Add path matching logic using storage functions
4. Implement request/response forwarding with proper header handling
5. Add transaction capture and storage
6. Handle errors gracefully with appropriate HTTP status codes
7. Write comprehensive unit tests

### httpx Client Usage
```python
async with httpx.AsyncClient() as client:
    response = await client.request(
        method=request.method,
        url=target_url,
        headers=dict(request.headers),
        params=request.query_params,
        content=await request.body()
    )
```

### Dependencies
- Use existing httpx dependency for HTTP client
- Import Request, Response from FastAPI
- Use storage functions from core/storage.py
- Generate UUIDs for transaction IDs
- Follow async patterns from existing codebase

## Acceptance Criteria

### Functional Requirements
- Proxy handler accepts all HTTP methods (GET, POST, PUT, DELETE, etc.)
- Correctly matches path prefixes using longest-match algorithm
- Forwards complete request data to target URL
- Returns exact response from target server
- Captures and stores complete transaction data
- Handles requests with query parameters and request bodies

### Path Matching Examples
- Configuration: `{"/v1/users": "https://api.example.com"}`
- Request: `/proxy/v1/users/123` → forwards to `https://api.example.com/v1/users/123`
- Request: `/proxy/v1/users/456/profile` → forwards to `https://api.example.com/v1/users/456/profile`
- Request: `/proxy/v2/orders` → returns 404 (no matching prefix)

### HTTP Compliance
- Preserves request method, headers, query params, body
- Returns response with original status code and headers
- Handles various content types (JSON, form data, files)
- Maintains HTTP semantics for all methods

### Transaction Recording
- Each proxy request generates unique transaction record
- Transaction includes complete request/response metadata
- Transactions stored in chronological order
- Failed requests also recorded (with error details)

### Error Handling
- Returns 404 for unmatched paths with clear error message
- Returns 502 for upstream connection failures
- Returns 504 for upstream timeouts
- Logs errors appropriately without exposing sensitive data

### Code Quality
- Async implementation with proper error handling
- Type hints for all function parameters and returns
- Unit tests cover successful forwarding, errors, edge cases
- Integration tests verify end-to-end proxy functionality
- Code follows project style and passes quality checks

## Testing Requirements
Write unit tests covering:
- Successful request forwarding for different HTTP methods
- Path prefix matching with various configured mappings
- Request/response data preservation (headers, body, query params)
- Transaction capture and storage verification
- Error scenarios: no matching prefix, upstream failures
- Edge cases: empty body, special headers, large responses

## Out of Scope
- Setup endpoint implementation (separate task)
- Transaction query endpoint (separate task)
- Advanced load balancing or retry logic
- Persistent transaction storage
- Authentication/authorization for proxy requests