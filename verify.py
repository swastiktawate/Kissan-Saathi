import os
import subprocess
import time
import urllib.request
import json

def check_env_duckdb_git():
    print("Checking git ls-files for .env and .duckdb...")
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Git ls-files failed")
        return False
    
    files = result.stdout.splitlines()
    bad_files = [f for f in files if f.endswith('.env') or f.endswith('.duckdb')]
    if bad_files:
        print(f"FAILED: Found tracked .env or .duckdb files: {bad_files}")
        return False
    print("PASS: No .env or .duckdb tracked.")
    return True

def check_config():
    print("Checking config without .env...")
    if os.path.exists('.env'):
        os.rename('.env', '.env.bak')
    
    try:
        from backend.app.config import settings
        if settings.DATA_MODE not in ["auto", "sample", "synthetic"]:
            print(f"FAILED: Unexpected DATA_MODE: {settings.DATA_MODE}")
            return False
        print(f"PASS: config loaded successfully. DATA_MODE: {settings.DATA_MODE}")
        return True
    except Exception as e:
        print(f"FAILED: config load failed: {e}")
        return False
    finally:
        if os.path.exists('.env.bak'):
            os.rename('.env.bak', '.env')

def check_init_db():
    print("Checking init_db idempotency...")
    import duckdb
    from backend.scripts.init_db import init_db
    
    init_db()
    conn = duckdb.connect("data/kisan.duckdb")
    mandis_count1 = conn.execute("SELECT count(*) FROM mandis").fetchone()[0]
    
    init_db()
    mandis_count2 = conn.execute("SELECT count(*) FROM mandis").fetchone()[0]
    
    if mandis_count1 != mandis_count2:
        print(f"FAILED: Idempotency check failed. Count 1: {mandis_count1}, Count 2: {mandis_count2}")
        return False
        
    crops_count = conn.execute("SELECT count(*) FROM crops").fetchone()[0]
    if crops_count < 4:
        print(f"FAILED: Only {crops_count} crops found. Expected >= 4.")
        return False
        
    cost_params = conn.execute("SELECT count(*) FROM cost_params WHERE assumption = true").fetchone()[0]
    if cost_params < 4:
        print(f"FAILED: Only {cost_params} cost_params with assumption=true found.")
        return False
        
    print("PASS: DB initialized correctly and is idempotent.")
    return True

if __name__ == '__main__':
    ok = True
    ok = ok and check_env_duckdb_git()
    ok = ok and check_config()
    ok = ok and check_init_db()
    
    if ok:
        print("ALL PYTHON CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED")
