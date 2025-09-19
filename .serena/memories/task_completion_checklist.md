# Task Completion Checklist

## REQUIRED After Every Code Change

1. **Quality Checks** (MANDATORY)
   ```bash
   uv run poe quality
   ```
   This runs: black formatting, isort import sorting, flake8 linting, pyright type checking

2. **Unit Tests** (MANDATORY)
   ```bash
   uv run pytest
   ```

3. **Fix All Issues Immediately**
   - Address any linting errors
   - Fix type checking failures
   - Ensure all tests pass

## Pre-commit Hooks
The project has pre-commit configured (.pre-commit-config.yaml), which should catch issues before commit.

## Quality Standards
- Zero linting errors
- Zero type checking errors
- All tests passing
- Code formatted consistently

## Development Workflow
1. Make code changes
2. Run `uv run poe quality` 
3. Fix any issues found
4. Run `uv run pytest`
5. Fix any test failures
6. Commit changes

## Notes
- Quality checks are non-negotiable
- Breaking old code is preferred over keeping deprecated code
- No backwards compatibility requirements (greenfield project)