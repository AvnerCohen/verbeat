.PHONY: test clean install lint format help build publish update-version

# Default target
help:
	@echo "Available targets:"
	@echo "  test     - Run all tests"
	@echo "  clean    - Remove build artifacts"
	@echo "  install  - Install in development mode"
	@echo "  lint     - Run linting"
	@echo "  format   - Format code"
	@echo "  build    - Build package for distribution"
	@echo "  publish  - Build and publish to PyPI (requires twine)"
	@echo "  update-version - Update package version to match VerBeat"

# Run all tests
test:
	@echo "Running VerBeat Python implementation tests..."
	@python test_verbeat.py
	@python test_git_edge_cases.py

# Clean up cache files
clean:
	@echo "Cleaning Python build artifacts..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Install dependencies (none required for basic functionality)
install:
	@echo "Installing VerBeat in development mode..."
	@uv pip install -e .

# Lint code (requires flake8)
lint:
	@echo "Linting code..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run flake8 verbeat.py test_verbeat.py test_git_edge_cases.py; \
	else \
		echo "uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi

# Format code (requires black)
format:
	@echo "Formatting code..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run black verbeat.py test_verbeat.py test_git_edge_cases.py; \
	else \
		echo "uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi

update-version:
	@echo "Updating package version to match VerBeat..."
	@python -c "import sys; sys.path.insert(0, '../..'); from verbeat import get_version; version = get_version('../..'); print(f'Current VerBeat version: {version}'); print('Package version will be updated automatically during build')"

build: update-version
	@echo "Building Python package..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run python -m build; \
	else \
		echo "uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi

publish: build
	@echo "Publishing to PyPI..."
	@if command -v uv >/dev/null 2>&1; then \
		uv run twine upload dist/*; \
	else \
		echo "uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi 