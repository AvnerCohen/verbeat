.PHONY: test clean help publish-nodejs publish-python

help:
	@echo "Available targets:"
	@echo "  test     - Run all implementation tests"
	@echo "  clean    - Clean all implementation files"
	@echo "  publish-nodejs - Publish Node.js package to NPM"
	@echo "  publish-python - Publish Python package to PyPI"

test:
	@echo "Running all VerBeat implementation tests..."
	@echo ""
	@echo "=== Python Implementation ==="
	@cd implementations/python && make test
	@echo ""
	@echo "=== Node.js Implementation ==="
	@cd implementations/nodejs && make test
	@echo ""
	@echo "🎉 All implementation tests passed!"

clean:
	@echo "Cleaning all implementations..."
	@cd implementations/python && make clean
	@cd implementations/nodejs && make clean

publish-nodejs:
	@echo "Publishing Node.js package to NPM..."
	@cd implementations && make publish-nodejs

publish-python:
	@echo "Publishing Python package to PyPI..."
	@cd implementations && make publish-python 