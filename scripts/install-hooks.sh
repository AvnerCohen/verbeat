#!/bin/bash

# Install VerBeat Git hooks

HOOKS_DIR="hooks"
GIT_HOOKS_DIR=".git/hooks"

if [ ! -d "$GIT_HOOKS_DIR" ]; then
    echo "Error: Not in a Git repository"
    exit 1
fi

if [ ! -d "$HOOKS_DIR" ]; then
    echo "Error: hooks directory not found"
    exit 1
fi

echo "Installing VerBeat Git hooks..."

# Symlink pre-commit hook
if [ -f "$HOOKS_DIR/pre-commit" ]; then
    ln -sf "../../$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"
    echo "✓ Symlinked pre-commit hook"
else
    echo "✗ pre-commit hook not found"
fi

echo "VerBeat Git hooks installed successfully!"
echo ""
echo "The pre-commit hook will automatically:"
echo "- Update version.json with current VerBeat version"
echo "- Add version.json to your commits"
echo ""
echo "To uninstall, run: rm .git/hooks/pre-commit" 