---
id: T-implement-post-apisetup
title: Implement POST /api/setup endpoint with validation
status: done
priority: high
parent: F-reverse-proxy-api-for-testing
prerequisites:
  - T-create-data-models-and-in
affectedFiles:
  src/app/api/endpoints/proxy_setup.py: Created new endpoint module implementing
    POST /api/setup with async handler, URL validation, storage integration,
    error handling, and logging
  src/app/api/router.py: Modified to import and include proxy_setup router in main API router
  tests/test_proxy_setup_endpoint.py: Created comprehensive test suite with 6 test
    cases covering valid requests, error handling, and response format
    validation
  pyproject.toml: Added pytest-asyncio>=0.21.0 to dev dependencies to support
    async test execution
log:
  - Successfully implemented POST /api/setup endpoint with comprehensive
    validation and error handling. The endpoint allows test fixtures to
    configure proxy forwarding rules by accepting path prefix to target URL
    mappings, clearing existing configurations, and storing new mappings in
    memory. Added robust validation through existing SetupRequest/SetupResponse
    models, proper error handling with HTTPException, and comprehensive logging.
    Includes full test coverage with 6 test cases covering valid requests, empty
    mappings, error scenarios, and response format validation. All quality
    checks pass and pytest-asyncio was added to support async endpoint testing.
schema: v1.0
childrenIds: []
created: 2025-09-19T11:55:06.083Z
updated: 2025-09-19T11:55:06.083Z
---

# Implement POST /api/setup Endpoint with Validation

## Context
This task implements the setup endpoint that allows test fixtures to configure proxy forwarding rules. The endpoint accepts path prefix to target URL mappings and stores them in memory for use by the proxy handler.

**Related Feature**: F-reverse-proxy-api-for-testing - Reverse Proxy API for Testing
**Prerequisites**: T-create-data-models-and-in (data models and storage)

## Specific Implementation Requirements

### 1. Create Setup Endpoint Module
Create `src/app/api/endpoints/proxy_setup.py` following the existing pattern from `health_check.py`:

- Import required dependencies: FastAPI, HTTPException, Pydantic models
- Create APIRouter instance
- Implement async POST endpoint at `/setup`

### 2. Endpoint Implementation
```python
@router.post("/setup", response_model=SetupResponse)
async def configure_proxy_mappings(request: SetupRequest) -> SetupResponse:
```

**Functionality**:
- Accept SetupRequest with path prefix to URL mappings
- Validate all URLs are valid HTTP/HTTPS format
- Clear existing proxy configurations (fresh setup each call)
- Store new mappings using storage module functions
- Return SetupResponse confirming configured mappings

### 3. Request Processing
- Extract mappings from SetupRequest
- Validate each target URL format (HTTP/HTTPS only)
- Handle duplicate prefixes (last one wins)
- Store mappings using `add_proxy_config()` from storage module

### 4. Error Handling
- **400 Bad Request**: Invalid URL format, malformed JSON, invalid path prefixes
- **500 Internal Server Error**: Storage failures, unexpected errors
- Use FastAPI's HTTPException for proper status codes

### 5. Integration with Router
Modify `src/app/api/router.py` to include the new setup router:
- Import proxy_setup module
- Add router to api_router with proper prefix

## Technical Approach

### Implementation Steps
1. Create `proxy_setup.py` following health_check.py structure
2. Import storage functions and Pydantic models from previous task
3. Implement setup endpoint with proper async handling
4. Add input validation and error handling
5. Update main router to include setup endpoints
6. Write unit tests for endpoint functionality

### Example Request/Response
```json
# Request
POST /api/setup
{
  "mappings": {
    "/v1/users": "https://api.example.com",
    "/v2/orders": "https://orders.service.com"
  }
}

# Response  
{
  "success": true,
  "configured_mappings": {
    "/v1/users": "https://api.example.com", 
    "/v2/orders": "https://orders.service.com"
  },
  "message": "Configured 2 proxy mappings"
}
```

### Dependencies
- Use existing FastAPI, HTTPException from the project
- Import storage functions from core/storage.py (previous task)
- Import Pydantic models from api/models/proxy_models.py (previous task)
- Follow async patterns from existing health_check.py

## Acceptance Criteria

### Functional Requirements
- POST /api/setup accepts valid JSON with path/URL mappings
- Endpoint validates URL format (HTTP/HTTPS scheme only)
- Successfully stores mappings in memory storage
- Returns confirmation with configured mappings
- Clears previous configurations on each setup call
- Handles multiple mappings in single request

### API Behavior
- Returns 200 status for successful configuration
- Returns 400 for invalid URLs or malformed requests
- Returns 500 for internal storage failures
- Response matches SetupResponse model format
- Content-Type: application/json for all responses

### Integration
- Endpoint accessible at `/api/setup` (with existing `/api` prefix)
- Router properly integrated with main API router
- Follows existing FastAPI patterns and error handling

### Code Quality
- Async endpoint handler with proper type hints
- Error handling with appropriate HTTP status codes
- Unit tests cover valid requests, invalid URLs, error scenarios
- Code follows project style guidelines and passes quality checks
- Proper logging using existing logger patterns

## Testing Requirements
Write unit tests covering:
- Valid setup requests with single and multiple mappings
- Invalid URL formats (non-HTTP/HTTPS schemes)
- Malformed JSON and missing required fields
- Empty mappings and edge cases
- Error response format and status codes
- Integration with storage module functions

## Out of Scope
- Network reachability testing of target URLs (proxy will surface upstream errors)
- Proxy forwarding logic (handled by separate task)
- Transaction capturing (handled by separate task)
- Persistent storage or configuration files
- Authentication or authorization for setup endpoint