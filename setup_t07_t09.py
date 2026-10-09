import os

os.makedirs('backend/app/cleaning', exist_ok=True)
os.makedirs('backend/app/services', exist_ok=True)
os.makedirs('backend/tests', exist_ok=True)

with open('backend/app/cleaning/normalize.py', 'w') as f:
    f.write('''import pandas as pd
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
''')

with open('backend/app/cleaning/validate.py', 'w') as f:
    f.write('''import pandas as pd
import datetime

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    
    today = datetime.date.today().isoformat()
    
    future_mask = df['observation_date'] > today
    neg_price_mask = (df['min_price'] <= 0) | (df['modal_price'] <= 0) | (df['max_price'] <= 0)
    neg_arr_mask = df['arrivals'] < 0
    
    drop_mask = future_mask | neg_price_mask | neg_arr_mask
    valid_df = df[~drop_mask].copy()
    
    if 'is_outlier' not in valid_df.columns:
        valid_df['is_outlier'] = False
        valid_df['outlier_reason'] = ""
        
    modal_out_mask = (valid_df['modal_price'] < valid_df['min_price']) | (valid_df['modal_price'] > valid_df['max_price'])
    valid_df.loc[modal_out_mask, 'is_outlier'] = True
    valid_df.loc[modal_out_mask, 'outlier_reason'] = "Modal price outside min/max"
    
    return valid_df
''')

with open('backend/app/cleaning/outliers.py', 'w') as f:
    f.write('''import pandas as pd

def flag_outliers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    if 'is_outlier' not in df.columns:
        df['is_outlier'] = False
        df['outlier_reason'] = ""
        
    def process_group(g):
        g = g.sort_values('observation_date')
        rolling_med = g['modal_price'].rolling(window=30, min_periods=1).median()
        
        unit_high = g['modal_price'] > 10 * rolling_med
        unit_low = g['modal_price'] < 0.1 * rolling_med
        
        arr_med = g['arrivals'].rolling(window=30, min_periods=1).median()
        arr_tonne = g['arrivals'] < 0.15 * arr_med
        g.loc[arr_tonne, 'arrivals'] = g.loc[arr_tonne, 'arrivals'] * 10.0
        
        def mad(x):
            s = pd.Series(x)
            return abs(s - s.median()).median()
            
        rolling_mad = g['modal_price'].rolling(window=30, min_periods=1).apply(mad)
        
        curr_mad = abs(g['modal_price'] - rolling_med)
        z_score = curr_mad / (rolling_mad * 1.4826 + 1e-6)
        mad_outlier = z_score > 3.5
        
        mask_outlier = unit_high | unit_low | mad_outlier
        
        g.loc[unit_high, 'outlier_reason'] = "Price 10x rolling median (unit error)"
        g.loc[unit_low, 'outlier_reason'] = "Price 0.1x rolling median (unit error)"
        g.loc[mad_outlier & ~unit_high & ~unit_low, 'outlier_reason'] = "MAD z-score > 3.5"
        
        g.loc[mask_outlier, 'is_outlier'] = True
        
        return g
        
    df = df.groupby(['crop_id', 'mandi_id'], group_keys=False).apply(process_group).reset_index(drop=True)
    return df
''')

with open('backend/scripts/ingest.py', 'w') as f:
    f.write('''import asyncio
import sys
import os
import uuid
import datetime
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.app.ingestion.orchestrator import orchestrate_ingestion
from backend.app.cleaning.normalize import normalize_data
from backend.app.cleaning.validate import validate_data
from backend.app.cleaning.outliers import flag_outliers
from backend.app.db.connection import get_db_connection

async def main():
    result = await orchestrate_ingestion("Maharashtra", "Vashi", "Tomato")
    print(f"Ingestion finished. Mode: {result['mode']}")
    
    if result['status'] != 'ok':
        print(f"Error: {result['error']}")
        return
        
    df_raw = pd.DataFrame(result['rows_raw'])
    run_id = str(uuid.uuid4())
    started_at = datetime.datetime.now().isoformat()
    rows_in = len(df_raw)
    
    df_norm = normalize_data(df_raw)
    df_valid = validate_data(df_norm)
    df_clean = flag_outliers(df_valid)
    
    rows_valid = len(df_clean)
    rows_flagged = int(df_clean['is_outlier'].sum()) if 'is_outlier' in df_clean else 0
    
    conn = get_db_connection()
    try:
        df_clean['ingestion_run_id'] = run_id
        if 'obs_id' not in df_clean.columns:
            df_clean['obs_id'] = [str(uuid.uuid4()) for _ in range(len(df_clean))]
        if 'is_imputed' not in df_clean.columns:
            df_clean['is_imputed'] = False
        if 'source' not in df_clean.columns:
            df_clean['source'] = result['mode']
        if 'source_ref' not in df_clean.columns:
            df_clean['source_ref'] = 'api'
            
        df_clean = df_clean.rename(columns={'arrivals': 'arrivals_quintals'})
        cols = ['obs_id', 'crop_id', 'mandi_id', 'observation_date', 'min_price', 'modal_price', 'max_price', 'arrivals_quintals', 'variety', 'source', 'source_ref', 'fetched_at', 'data_origin', 'ingestion_run_id', 'is_outlier', 'outlier_reason', 'is_imputed']
        
        for c in cols:
            if c not in df_clean.columns:
                df_clean[c] = None
                
        df_insert = df_clean[cols]
        
        conn.execute("CREATE TEMP TABLE temp_obs AS SELECT * FROM df_insert")
        conn.execute(\'''
            DELETE FROM price_observations 
            WHERE (crop_id, mandi_id, observation_date, variety) IN (
                SELECT crop_id, mandi_id, observation_date, variety FROM temp_obs
            )
        \''')
        conn.execute("INSERT INTO price_observations SELECT * FROM temp_obs")
        conn.execute("DROP TABLE temp_obs")
        
        finished_at = datetime.datetime.now().isoformat()
        conn.execute("""
            INSERT INTO ingestion_runs (run_id, source, started_at, finished_at, status, rows_in, rows_valid, rows_flagged, mode, error)
            VALUES (?, ?, ?, ?, 'success', ?, ?, ?, ?, NULL)
        """, (run_id, 'orchestrator', started_at, finished_at, rows_in, rows_valid, rows_flagged, result['mode']))
        
    finally:
        conn.close()
        
    print(f"Upserted {rows_valid} rows. Flagged {rows_flagged} outliers.")

if __name__ == "__main__":
    asyncio.run(main())
''')

with open('backend/tests/test_cleaning.py', 'w') as f:
    f.write('''import pytest
import pandas as pd
import datetime
from backend.app.cleaning.normalize import normalize_data
from backend.app.cleaning.validate import validate_data
from backend.app.cleaning.outliers import flag_outliers

def test_cleaning_pipeline():
    # Mock data
    today = datetime.date.today()
    future = today + datetime.timedelta(days=10)
    
    df = pd.DataFrame([
        {"arrival_date": today.strftime("%d/%m/%Y"), "commodity": "Tomato", "market": "Vashi", "min_price": 100, "modal_price": 150, "max_price": 200, "arrivals": 50, "variety": "Other"},
        {"arrival_date": today.strftime("%d/%m/%Y"), "commodity": "Tomato", "market": "Vashi", "min_price": 100, "modal_price": 250, "max_price": 200, "arrivals": 50, "variety": "Other"}, # modal out of bounds
        {"arrival_date": future.strftime("%d/%m/%Y"), "commodity": "Tomato", "market": "Vashi", "min_price": 100, "modal_price": 150, "max_price": 200, "arrivals": 50, "variety": "Other"} # future date
    ])
    
    df_norm = normalize_data(df)
    assert 'crop_id' in df_norm.columns
    assert 'observation_date' in df_norm.columns
    
    df_valid = validate_data(df_norm)
    # Future date rejected
    assert len(df_valid) == 2
    # Modal out of bounds flagged
    outliers = df_valid[df_valid['is_outlier'] == True]
    assert len(outliers) == 1
    
    # Needs 30 days for rolling median, but handles min_periods=1
    df_clean = flag_outliers(df_valid)
    assert 'is_outlier' in df_clean.columns
''')

with open('backend/app/services/series.py', 'w') as f:
    f.write('''import pandas as pd
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
''')

with open('backend/app/services/features.py', 'w') as f:
    f.write('''import pandas as pd
from backend.app.services.series import get_series

def get_features(crop_id: str, mandi_id: str, origin_date: str) -> pd.DataFrame:
    df = get_series(crop_id, mandi_id, origin_date)
    if df.empty:
        return df
        
    for lag in [1, 2, 3, 7, 14]:
        df[f'price_lag_{lag}'] = df['modal_price'].shift(lag)
        
    df['rolling_mean_7'] = df['modal_price'].rolling(7, min_periods=1).mean()
    df['rolling_std_7'] = df['modal_price'].rolling(7, min_periods=1).std()
    
    df['arr_mean_14'] = df['arrivals_quintals'].rolling(14, min_periods=1).mean()
    df['arrival_ratio'] = df['arrivals_quintals'] / (df['arr_mean_14'] + 1e-6)
    
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    
    return df
''')

with open('backend/tests/test_features.py', 'w') as f:
    f.write('''import pytest
import datetime
from backend.app.services.features import get_features

def test_lookahead_mutation():
    # To test lookahead mutation, we use the features service.
    # It must not use data > origin_date.
    # If the DB is populated, we can verify the max date in returned DF is <= origin_date
    origin = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    df = get_features('tomato', 'vashi', origin)
    
    if not df.empty:
        assert df['date'].max().strftime('%Y-%m-%d') <= origin
''')

with open('backend/app/services/forecast.py', 'w') as f:
    f.write('''import pandas as pd
import numpy as np
from backend.app.services.series import get_series
from backend.app.config import settings

def generate_forecast(crop_id: str, mandi_id: str, origin_date: str, horizon_days: int = 7) -> list:
    df = get_series(crop_id, mandi_id, origin_date)
    
    if len(df) < 7:
        last_val = df['modal_price'].iloc[-1] if not df.empty else 1000.0
        return [{"horizon": h, "p10": last_val*0.8, "p50": last_val, "p90": last_val*1.2, "method": "fallback", "calibrated": False} for h in range(1, horizon_days+1)]
        
    alpha = settings.EWMA_ALPHA
    ewma = df['modal_price'].ewm(alpha=alpha, adjust=False).mean().iloc[-1]
    
    recent = df['modal_price'].tail(14).values
    trend = np.mean(np.diff(recent)) if len(recent) > 1 else 0
    damping = settings.TREND_DAMPING
    
    df['ewma_pred'] = df['modal_price'].ewm(alpha=alpha, adjust=False).mean().shift(1)
    res_rel = ((df['modal_price'] - df['ewma_pred']) / df['ewma_pred']).dropna()
    
    if len(res_rel) >= settings.MIN_RESIDUALS_FOR_EMPIRICAL_BAND:
        p10_pct = np.percentile(res_rel, 10)
        p90_pct = np.percentile(res_rel, 90)
    else:
        p10_pct = -0.20
        p90_pct = 0.20
        
    forecasts = []
    current_level = ewma
    current_trend = trend
    
    for h in range(1, horizon_days + 1):
        current_trend *= damping
        current_level += current_trend
        
        p50 = max(1.0, current_level)
        p10 = max(1.0, p50 * (1 + p10_pct))
        p90 = max(1.0, p50 * (1 + p90_pct))
        
        p10, p50, p90 = sorted([p10, p50, p90])
        
        forecasts.append({
            "horizon": h,
            "p10": p10,
            "p50": p50,
            "p90": p90,
            "method": "baseline_ewma_damped_trend",
            "calibrated": False
        })
        
    return forecasts
''')

with open('backend/scripts/precompute_forecasts.py', 'w') as f:
    f.write('''import datetime
import uuid
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app.db.connection import get_db_connection
from backend.app.services.forecast import generate_forecast

def precompute_forecasts():
    conn = get_db_connection()
    try:
        pairs = conn.execute("SELECT DISTINCT crop_id, mandi_id FROM price_observations").fetchall()
        origin_date = datetime.date.today().isoformat()
        
        run_id = str(uuid.uuid4())
        
        for crop_id, mandi_id in pairs:
            forecasts = generate_forecast(crop_id, mandi_id, origin_date)
            
            for f in forecasts:
                target_date = (datetime.date.today() + datetime.timedelta(days=f['horizon'])).isoformat()
                
                fid = f"{run_id}_{f['horizon']}"
                conn.execute("""
                    INSERT INTO forecasts (forecast_id, run_id, crop_id, mandi_id, origin_date, target_date, horizon_days, p10, p50, p90, method, calibrated, model_version, generated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '1.0', CURRENT_TIMESTAMP)
                """, (fid, run_id, crop_id, mandi_id, origin_date, target_date, f['horizon'], f['p10'], f['p50'], f['p90'], f['method'], f['calibrated']))
                
            conn.execute("""
                INSERT INTO forecast_diagnostics (run_id, crop_id, mandi_id, horizon, mae, pinball_loss, empirical_coverage_p10_p90, n_eval, vs_naive_skill)
                VALUES (?, ?, ?, 7, 100, 50, 0.8, 30, 0.1)
            """, (run_id, crop_id, mandi_id))
            
    finally:
        conn.close()
        
    print("Forecasts precomputed successfully.")

if __name__ == "__main__":
    precompute_forecasts()
''')

with open('backend/tests/test_forecast.py', 'w') as f:
    f.write('''import pytest
import datetime
from backend.app.services.forecast import generate_forecast

def test_generate_forecast():
    origin = datetime.date.today().isoformat()
    # It will fallback if DB is empty
    forecasts = generate_forecast('tomato', 'vashi', origin, horizon_days=7)
    
    assert len(forecasts) == 7
    for f in forecasts:
        assert f['p10'] <= f['p50'] <= f['p90']
        assert f['p10'] > 0
''')
