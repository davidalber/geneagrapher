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
image-names = bunder chioniadis curry ryff-zwinger zwinger
image-targets = $(addsuffix -geneagraph.png, $(addprefix images/, $(image-names)))
images: $(image-targets)

bunder.dot: ids = 15648:d
chioniadis.dot: ids = 201288:a
curry.dot: ids = 7398:d
ryff-zwinger.dot: ids = 125148:a 130248:a
zwinger.dot: ids = 125148:a

$(image-targets): images/%-geneagraph.png: %.png
	optipng -o5 $? -clobber -out $@
%.png: %.dot
	dot -Tpng -Gdpi=150 $? > $@
%.dot:
	poetry run python -m geneagrapher.geneagrapher $(ids) | sed s/‐/-/g > $@

clean-images:
	rm -rf $(addsuffix .dot, $(image-names)) $(addsuffix .png, $(image-names)) images/*-geneagraph.png.bak

all:

clean:
	rm -rf dist
