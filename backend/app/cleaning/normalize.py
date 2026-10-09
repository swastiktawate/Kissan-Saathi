import pandas as pd

from backend.app.db.connection import get_db_connection


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    
    # Parse dates
    df['observation_date'] = pd.to_datetime(df['arrival_date'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    try:
        crops = conn.execute("SELECT crop_id, name_en, name_hi FROM crops").fetchall()
        mandis = conn.execute("SELECT mandi_id, name, aliases FROM mandis").fetchall()
    finally:
        conn.close()
        
    crop_map = {}
    for c in crops:
        crop_map[c[1].lower()] = c[0]
        if c[2]: crop_map[c[2].lower()] = c[0]
        
    mandi_map = {}
    for m in mandis:
        mandi_map[m[1].lower()] = m[0]
        if m[2]:
            for a in m[2]:
                mandi_map[a.lower()] = m[0]
                
    df['crop_id'] = df['commodity'].str.lower().map(crop_map).fillna(df['commodity'].str.lower())
    df['mandi_id'] = df['market'].str.lower().map(mandi_map).fillna(df['market'].str.lower())
    
    if 'fetched_at' not in df.columns:
        df['fetched_at'] = pd.Timestamp.now().isoformat()
    
    df = df.sort_values('fetched_at').drop_duplicates(subset=['crop_id', 'mandi_id', 'observation_date', 'variety'], keep='last')
    return df
