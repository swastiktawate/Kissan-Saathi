import os

os.makedirs('backend/app/db', exist_ok=True)
os.makedirs('backend/scripts', exist_ok=True)
os.makedirs('backend/tests', exist_ok=True)
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/sample', exist_ok=True)

with open('backend/app/db/connection.py', 'w') as f:
    f.write('''import duckdb
from backend.app.config import settings

def get_db():
    conn = duckdb.connect(settings.DUCKDB_PATH)
    try:
        yield conn
    finally:
        conn.close()

def get_db_connection():
    return duckdb.connect(settings.DUCKDB_PATH)
''')

with open('backend/app/db/ddl.sql', 'w') as f:
    f.write('''-- Idempotent DDL for Kisan Saathi
CREATE TABLE IF NOT EXISTS crops (
    crop_id VARCHAR PRIMARY KEY,
    name_en VARCHAR,
    name_hi VARCHAR,
    name_mr VARCHAR,
    name_pa VARCHAR,
    name_hr VARCHAR,
    unit_basis VARCHAR,
    perishability_class VARCHAR,
    max_wait_days INTEGER,
    spoilage_params JSON
);

CREATE TABLE IF NOT EXISTS mandis (
    mandi_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    district VARCHAR,
    state VARCHAR,
    lat DOUBLE,
    lon DOUBLE,
    is_pilot BOOLEAN,
    aliases VARCHAR[]
);

CREATE TABLE IF NOT EXISTS price_observations (
    obs_id VARCHAR PRIMARY KEY,
    crop_id VARCHAR,
    mandi_id VARCHAR,
    observation_date DATE,
    min_price DOUBLE,
    modal_price DOUBLE,
    max_price DOUBLE,
    arrivals_quintals DOUBLE,
    variety VARCHAR,
    source VARCHAR,
    source_ref VARCHAR,
    fetched_at TIMESTAMP,
    data_origin VARCHAR,
    ingestion_run_id VARCHAR,
    is_outlier BOOLEAN,
    outlier_reason VARCHAR,
    is_imputed BOOLEAN
);

CREATE TABLE IF NOT EXISTS weather_daily (
    location_id VARCHAR,
    date DATE,
    precip_mm DOUBLE,
    precip_prob DOUBLE,
    temp_max DOUBLE,
    temp_min DOUBLE,
    is_forecast BOOLEAN,
    source VARCHAR,
    fetched_at TIMESTAMP,
    data_origin VARCHAR
);

CREATE TABLE IF NOT EXISTS distances (
    from_id VARCHAR,
    to_mandi_id VARCHAR,
    distance_km DOUBLE,
    duration_h DOUBLE,
    method VARCHAR,
    computed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS forecasts (
    forecast_id VARCHAR PRIMARY KEY,
    run_id VARCHAR,
    crop_id VARCHAR,
    mandi_id VARCHAR,
    origin_date DATE,
    target_date DATE,
    horizon_days INTEGER,
    p10 DOUBLE,
    p50 DOUBLE,
    p90 DOUBLE,
    method VARCHAR,
    calibrated BOOLEAN,
    model_version VARCHAR,
    generated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS forecast_diagnostics (
    run_id VARCHAR PRIMARY KEY,
    crop_id VARCHAR,
    mandi_id VARCHAR,
    horizon INTEGER,
    mae DOUBLE,
    pinball_loss DOUBLE,
    empirical_coverage_p10_p90 DOUBLE,
    n_eval INTEGER,
    vs_naive_skill DOUBLE
);

CREATE TABLE IF NOT EXISTS cost_params (
    crop_id VARCHAR PRIMARY KEY,
    commission_rate DOUBLE,
    hamali_rs_per_q DOUBLE,
    storage_rs_per_q_day DOUBLE,
    spoilage_transit_per_hour DOUBLE,
    spoilage_daily_rate DOUBLE,
    vehicle_tiers JSON,
    diesel_index DOUBLE,
    assumption BOOLEAN,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS trust_scores (
    crop_id VARCHAR,
    mandi_id VARCHAR,
    computed_at TIMESTAMP,
    total DOUBLE,
    components JSON,
    label VARCHAR,
    reasons VARCHAR[]
);

CREATE TABLE IF NOT EXISTS policy_events (
    event_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    summary VARCHAR,
    category VARCHAR,
    crops VARCHAR[],
    published_at TIMESTAMP,
    source_url VARCHAR,
    data_origin VARCHAR
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id VARCHAR PRIMARY KEY,
    source VARCHAR,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    status VARCHAR,
    rows_in INTEGER,
    rows_valid INTEGER,
    rows_flagged INTEGER,
    mode VARCHAR,
    error VARCHAR
);

CREATE TABLE IF NOT EXISTS backtest_runs (
    run_id VARCHAR PRIMARY KEY,
    crop_id VARCHAR,
    window INTEGER,
    strategy_params JSON,
    results JSON,
    data_origin_summary VARCHAR,
    created_at TIMESTAMP
);
''')

with open('backend/app/db/repositories.py', 'w') as f:
    f.write('''from backend.app.db.connection import get_db_connection

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
''')

with open('backend/scripts/init_db.py', 'w') as f:
    f.write('''import json
import duckdb
from backend.app.config import settings

def init_db():
    conn = duckdb.connect(settings.DUCKDB_PATH)
    
    with open('backend/app/db/ddl.sql', 'r') as f:
        ddl = f.read()
    
    # Execute DDL
    conn.execute(ddl)

    # Seed Crops
    # 4 crops (tomato, onion, potato, banana) with 5 languages
    conn.execute("""
        INSERT INTO crops (crop_id, name_en, name_hi, name_mr, name_pa, name_hr, unit_basis, perishability_class, max_wait_days, spoilage_params)
        VALUES 
        ('tomato', 'Tomato', 'Tamatar', 'Tomato', 'Tamatar', 'Tamatar', 'quintal', 'high', 4, '{}'),
        ('onion', 'Onion', 'Pyaaz', 'Kanda', 'Ganda', 'Pyaaz', 'quintal', 'low', 30, '{}'),
        ('potato', 'Potato', 'Aloo', 'Batata', 'Aloo', 'Aloo', 'quintal', 'low', 30, '{}'),
        ('banana', 'Banana', 'Kela', 'Kele', 'Kela', 'Kela', 'quintal', 'high', 5, '{}')
        ON CONFLICT (crop_id) DO NOTHING;
    """)

    # Seed Mandis
    # 5-6 pilot mandis in Mumbai/Maharashtra belt: Vashi, Nerul, Panvel, Pune, Nashik, Kalyan
    # Using approx lat/lon
    conn.execute("""
        INSERT INTO mandis (mandi_id, name, district, state, lat, lon, is_pilot, aliases)
        VALUES 
        ('vashi', 'Vashi', 'Thane', 'Maharashtra', 19.074, 72.997, true, ['Vashi APMC', 'Navi Mumbai']),
        ('nerul', 'Nerul', 'Thane', 'Maharashtra', 19.033, 73.018, true, ['Nerul APMC']),
        ('panvel', 'Panvel', 'Raigad', 'Maharashtra', 18.990, 73.116, true, ['Panvel APMC']),
        ('pune', 'Pune', 'Pune', 'Maharashtra', 18.520, 73.856, true, ['Pune APMC']),
        ('nashik', 'Nashik', 'Nashik', 'Maharashtra', 19.997, 73.789, true, ['Nashik APMC']),
        ('kalyan', 'Kalyan', 'Thane', 'Maharashtra', 19.240, 73.130, true, ['Kalyan APMC'])
        ON CONFLICT (mandi_id) DO NOTHING;
    """)

    # Seed Cost Params
    # Assumption = true for all
    vehicle_tiers = json.dumps([
        {"capacity_q": 10, "base_fare": 500, "rate_per_km": 15},
        {"capacity_q": 30, "base_fare": 1000, "rate_per_km": 25},
        {"capacity_q": 90, "base_fare": 2500, "rate_per_km": 40}
    ])
    conn.execute(f"""
        INSERT INTO cost_params (crop_id, commission_rate, hamali_rs_per_q, storage_rs_per_q_day, spoilage_transit_per_hour, spoilage_daily_rate, vehicle_tiers, diesel_index, assumption, notes)
        VALUES 
        ('tomato', 0.06, 10, 0, 0.005, 0.05, '{vehicle_tiers}', 100, true, 'team default, verify locally'),
        ('onion', 0.06, 10, 2, 0.001, 0.01, '{vehicle_tiers}', 100, true, 'team default, verify locally'),
        ('potato', 0.06, 10, 2, 0.001, 0.01, '{vehicle_tiers}', 100, true, 'team default, verify locally'),
        ('banana', 0.06, 10, 0, 0.003, 0.03, '{vehicle_tiers}', 100, true, 'team default, verify locally')
        ON CONFLICT (crop_id) DO NOTHING;
    """)

    # Distance matrix (Haversine * 1.3)
    # Using a simple python approach for distances
    import math
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    mandis = conn.execute("SELECT mandi_id, lat, lon FROM mandis").fetchall()
    
    # Just seed distances between all pairs
    for m1 in mandis:
        for m2 in mandis:
            if m1[0] != m2[0]:
                dist_km = haversine(m1[1], m1[2], m2[1], m2[2]) * 1.3
                dur_h = dist_km / 40.0 # assumed 40km/h
                
                # Check if exists
                exists = conn.execute("SELECT 1 FROM distances WHERE from_id=? AND to_mandi_id=?", (m1[0], m2[0])).fetchone()
                if not exists:
                    conn.execute("INSERT INTO distances (from_id, to_mandi_id, distance_km, duration_h, method, computed_at) VALUES (?, ?, ?, ?, 'estimated', CURRENT_TIMESTAMP)", (m1[0], m2[0], dist_km, dur_h))

    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
''')

with open('backend/tests/test_db.py', 'w') as f:
    f.write('''import os
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
''')
