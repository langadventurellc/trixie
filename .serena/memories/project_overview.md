# Trixie Project Overview

## Purpose
Trixie is a Docker image for a testing proxy that captures requests and responses and stores them to be queried for test assertions. The project is designed to facilitate end-to-end testing by acting as a reverse proxy that can intercept, forward, and record HTTP transactions.

## Current State
The project is in early development with a basic FastAPI application structure in place. Currently only has a health check endpoint implemented.

## Tech Stack
- **Python**: 3.12+ (primary language)
- **Package Manager**: uv (modern Python package manager)
- **Web Framework**: FastAPI (async web framework)
- **HTTP Client**: httpx (for making outbound requests)
- **Container**: Docker (for deployment)
- **Data Validation**: Pydantic v2
- **Logging**: pyla-logger
- **ASGI Server**: uvicorn

## Key Dependencies
- FastAPI 0.116.1+ (web framework)
- httpx 0.28.0+ (HTTP client for proxy functionality)
- Pydantic 2.11.7+ (data validation)
- uvicorn 0.35.0+ (ASGI server)

## Development Dependencies
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- pyright (type checking)
- pre-commit (git hooks)
- poethepoet (task runner)