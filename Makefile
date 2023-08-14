.PHONY: *
run:
	python3 src/main.py

flake8:
	python3 -m flake8 src/
mypy:
	python3 -m mypy src/
lint: flake8 mypy

test:
	python3 -m pytest -q test/

all: lint test run