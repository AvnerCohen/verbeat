.PHONY: test clean install lint format help

# Default target
help:
	@echo "Available targets:"
	@echo "  test     - Run all tests (basic + Git edge cases)"
	@echo "  clean    - Remove Python cache files"
	@echo "  install  - Install dependencies (none required for basic functionality)"
	@echo "  lint     - Run linting (requires flake8)"
	@echo "  format   - Format code (requires black)"

# Run all tests
test:
	@echo "Running VerBeat Python implementation tests..."
	@python3 test_verbeat.py
	@echo ""
	@echo "Running Git edge case tests..."
	@python3 test_git_edge_cases.py

# Clean up cache files
clean:
	@echo "Cleaning Python cache files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Install dependencies (none required for basic functionality)
install:
	@echo "No external dependencies required for basic VerBeat functionality"
	@echo "Optional: pip install flake8 black for development tools"

# Lint code (requires flake8)
lint:
	@echo "Linting code..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 verbeat.py test_verbeat.py test_git_edge_cases.py; \
	else \
		echo "flake8 not found. Install with: pip install flake8"; \
	fi

# Format code (requires black)
format:
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black verbeat.py test_verbeat.py test_git_edge_cases.py; \
	else \
		echo "black not found. Install with: pip install black"; \
	fi 