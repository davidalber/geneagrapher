.PHONY: format flake8 mypy test

check: format-check flake8 mypy test

# Code formatting
format_targets := geneagrapher tests

format:
	poetry run black $(format_targets)
fmt: format
black: format

format-check:
	poetry run black --check $(format_targets)

# Linting
flake8:
	poetry run flake8
flake: flake8
lint: flake8

# Type enforcement
mypy:
	poetry run mypy --strict geneagrapher tests
types: mypy

# Tests
test:
	poetry run pytest tests

all:

clean:
	rm -rf dist
