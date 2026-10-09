import os
import httpx
import json
import datetime
from backend.app.config import settings

async def fetch_datagov_prices(state: str, market: str, commodity: str):
    if not settings.DATA_GOV_API_KEY or not settings.DATA_GOV_RESOURCE_ID:
        return {"status": "failed", "error": "API key or resource ID not configured"}
        
    url = f"https://api.data.gov.in/resource/{settings.DATA_GOV_RESOURCE_ID}"
    params = {
        "api-key": settings.DATA_GOV_API_KEY,
        "format": "json",
        "filters[state]": state,
        "filters[market]": market,
        "filters[commodity]": commodity,
        "limit": 100
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            os.makedirs("data/raw", exist_ok=True)
            timestamp = datetime.datetime.now().isoformat().replace(":", "-")
            filename = f"data/raw/datagov_{state}_{market}_{commodity}_{timestamp}.json"
            
            with open(filename, "w") as f:
                json.dump(data, f)
                
            return {"status": "ok", "rows": data.get("records", []), "fetched_at": timestamp}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
