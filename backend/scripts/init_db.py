import json
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
