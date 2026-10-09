.PHONY: setup seed run-api run-web test lint

VENV_BIN := $(if $(OS),venv/Scripts,venv/bin)
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
UVICORN := $(VENV_BIN)/uvicorn
PYTEST := $(VENV_BIN)/pytest

setup:
	py -3.11 -m venv venv
	$(PIP) install -r backend/requirements.txt

seed:
	$(PYTHON) backend/scripts/init_db.py

run-api:
	$(UVICORN) backend.app.main:app --reload

run-web:
	cd frontend && npm run dev

test:
	$(PYTEST) backend/tests/

lint:
	@echo "Linting (to be implemented)"
