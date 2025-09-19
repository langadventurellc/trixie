#!/bin/bash

# Pre-tool-task hook for preventing problematic bash commands
# Maps regex patterns to error messages and blocks execution

# Read the hook input from stdin
HOOK_INPUT=$(cat)

# Extract tool name and command from the JSON
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // empty')
COMMAND=$(echo "$HOOK_INPUT" | jq -r '.tool_input.command // empty')

# Only process Bash tool calls
if [[ "$TOOL_NAME" != "Bash" ]] || [[ -z "$COMMAND" ]]; then
    # Allow execution for non-Bash tools or missing commands
    exit 0
fi

# Define regex patterns and their corresponding error messages
# Format: "regex_pattern|error_message"
declare -a PATTERN_MAP=(
    "echo \"\" >> |Use 'uv run poe format' to add a new line at the end of a file instead of appending empty lines."
    # Add more patterns here as needed:
    # "npm run.*--.*|Use pnpm instead of npm for this monorepo."
    # "cd.*&&.*|Avoid chaining commands with cd. Use absolute paths instead."
)

# Check each pattern against the command
for pattern_entry in "${PATTERN_MAP[@]}"; do
    # Split on the first pipe character
    pattern="${pattern_entry%%|*}"
    message="${pattern_entry#*|}"
    
    # Check if command matches the regex pattern
    if [[ $COMMAND =~ $pattern ]]; then
        # Output error message to stderr and exit with code 2 to block execution
        echo "Error: $message" >&2
        echo "Blocked command: $COMMAND" >&2
        exit 2
    fi
done

# If no patterns matched, allow the tool to execute
exit 0