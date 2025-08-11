.PHONY: help publish-nodejs publish-python update-version-nodejs update-version-python clean

help:
	@echo "VerBeat Implementations Publishing"
	@echo ""
	@echo "Available targets:"
	@echo "  help              - Show this help message"
	@echo "  update-version-nodejs  - Update Node.js package.json version"
	@echo "  update-version-python  - Update Python setup.py/pyproject.toml version"
	@echo "  publish-nodejs    - Publish Node.js package to NPM"
	@echo "  publish-python    - Publish Python package to PyPI"
	@echo "  clean             - Clean all implementation build artifacts"

update-version-nodejs:
	@echo "Updating Node.js implementation version..."
	@node scripts/update-version.js nodejs

update-version-python:
	@echo "Python implementation uses dynamic versioning - no update needed"
	@echo "Version is automatically determined from verbeat._get_verbeat_version"

publish-nodejs: update-version-nodejs
	@echo "Publishing Node.js package to NPM..."
	@cd nodejs && yarn test
	@cd nodejs && yarn publish
	@echo "Resetting Node.js version to placeholder..."
	@cd nodejs && sed -i '' 's/"version": "[^"]*"/"version": "CURRENT_VERSION_PLACEHOLDER"/' package.json

publish-python: update-version-python
	@echo "Publishing Python package to PyPI..."
	@cd python && uv run python -m pytest tests/
	@cd python && uv run python -m build
	@cd python && uv run python -m twine upload dist/*

clean:
	@echo "Cleaning implementation build artifacts..."
	@cd nodejs && make clean
	@cd python && make clean
	@find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
