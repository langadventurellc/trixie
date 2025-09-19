# Essential Development Commands

## Quality Assurance (Run after every change)
- `uv run poe quality` - Run complete quality checks (formatting, linting, type checking)
- `uv run pytest` - Run unit tests

## Individual Quality Checks
- `uv run poe black` or `uv run poe format` - Format code with black
- `uv run poe isort` - Sort imports
- `uv run poe lint` - Run flake8 linting
- `uv run poe type-check` - Run pyright type checking

## Development Server
- `uv run poe dev-start` - Start development server with hot reload (port 8000)
- `uv run poe dev-docker` - Start via Docker using scripts/docker_start.sh

## Docker
- Build and run via docker-compose.yml available in root

## Git and Utilities (Darwin/macOS)
- Standard Unix commands: `git`, `ls`, `cd`, `grep`, `find`
- Package management: `uv` commands for dependencies