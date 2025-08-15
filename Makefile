.PHONY: install lint format check clean run

# Source directory
SRC = src/torrentbd_api

# Install dependencies
install:
	-pip install uv || python -m pip install uv
	-uv --version || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv
	uv pip install .[dev]
	uv run pre-commit install

# Linting & formatting
lint:
	uv run ruff check $(SRC)

format:
	uv run black $(SRC)
	uv run isort $(SRC)

# Run all checks
check:
	uv run mypy $(SRC)
	uv run bandit -r $(SRC)
	uv run ruff check $(SRC)
	uv run pre-commit run --all-files

# Run API server
run:
	uv run python -m src.torrentbd_api.main

# Clean artifacts
clean:
	-uv run python -c "import shutil; shutil.rmtree('dist', ignore_errors=True)"
	-uv run python -c "import shutil; shutil.rmtree('build', ignore_errors=True)"
	-uv run python -c "import shutil; shutil.rmtree('src/tbd_api.egg-info', ignore_errors=True)"
	-uv run python -c "import shutil; shutil.rmtree('.pytest_cache', ignore_errors=True)"
	-uv run python -c "import shutil; shutil.rmtree('.mypy_cache', ignore_errors=True)"
	-uv run python -c "import shutil; shutil.rmtree('.ruff_cache', ignore_errors=True)"

# Default target
all: install check
