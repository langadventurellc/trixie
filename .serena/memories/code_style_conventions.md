# Code Style and Conventions

## Formatting and Linting Rules
- **Line Length**: 100 characters (black, isort, flake8)
- **Code Formatter**: black with trailing commas
- **Import Sorting**: isort with multi-line output mode 3
- **Linting**: flake8 with specific ignores: E203, W503, E226

## Python Standards
- **Python Version**: 3.12+ required
- **Type Hints**: Required (pyright enforced, no `any` types allowed)
- **Async/Await**: FastAPI async patterns

## Architecture Rules (from CLAUDE.md)
- **File Size**: ≤ 400 logical lines of code
- **No "util" dumping grounds**: Avoid shared kitchen-sink modules
- **No hard-coded secrets**: Use environment variables/settings
- **No dead code**: Remove deprecated code immediately
- **Breaking changes encouraged**: No backwards compatibility needed

## FastAPI Patterns
- Router-based organization (`APIRouter`)
- Dependency injection for shared logic
- Pydantic models for request/response validation
- Async endpoint handlers

## Project Structure
```
src/
├── app/
│   ├── __init__.py
│   ├── main.py (FastAPI app creation)
│   ├── api/
│   │   ├── router.py (main API router)
│   │   └── endpoints/ (individual endpoint modules)
│   └── app_prestart.py
```

## Testing
- Unit tests with pytest
- No integration or performance tests (forbidden)
- Test fixtures should be focused and minimal