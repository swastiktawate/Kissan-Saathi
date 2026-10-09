import os

dirs = [
    'backend/app/schemas', 'backend/app/db', 'backend/app/ingestion',
    'backend/app/cleaning', 'backend/app/services', 'backend/app/assistant',
    'backend/app/api', 'backend/scripts', 'backend/tests',
    'data/sample', 'data/raw', 'frontend', 'docs'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

with open('backend/requirements.txt', 'w') as f:
    f.write('''fastapi==0.111.0
uvicorn==0.30.1
pydantic==2.7.4
pydantic-settings==2.3.4
pandas==2.2.2
duckdb==1.0.0
httpx==0.27.0
numpy==1.26.4
scikit-learn==1.5.0
pytest==8.2.2
pytest-asyncio==0.23.7
python-dotenv==1.0.1
# lightgbm==4.4.0
''')

with open('backend/app/main.py', 'w') as f:
    f.write('''from fastapi import FastAPI

app = FastAPI(title="Kisan Saathi API", version="1.0.0")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
''')

with open('.gitignore', 'w') as f:
    f.write('''venv/
node_modules/
.env
data/raw/
*.duckdb
__pycache__/
dist/
.pytest_cache/
''')

with open('Makefile', 'w') as f:
    f.write('''.PHONY: setup seed run-api run-web test lint

VENV_BIN := $(if $(OS),venv/Scripts,venv/bin)
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
UVICORN := $(VENV_BIN)/uvicorn
PYTEST := $(VENV_BIN)/pytest

setup:
\tpython -m venv venv
\t$(PIP) install -r backend/requirements.txt

seed:
\t$(PYTHON) backend/scripts/init_db.py

run-api:
\t$(UVICORN) backend.app.main:app --reload

run-web:
\tcd frontend && npm run dev

test:
\t$(PYTEST) backend/tests/

lint:
\t@echo "Linting (to be implemented)"
''')

with open('README.md', 'w') as f:
    f.write('''# Kisan Saathi

Sahi Samay, Behtar Daam. (Right time, better price.)

## Status Vocabulary
- **Implemented (MVP)**: Real code, real logic, works end-to-end in the demo.
- **Simplified**: Real code but a reduced method.
- **Mocked**: Fixed or synthetic data/behaviour.
- **Future**: Not built in the hackathon. Listed for roadmap only.

## How to run
1. Run `make setup`
2. Run `make seed`
3. Run `make run-api`
4. Run `make run-web`

## Data Origin Honesty
Every number traceable to a source, a timestamp and an origin label.
Data origins: `live`, `cached`, `sample`, `synthetic`, `user_input`.
''')

for d in dirs:
    if d.startswith('backend/app') or d.startswith('backend/tests') or d.startswith('backend/scripts'):
        with open(f'{d}/__init__.py', 'w') as f:
            pass
with open('backend/app/__init__.py', 'w') as f: pass
with open('backend/__init__.py', 'w') as f: pass
