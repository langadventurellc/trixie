#!/bin/bash

# Pre-tool use hook for Trellis Complete Task
# Runs lint and test before completing tasks

echo "🔧 Running pre-completion checks for Trellis task..."

# Change to project root
cd "$(git rev-parse --show-toplevel)"

echo "📝 Running quality checks..."
if ! uv run poe quality; then
    echo "❌ Quality checks failed - fix issues before completing task" >&2
    exit 2
fi

echo "✅ Quality checks passed"
