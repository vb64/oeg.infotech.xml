.PHONY: all setup tests
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv\Scripts\python.exe
else
PYTHON = ./venv/bin/python
endif

SOURCE = oeg_infotech
TESTS = tests
COVERAGE = $(PYTHON) -m coverage

all: tests

test:
	$(PYTHON) $(TESTS)/run_tests.py test.$(T)

html:
	$(COVERAGE) html --skip-covered

coverage:
	$(COVERAGE) run $(TESTS)/run_tests.py

tests: flake8 lint coverage html
	$(COVERAGE) report --skip-covered

verbose:
	$(PYTHON) $(TESTS)/run_tests.py verbose

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(TESTS)
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(TESTS)/test
	$(PYTHON) -m pylint $(SOURCE)

setup: setup_python setup_pip

setup_pip:
	$(PYTHON) -m pip install -r tests/requirements.txt

setup_python:
	$(PYTHON_BIN) -m virtualenv ./venv
