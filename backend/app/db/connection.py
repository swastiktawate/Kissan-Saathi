import duckdb
from backend.app.config import settings

def get_db():
    conn = duckdb.connect(settings.DUCKDB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def get_db_connection():
    return duckdb.connect(settings.DUCKDB_PATH)
