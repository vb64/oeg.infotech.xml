.PHONY: all setup tests dist
# make tests >debug.log 2>&1

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = oeg_infotech
TESTS = tests
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
LINT = $(PYTHON) -m pylint
LINT3 = $(LINT) --init-hook="sys.path.insert(0, './')"

all: tests

test:
	$(PTEST) -s $(TESTS)/test/$(T)

tests: pep257 flake8 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

tests3: pep257 flake8 lint3
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

flake8:
	$(PYTHON) -m flake8 --max-line-length=120 $(TESTS)
	$(PYTHON) -m flake8 --max-line-length=120 $(SOURCE)

lint:
	$(LINT) $(TESTS)/test
	$(LINT) $(SOURCE)

lint3:
	$(LINT3) $(TESTS)/test
	$(LINT3) $(SOURCE)

pep257:
	$(PYTHON) -m pep257 $(SOURCE)

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup3: setup_python3 setup_pip

setup_pip:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r tests/requirements.txt
	$(PYTHON) -m pip install -r deploy.txt

setup_python:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv ./venv

setup_python3:
	$(PYTHON_BIN) -m venv ./venv
