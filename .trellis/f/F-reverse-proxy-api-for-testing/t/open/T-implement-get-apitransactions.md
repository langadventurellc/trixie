---
id: T-implement-get-apitransactions
title: Implement GET /api/transactions endpoint with query support
status: open
priority: medium
parent: F-reverse-proxy-api-for-testing
prerequisites:
  - T-create-data-models-and-in
affectedFiles: {}
log: []
schema: v1.0
childrenIds: []
created: 2025-09-19T11:56:08.768Z
updated: 2025-09-19T11:56:08.768Z
---

# Implement GET /api/transactions Endpoint with Query Support

## Context
This task implements the transactions query endpoint that allows test fixtures to retrieve captured HTTP transaction history for assertions. The endpoint returns transactions in reverse chronological order with optional count limiting.

**Related Feature**: F-reverse-proxy-api-for-testing - Reverse Proxy API for Testing
**Prerequisites**: T-create-data-models-and-in (data models and storage)

## Specific Implementation Requirements

### 1. Create Transactions Endpoint Module
Create `src/app/api/endpoints/transactions.py` following existing patterns:

- Import FastAPI components: APIRouter, Query, HTTPException
- Import Pydantic models for response formatting
- Import storage functions for transaction retrieval
- Create APIRouter instance

### 2. Endpoint Implementation
```python
@router.get("/transactions", response_model=TransactionsResponse)
async def get_transactions(count: Optional[int] = Query(None, ge=1, description="Limit number of transactions returned")) -> TransactionsResponse:
```

**Core Functionality**:
- Retrieve transactions from storage in reverse chronological order (newest first)
- Apply count limit if specified
- Convert internal storage format to API response format
- Return structured response with transaction data

### 3. Query Parameter Handling
- **count**: Optional integer parameter
  - Default: return all transactions if not specified
  - Validation: must be positive integer (≥ 1)
  - Behavior: limit results to most recent N transactions

### 4. Data Transformation
Transform internal storage format to API response:
- Convert stored transaction dicts to TransactionRecord Pydantic models
- Ensure proper JSON serialization of datetime fields
- Maintain transaction ordering (newest first)
- Handle empty transaction history gracefully

### 5. Response Format
Return TransactionsResponse containing:
- `transactions`: List of TransactionRecord objects
- `count`: Actual number of transactions returned
- Proper HTTP 200 status with JSON content type

### 6. Error Handling
- **400 Bad Request**: Invalid count parameter (negative or zero)
- **500 Internal Server Error**: Storage retrieval failures
- Handle empty transaction history as successful empty response

### 7. Integration with Router
Update `src/app/api/router.py` to include transactions router

## Technical Approach

### Implementation Steps
1. Create transactions.py following health_check.py structure
2. Implement GET endpoint with Query parameter validation
3. Add data transformation from storage format to Pydantic models
4. Handle optional count parameter with proper defaults
5. Add error handling for invalid parameters
6. Update main router to include transactions endpoints
7. Write unit tests for various query scenarios

### Data Flow
1. Receive GET request with optional count parameter
2. Validate count parameter if provided
3. Call `get_transactions(count)` from storage module
4. Transform dict data to TransactionRecord models
5. Create TransactionsResponse with results
6. Return JSON response

### Dependencies
- Use existing FastAPI Query parameter validation
- Import storage functions from core/storage.py
- Import Pydantic models from api/models/proxy_models.py
- Follow async patterns from existing endpoints

## Acceptance Criteria

### Functional Requirements
- GET /api/transactions returns all transactions when count not specified
- Count parameter limits results to N most recent transactions
- Transactions returned in reverse chronological order (newest first)
- Empty transaction history returns empty array with 200 status
- Response matches TransactionsResponse model structure

### Query Parameter Behavior
- `/api/transactions` → returns all transactions
- `/api/transactions?count=5` → returns 5 most recent transactions
- `/api/transactions?count=1` → returns single most recent transaction
- `/api/transactions?count=0` → returns 400 error
- `/api/transactions?count=-1` → returns 400 error

### Response Format
```json
{
  "transactions": [
    {
      "id": "uuid-string",
      "timestamp": "2024-01-01T12:00:00Z",
      "request": {
        "method": "GET",
        "url": "/v1/users/123",
        "headers": {...},
        "body": "",
        "query_params": {...}
      },
      "response": {
        "status_code": 200,
        "headers": {...},
        "body": "{...}"
      },
      "proxy_mapping_used": "/v1/users"
    }
  ],
  "count": 1
}
```

### API Behavior
- Returns 200 status for successful queries
- Returns 400 for invalid count parameters with error details
- Content-Type: application/json for all responses
- Handles large transaction histories efficiently
- Maintains data integrity during concurrent access

### Integration
- Endpoint accessible at `/api/transactions` (with existing `/api` prefix)
- Properly integrated with main API router
- Follows existing FastAPI patterns and conventions

### Code Quality
- Async endpoint handler with proper type hints
- Query parameter validation using FastAPI Query
- Error handling with appropriate HTTP status codes
- Unit tests cover various query scenarios and edge cases
- Code follows project style guidelines and passes quality checks

## Testing Requirements
Write unit tests covering:
- Query all transactions (no count parameter)
- Query with valid count parameter (various values)
- Query with invalid count parameters (zero, negative, non-integer)
- Empty transaction history response
- Large transaction history with count limiting
- Data transformation accuracy and datetime serialization
- Error response format and status codes

## Out of Scope
- Real-time transaction filtering or search capabilities
- Pagination beyond simple count limiting
- Transaction data modification or deletion endpoints
- Advanced query parameters (date ranges, method filtering)
- Performance optimization for very large transaction histories