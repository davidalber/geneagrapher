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

# Images (for the README)
image-targets = images/chioniadis-geneagraph.png images/curry-geneagraph.png images/ryff-zwinger-geneagraph.png images/zwinger-geneagraph.png
images: $(image-targets)

chioniadis.dot: ids = 201288
curry.dot: ids = 7398:d
ryff-zwinger.dot: ids = 125148 130248
zwinger.dot: ids = 125148

$(image-targets): images/%-geneagraph.png: %.png
	optipng -o5 $? -clobber -out $@
%.png: %.dot
	dot -Tpng -Gdpi=150 $? > $@
%.dot:
	poetry run python -m geneagrapher.geneagrapher $(ids) | sed s/‐/-/g > $@

clean-images:
	rm -rf chioniadis.dot chioniadis.png curry.dot curry.png ryff-zwinger.dot ryff-zwinger.png zwinger.dot zwinger.png images/*-geneagraph.png.bak

all:

clean:
	rm -rf dist
