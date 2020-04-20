# Python poetry Makefile
PACKAGE_FOLDER=business
TEST_FOLDER=test

build:
	poetry build

clean:
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

install:
	poetry install --no-root

test: install lint
	poetry run python -m pytest --cov=./$(PACKAGE_FOLDER) $(TEST_FOLDER) --cov-report=html
	poetry run flake8 $(PACKAGE_FOLDER) $(TEST_FOLDER) --statistics
	poetry run mypy $(PACKAGE_FOLDER)

lint: install
	poetry run black $(PACKAGE_FOLDER) $(TEST_FOLDER)
	poetry run isort --recursive $(PACKAGE_FOLDER) $(TEST_FOLDER)

tox:
	poetry run tox

release: clean test tox
	# 1. create API token at https://pypi.org/manage/account/token/
	# 2. configure poetry credentials: https://python-poetry.org/docs/repositories/#configuring-credentials
	poetry publish --build

.PHONY: build clean install test lint tox release
