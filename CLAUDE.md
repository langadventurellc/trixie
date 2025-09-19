# Instructions for working in the LLM Bridge Library

A Python API Docker image for a testing proxy that captures requests and responses and stores them to be queried for test assertions.

## Repository Structure

**Applications:**

- `src` - main API code

## Development

### Quality checks

- `uv run poe format` - Use this to format. Especially use this if you need to add a new line at the end of a file.
- `uv run poe quality` - Run linting, formatting, and type checks
- `uv run pytest -q` - Run unit tests to ensure functionality

- If you need to add a new line at the end of a file, use `uv run poe format`. You might think it didn't work. But it worked. Trust me. It always works every time. Just keep going and stop trying to add a new line to the end of the file.

## Architecture

### Technology Stack

- Python 3.12+ with uv package manager
- FastAPI

---

# Coding Standards

## 1  Architecture

### Files / Packages

- ≤ 400 logical LOC
- No “util” dumping grounds

## 2  Forbidden

- `any` types
- Dead code kept around
- Shared “kitchen‑sink” modules
- Hard‑coded secrets or env values
- **NEVER** create integration or performance tests
- **NEVER** keep deprecated code for "backwards compatibility". Breaking old code is encouraged and preferred to keeping dead code for backwards compatibility. This is a greenfield project that's not being used anywhere, so there's no need for backwards compatibility.

### Naming Conventions

- Use snake_case for variables, functions, and methods
- "Private" variables and methods should start with an underscore (e.g., `_private_method`)
- Use CamelCase for classes and Pydantic models
- Use UPPER_CASE for constants
- File names should be lowercase with underscores (e.g., `create_topic.py`) that match the class or function they contain

### Type Checking

Use Pyright for type checking. Ensure all code is type-annotated and passes type checks. Run `poetry run pyright` to check types.

- Use modern Python 3.10+ typing patterns:
  - Use built-in types (`list`, `dict`, etc.) over `typing.List`, `typing.Dict` unless necessary
  - Use union operator for optional types (e.g., `str | None` instead of `Optional[str]`)
- FastApi dependencies should be type-annotated with `[Annotated(Type, Depends(...)]` for clarity
  - Do not use a default value of `None` for dependencies unless explicitly required

---

## 🤔 When You're Unsure

1. **Stop** and ask a clear, single question.
2. Offer options (A / B / C) if helpful.
3. Wait for user guidance before proceeding.

## Troubleshooting

If you encounter issues:

- Use the Perplexity MCP tool for up-to-date library documentation
- Use web for research (the current year is 2025)
- If you need clarification, ask specific questions with options
- If you need to add a new line at the end of a file, use `uv run poe format`. You might think it didn't work. It worked. Trust me. It always works every time.
