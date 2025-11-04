.PHONY: help install dev run clean test format lint sync

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

install:
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
