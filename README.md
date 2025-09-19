# Trixie - Reverse Proxy API for Testing

A Docker-based reverse proxy API that captures HTTP requests and responses for end-to-end test assertions. Trixie allows you to configure URL mappings, forward requests to target services, and query transaction history for testing validation.

## Quick Start

### Docker Compose (Recommended)

```bash
# Start the API
docker-compose up -d

# The API will be available at http://localhost:17080
```

### Docker Run

```bash
# Build the image
docker build -t trixie .

# Run the container
docker run -p 17080:80 trixie
```

## API Overview

The API provides three main endpoints:

- **Setup**: Configure proxy path mappings
- **Proxy**: Forward requests and capture transactions
- **Query**: Retrieve captured transaction history

### Base URL
When running via Docker: `http://localhost:17080`

## API Endpoints

### 1. Health Check
```http
GET /api/health
```

Returns API health status.

**Response:**
```json
{
  "status": "ok"
}
```

### 2. Configure Proxy Mappings
```http
POST /api/setup
Content-Type: application/json

{
  "mappings": {
    "/v1/users": "https://api.example.com",
    "/v2/orders": "https://orders.api.com"
  }
}
```

Configure path prefixes to target URL mappings. Each request clears existing configurations.

**Response:**
```json
{
  "success": true,
  "configured_mappings": {
    "/v1/users": "https://api.example.com",
    "/v2/orders": "https://orders.api.com"
  },
  "message": "Configured 2 proxy mappings"
}
```

### 3. Proxy Requests
```http
GET|POST|PUT|DELETE /proxy/{path}
```

Forward requests to configured target URLs based on longest-prefix matching.

**Examples:**
- `GET /proxy/v1/users/123` → forwards to `https://api.example.com/v1/users/123`
- `POST /proxy/v2/orders` → forwards to `https://orders.api.com/v2/orders`

All HTTP methods, headers, query parameters, and request bodies are forwarded exactly as received.

### 4. Query Transactions
```http
GET /api/transactions
GET /api/transactions?count=10
```

Retrieve captured transaction history in reverse chronological order (newest first).

**Response:**
```json
{
  "transactions": [
    {
      "id": "uuid",
      "timestamp": "2025-01-15T10:30:00Z",
      "request": {
        "method": "GET",
        "url": "https://api.example.com/v1/users/123",
        "headers": {...},
        "query_params": {...},
        "body": ""
      },
      "response": {
        "status_code": 200,
        "headers": {...},
        "body": "{...}"
      },
      "proxy_mapping_used": "/v1/users -> https://api.example.com"
    }
  ],
  "count": 1
}
```

## Usage Workflow

### 1. Setup Proxy Configuration
Configure which URL prefixes should be forwarded to which target services:

```bash
curl -X POST http://localhost:17080/api/setup \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "/api/users": "https://users.service.com",
      "/api/orders": "https://orders.service.com"
    }
  }'
```

### 2. Make Requests Through Proxy
Route your test requests through the proxy to capture them:

```bash
# This request gets forwarded to https://users.service.com/api/users/123
curl http://localhost:17080/proxy/api/users/123

# This request gets forwarded to https://orders.service.com/api/orders
curl -X POST http://localhost:17080/proxy/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": "abc123", "quantity": 2}'
```

### 3. Query Captured Data
Retrieve transaction history for test assertions:

```bash
# Get all transactions
curl http://localhost:17080/api/transactions

# Get last 5 transactions
curl http://localhost:17080/api/transactions?count=5
```

## Testing with HTTP Files

The repository includes example HTTP request files in `/http_requests/` for testing:

- `health_check.http` - Health check
- `proxy_setup.http` - Configure mappings
- `get_all_transactions.http` - Query all transactions
- `proxy_*.http` - Various proxy request examples

Use these with HTTP clients like REST Client (VS Code) or Postman.

## Development

### Local Development
```bash
# Install dependencies
uv sync

# Run locally (development mode)
uv run poe dev-start

# Run quality checks
uv run poe quality

# Run tests
uv run pytest -q
```

### Docker Development
```bash
# Build and run with docker-compose
docker-compose up --build

# View logs
docker-compose logs -f trixie_api
```

## Technical Details

- **Framework**: FastAPI with Python 3.12+
- **HTTP Client**: httpx for request forwarding
- **Storage**: In-memory (no persistence)
- **Port**: Container exposes port 80, mapped to 17080 on host
- **Logging**: Structured logging with pyla-logger

## Docker Image

The official Docker image is available at:
```
ghcr.io/langadventurellc/docker-trixie
```

**Labels:**
- `org.opencontainers.image.source = "https://github.com/langadventurellc/docker-trixie"`

## Error Handling

- **404**: No proxy configuration matches the requested path
- **502**: Target server unreachable
- **504**: Timeout connecting to target server
- **500**: Internal proxy errors
