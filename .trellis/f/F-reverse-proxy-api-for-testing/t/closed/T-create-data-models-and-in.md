---
id: T-create-data-models-and-in
title: Create data models and in-memory storage for proxy system
status: done
priority: high
parent: F-reverse-proxy-api-for-testing
prerequisites: []
affectedFiles:
  pyproject.toml: Added pytest>=8.0.0 to dev dependencies for testing framework
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
log:
  - Successfully implemented data models and in-memory storage for the reverse
    proxy system. Created four Pydantic models (SetupRequest, SetupResponse,
    TransactionRecord, TransactionsResponse) with proper validation for URL
    formats and path prefixes. Implemented comprehensive storage functions with
    prefix matching logic that correctly handles longest-match-first routing.
    Added pytest dependency and created extensive test coverage (20 tests)
    covering model validation, storage operations, and edge cases. All quality
    checks pass including formatting, linting, and type checking.
schema: v1.0
childrenIds: []
created: 2025-09-19T11:54:35.669Z
updated: 2025-09-19T11:54:35.669Z
---

# Create Data Models and In-Memory Storage for Proxy System

## Context
This task implements the foundational data structures for the reverse proxy system. The implementation follows a mixed approach: Pydantic models for API request/response validation and simple Python data structures for internal storage.

**Related Feature**: F-reverse-proxy-api-for-testing - Reverse Proxy API for Testing

## Specific Implementation Requirements

### 1. Create Pydantic Models
Create `src/app/api/models/proxy_models.py` with the following models:

- **SetupRequest**: Validate POST /api/setup request body
  - `mappings: Dict[str, str]` - path prefix to target URL mappings
  - Validate URLs are valid HTTP/HTTPS endpoints
  - Validate path prefixes start with "/"

- **SetupResponse**: Response confirmation for setup
  - `success: bool` 
  - `configured_mappings: Dict[str, str]`
  - `message: str`

- **TransactionRecord**: For API response format
  - `id: str` - unique transaction identifier
  - `timestamp: datetime`
  - `request: Dict` - method, url, headers, body, query_params
  - `response: Dict` - status_code, headers, body
  - `proxy_mapping_used: str` - which prefix matched

- **TransactionsResponse**: For GET /api/transactions response
  - `transactions: List[TransactionRecord]`
  - `count: int`

### 2. Create In-Memory Storage Module
Create `src/app/core/storage.py` with simple data structures:

- `proxy_configurations: Dict[str, str] = {}` - path prefix -> target URL
- `transaction_history: List[Dict] = []` - simple dict storage for internal use
- Helper functions:
  - `add_proxy_config(prefix: str, target_url: str) -> None`
  - `get_proxy_config(path: str) -> Optional[str]` - find matching prefix
  - `clear_proxy_configs() -> None`
  - `add_transaction(transaction_data: Dict) -> None`
  - `get_transactions(count: Optional[int] = None) -> List[Dict]`

### 3. Implement Prefix Matching Logic
In the storage module, implement the core prefix matching algorithm:
- Sort configured prefixes by length (longest first) for accurate matching
- Return the target URL for the longest matching prefix
- Handle case where no prefix matches

## Technical Approach

### File Structure
```
src/app/
├── api/models/proxy_models.py (new)
└── core/storage.py (new)
```

### Implementation Steps
1. Create the models directory if it doesn't exist
2. Implement Pydantic models with proper validation
3. Create storage module with simple data structures
4. Implement prefix matching algorithm with proper sorting
5. Add basic error handling for invalid configurations
6. Write unit tests for models validation and storage operations

### Dependencies
- Use existing `pydantic` dependency for model validation
- Use Python standard library for data structures
- Follow existing project patterns from `src/app/api/endpoints/health_check.py`

## Acceptance Criteria

### Functional Requirements
- SetupRequest model validates JSON input with proper URL and path validation
- TransactionRecord model structures transaction data correctly
- Storage functions correctly add/retrieve proxy configurations
- Prefix matching returns longest matching prefix for any given path
- Example: `/v1/users` prefix matches `/v1/users/123` and `/v1/users/456/profile`
- Transaction storage maintains chronological order

### Code Quality
- All models have proper type hints and validation
- Storage functions handle edge cases (empty configs, invalid paths)
- Unit tests cover model validation and storage operations
- Code follows project style: 100-character lines, async patterns where applicable
- Pass `uv run poe quality` checks

### Security Considerations
- URL validation prevents basic injection attacks
- Path prefix validation ensures proper format
- No sensitive data logging in storage functions

## Testing Requirements
Write unit tests in appropriate test files covering:
- SetupRequest validation with valid/invalid URLs and paths
- TransactionRecord serialization/deserialization
- Storage functions: add, retrieve, clear operations
- Prefix matching algorithm with various path combinations
- Edge cases: empty storage, no matching prefix, malformed data

## Out of Scope
- API endpoint implementation (handled by other tasks)
- HTTP client functionality (handled by other tasks)  
- Persistent storage or database integration
- Advanced security features beyond basic validation