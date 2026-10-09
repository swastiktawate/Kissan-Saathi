import os
import duckdb
import pytest
from backend.app.config import settings

def test_db_initialization():
    # Use in-memory for testing or a test db
    test_db = "data/test.duckdb"
    if os.path.exists(test_db):
        os.remove(test_db)
        
    old_path = settings.DUCKDB_PATH
    settings.DUCKDB_PATH = test_db
    
    try:
        from backend.scripts.init_db import init_db
        init_db()
        
        conn = duckdb.connect(test_db)
        mandis = conn.execute("SELECT count(*) FROM mandis").fetchone()[0]
        assert mandis >= 5
        
        crops = conn.execute("SELECT count(*) FROM crops").fetchone()[0]
        assert crops == 4
        
        cost_params = conn.execute("SELECT count(*) FROM cost_params WHERE assumption = true").fetchone()[0]
        assert cost_params == 4
        
        # Test idempotency
        init_db()
        mandis2 = conn.execute("SELECT count(*) FROM mandis").fetchone()[0]
        assert mandis == mandis2
        
        conn.close()
    finally:
        settings.DUCKDB_PATH = old_path
        if os.path.exists(test_db):
            os.remove(test_db)
