import asyncio
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
        conn.execute('''
            DELETE FROM price_observations 
            WHERE EXISTS (
                SELECT 1 FROM temp_obs t 
                WHERE price_observations.crop_id = t.crop_id 
                AND price_observations.mandi_id = t.mandi_id 
                AND price_observations.observation_date = t.observation_date 
                AND price_observations.variety = t.variety
            )
        ''')
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
