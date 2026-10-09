from backend.app.db.connection import get_db_connection

class CropRepository:
    def get_all(self):
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM crops").fetchall()
        finally:
            conn.close()

class MandiRepository:
    def get_all(self):
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM mandis").fetchall()
        finally:
            conn.close()
