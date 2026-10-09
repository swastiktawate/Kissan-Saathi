import glob
import json
import os

import pandas as pd

from backend.app.config import settings
from backend.app.ingestion.datagov import fetch_datagov_prices


async def orchestrate_ingestion(state: str, market: str, commodity: str):
    if settings.DATA_MODE in ["auto", "live"]:
        live_result = await fetch_datagov_prices(state, market, commodity)
        if live_result["status"] == "ok" and len(live_result.get("rows", [])) > 0:
            return {"status": "ok", "mode": "live", "rows_raw": live_result["rows"], "error": None}
    
    if settings.DATA_MODE in ["auto", "cached"]:
        pattern = f"data/raw/datagov_{state}_{market}_{commodity}_*.json"
        files = glob.glob(pattern)
        if files:
            latest_file = max(files, key=os.path.getctime)
            try:
                with open(latest_file, "r") as f:
                    data = json.load(f)
                    return {"status": "ok", "mode": "cached", "rows_raw": data.get("records", []), "error": None}
            except Exception:
                pass
                
    synthetic_file = "data/sample/synthetic_mandi_prices.csv"
    if os.path.exists(synthetic_file):
        df = pd.read_csv(synthetic_file)
        return {"status": "ok", "mode": "synthetic", "rows_raw": df.to_dict(orient='records'), "error": None}
        
    return {"status": "failed", "mode": "none", "rows_raw": [], "error": "All ingestion methods failed"}
