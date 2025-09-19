# Instructions for working in the LLM Bridge Library

A Python API Docker image for a testing proxy that captures requests and responses and stores them to be queried for test assertions.

## Repository Structure

**Applications:**

- `src` - main API code

## Development

### Quality checks

**IMPORTANT** Run the following commands to ensure code quality after every change. Fix all issues as soon as possible.

- `uv run poe quality` - Run linting, formatting, and type checks
- `uv run pytest` - Run unit tests to ensure functionality

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
