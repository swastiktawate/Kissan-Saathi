import os

import pandas as pd


def load_ceda_data(filepath="data/sample/ceda_history.csv"):
    if not os.path.exists(filepath):
        return {"status": "failed", "error": "CEDA file not found", "rows": []}
    
    try:
        df = pd.read_csv(filepath)
        return {"status": "ok", "rows": df.to_dict(orient='records')}
    except Exception as e:
        return {"status": "failed", "error": str(e), "rows": []}
