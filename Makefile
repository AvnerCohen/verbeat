.PHONY: test clean help

help:
	@echo "Available targets:"
	@echo "  test     - Run all implementation tests"
	@echo "  clean    - Clean all implementation files"

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