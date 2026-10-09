import pandas as pd
from backend.app.db.connection import get_db_connection

def get_series(crop_id: str, mandi_id: str, end_date: str) -> pd.DataFrame:
    conn = get_db_connection()
    try:
        df = conn.execute("""
            SELECT observation_date as date, modal_price, arrivals_quintals 
            FROM price_observations 
            WHERE crop_id=? AND mandi_id=? AND observation_date <= ? AND is_outlier = False
            ORDER BY observation_date ASC
        """, (crop_id, mandi_id, end_date)).df()
    finally:
        conn.close()
        
    if df.empty:
        return pd.DataFrame(columns=['date', 'modal_price', 'arrivals_quintals', 'is_imputed'])
        
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    idx = pd.date_range(start=df.index.min(), end=pd.to_datetime(end_date), freq='D')
    df = df.reindex(idx)
    
    df['is_imputed'] = df['modal_price'].isna()
    df['modal_price'] = df['modal_price'].interpolate(method='linear', limit=3)
    df['arrivals_quintals'] = df['arrivals_quintals'].interpolate(method='linear', limit=3)
    
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'date'}, inplace=True)
    
    df = df.dropna(subset=['modal_price'])
    return df

def series_coverage(crop_id: str, mandi_id: str) -> dict:
    conn = get_db_connection()
    try:
        res = conn.execute("""
            SELECT MIN(observation_date), MAX(observation_date), COUNT(*)
            FROM price_observations
            WHERE crop_id=? AND mandi_id=? AND is_outlier = False
        """, (crop_id, mandi_id)).fetchone()
        
        if not res or not res[0]:
            return {"days": 0, "gaps": 0, "latest_date": None}
            
        min_d, max_d, count = res
        total_days = (max_d - min_d).days + 1
        return {"days": count, "gaps": total_days - count, "latest_date": max_d.isoformat()}
    finally:
        conn.close()
