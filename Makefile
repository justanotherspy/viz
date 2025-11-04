.PHONY: help install dev run clean test format lint sync check-deps

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Install development dependencies"
	@echo "  make run        - Run the audio visualizer"
	@echo "  make clean      - Clean up cache and build files"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code with ruff"
	@echo "  make lint       - Lint code with ruff"
	@echo "  make sync       - Sync dependencies with uv"

check-deps:
	@echo "Checking system dependencies..."
	@if ! pkg-config --exists portaudio-2.0 2>/dev/null; then \
		echo ""; \
		echo "❌ PortAudio is not installed!"; \
		echo ""; \
		echo "PyAudio requires PortAudio to build. Please install it first:"; \
		echo ""; \
		echo "  brew install portaudio"; \
		echo ""; \
		echo "After installation, run 'make install' again."; \
		echo ""; \
		exit 1; \
	fi
	@echo "✓ PortAudio is installed"

install: check-deps
	uv sync

dev:
	uv sync --all-extras

run:
	uv run viz

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/

test:
	uv run pytest

format:
	uv run ruff format .

lint:
	uv run ruff check .

sync:
	uv sync
