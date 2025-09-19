---
id: F-reverse-proxy-api-for-testing
title: Reverse Proxy API for Testing
status: open
priority: medium
parent: none
prerequisites: []
affectedFiles: {}
log: []
schema: v1.0
childrenIds: []
created: 2025-09-19T05:18:47.538Z
updated: 2025-09-19T05:18:47.538Z
---

# Reverse Proxy API for Testing

## Purpose
Implement a reverse proxy API that allows end-to-end tests to configure URL forwarding, capture HTTP transactions, and query request/response data for test assertions.

## Core Requirements

### 1. Setup Endpoint (`POST /api/setup`)
Configure path prefix to target URL mappings for the proxy to use.

### 2. Proxy Handler (`/proxy/{path:path}`)
Forward requests to configured URLs based on path prefix matching and capture all request/response data.

### 3. Query Endpoint (`GET /api/transactions?count=N`)
Retrieve captured transaction history with optional count limit.

## Acceptance Criteria

### Setup Endpoint
- **Input**: JSON containing path prefix to target URL mappings
- **Behavior**: Store mappings in memory for use by proxy handler
- **Example**: `{"/v1/users": "https://api.example.com"}` configures `/v1/users` prefix
- **Response**: Confirm successful configuration

### Proxy Handler
- **Route**: `/proxy/{path:path}` accepts all HTTP methods
- **Matching Logic**: Find configured prefix that matches start of requested path
  - `/v1/users` matches `/v1/users/123`, `/v1/users/456/profile`, etc.
  - Forward to `{target_url}/{full_path}` where full_path includes everything after `/proxy/`
- **Request Forwarding**: Pass through HTTP method, headers, query parameters, and body
- **Response**: Return the upstream response exactly as received
- **Data Capture**: Store complete request and response data before returning response

### Query Endpoint
- **URL**: `GET /api/transactions?count=N`
- **Behavior**: Return captured transactions in reverse chronological order (newest first)
- **Count Parameter**: Optional limit on number of transactions returned
- **Response Format**: JSON array with complete request/response metadata including:
  - Request: method, URL, headers, body, query parameters
  - Response: status code, headers, body
  - Timestamp

## Technical Implementation

### Integration
- Follow existing FastAPI project structure in `src/app/api/endpoints/`
- Use existing `httpx` dependency for outbound requests
- Include new endpoints in main API router

### Data Storage
- In-memory storage (no persistence required)
- Store proxy configuration mappings
- Store transaction history as list of request/response pairs

### Error Handling
- Return appropriate HTTP status codes for common failure scenarios
- Handle cases where no prefix matches requested path
- Handle upstream connection failures

## Implementation Files
- `proxy_setup.py` - Setup endpoint
- `proxy_handler.py` - Proxy forwarding logic  
- `transactions.py` - Transaction query endpoint
- Add routes to existing `api/router.py`

## Quality Requirements
- Pass all existing code quality checks: `uv run poe quality`
- Pass tests: `uv run pytest`
- Follow existing code style and async patterns

This feature provides the core functionality needed for end-to-end test fixtures to configure, use, and query the reverse proxy without additional complexity.