.PHONY: test clean install lint format help build publish update-version

help:
	@echo "Available targets:"
	@echo "  test     - Run all tests"
	@echo "  clean    - Remove node_modules and cache files"
	@echo "  install  - Install dependencies"
	@echo "  lint     - Run linting (requires eslint)"
	@echo "  format   - Format code (requires prettier)"
	@echo "  build    - Build package for distribution"
	@echo "  publish  - Build and publish to npm"
	@echo "  update-version - Update package version to match VerBeat"

test:
	@echo "Running VerBeat Node.js implementation tests..."
	@node tests/test_verbeat.js

clean:
	@echo "Cleaning Node.js files..."
	@rm -rf node_modules
	@rm -rf .nyc_output
	@rm -rf coverage
	@find . -name "*.log" -delete

install:
	@echo "Installing Node.js dependencies..."
	@npm install

lint:
	@echo "Linting code..."
	@if command -v npx >/dev/null 2>&1; then \
		npx eslint src/ tests/ bin/; \
	else \
		echo "npx not found. Install with: npm install -g npx"; \
	fi

format:
	@echo "Formatting code..."
	@if command -v npx >/dev/null 2>&1; then \
		npx prettier --write src/ tests/ bin/; \
	else \
		echo "npx not found. Install with: npm install -g npx"; \
	fi

update-version:
	@echo "Updating package version to match VerBeat..."
	@npm run update-version

build: update-version
	@echo "Building Node.js package..."
	@npm pack

publish: update-version
	@echo "Publishing to npm..."
	@npm publish 