---
id: F-reverse-proxy-api-for-testing
title: Reverse Proxy API for Testing
status: in-progress
priority: medium
parent: none
prerequisites: []
affectedFiles:
  pyproject.toml: Added pytest>=8.0.0 to dev dependencies for testing framework;
    Added pytest-asyncio>=0.21.0 to dev dependencies to support async test
    execution
  src/app/api/models/__init__.py: Created models package directory
  src/app/api/models/setup_request.py: Created SetupRequest Pydantic model with URL and path prefix validation
  src/app/api/models/setup_response.py: Created SetupResponse Pydantic model for API responses
  src/app/api/models/transaction_record.py: Created TransactionRecord Pydantic model for transaction data
  src/app/api/models/transactions_response.py: Created TransactionsResponse Pydantic model for transaction lists
  src/app/core/__init__.py: Created core package directory
  src/app/core/storage_data.py: Created global storage variables for proxy
    configurations and transaction history
  src/app/core/add_proxy_config.py: Created function to add proxy configuration mappings
  src/app/core/get_proxy_config.py: Created function with longest-prefix-first matching algorithm for routing
  src/app/core/clear_proxy_configs.py: Created function to clear all proxy configurations
  src/app/core/add_transaction.py: Created function to add transactions to history
  src/app/core/get_transactions.py: Created function to retrieve transactions in
    reverse chronological order with optional count limit
  tests/__init__.py: Created tests package directory
  tests/test_setup_request.py: Created comprehensive tests for SetupRequest model validation
  tests/test_setup_response.py: Created tests for SetupResponse model
  tests/test_transaction_record.py: Created tests for TransactionRecord model serialization
  tests/test_transactions_response.py: Created tests for TransactionsResponse model
  tests/test_storage_functions.py: Created comprehensive tests for all storage
    functions including prefix matching algorithm and edge cases
  src/app/api/endpoints/proxy_setup.py: Created new endpoint module implementing
    POST /api/setup with async handler, URL validation, storage integration,
    error handling, and logging
  src/app/api/router.py: Modified to import and include proxy_setup router in main
    API router; Modified to import and include transactions router in main API
    router, making the endpoint accessible at /api/transactions with proper
    integration into existing FastAPI application structure.
  tests/test_proxy_setup_endpoint.py: Created comprehensive test suite with 6 test
    cases covering valid requests, error handling, and response format
    validation
  src/app/api/endpoints/proxy_handler.py: Created new proxy handler module with
    async endpoint that forwards HTTP requests to configured target URLs using
    httpx client, captures complete transaction data, and handles all error
    scenarios
  src/app/main.py: Modified to import and mount proxy router at root level (before
    API router) to enable /proxy/{path:path} endpoints without /api prefix
    conflicts
  tests/test_proxy_handler_endpoint.py: Created comprehensive test suite with 13
    test cases covering successful forwarding, all HTTP methods, header/query
    parameter forwarding, transaction recording, error handling, and response
    preservation
  src/app/api/endpoints/transactions.py: Created new endpoint module implementing
    GET /api/transactions with async handler, optional count parameter
    validation using FastAPI Query, transaction data transformation from storage
    dicts to TransactionRecord models, comprehensive error handling with
    HTTPException, and detailed logging for debugging and monitoring.
  tests/test_transactions_endpoint.py: "Created comprehensive test suite with 9
    test cases covering: all transactions retrieval without count, count
    limiting with various values, empty transaction history, storage error
    handling, data transformation accuracy, response model validation, and large
    transaction counts. All tests use proper mocking and async patterns."
log: []
schema: v1.0
childrenIds:
  - T-implement-get-apitransactions
  - T-update-main-api-router-to
  - T-create-data-models-and-in
  - T-implement-post-apisetup
  - T-implement-proxypathpath
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