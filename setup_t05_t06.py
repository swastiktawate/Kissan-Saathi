import os

os.makedirs('backend/app/ingestion', exist_ok=True)
os.makedirs('backend/scripts', exist_ok=True)
os.makedirs('backend/tests', exist_ok=True)

with open('backend/app/ingestion/datagov.py', 'w') as f:
    f.write('''import os
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
''')

with open('backend/app/ingestion/ceda.py', 'w') as f:
    f.write('''import os
import pandas as pd

def load_ceda_data(filepath="data/sample/ceda_history.csv"):
    if not os.path.exists(filepath):
        return {"status": "failed", "error": "CEDA file not found", "rows": []}
    
    try:
        df = pd.read_csv(filepath)
        return {"status": "ok", "rows": df.to_dict(orient='records')}
    except Exception as e:
        return {"status": "failed", "error": str(e), "rows": []}
''')

with open('backend/app/ingestion/orchestrator.py', 'w') as f:
    f.write('''import os
import glob
import json
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
''')

with open('backend/scripts/ingest.py', 'w') as f:
    f.write('''import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.app.ingestion.orchestrator import orchestrate_ingestion

async def main():
    result = await orchestrate_ingestion("Maharashtra", "Vashi", "Tomato")
    print(f"Ingestion finished. Mode: {result['mode']}")
    if result['status'] != 'ok':
        print(f"Error: {result['error']}")
    else:
        print(f"Rows fetched: {len(result['rows_raw'])}")

if __name__ == "__main__":
    asyncio.run(main())
''')

with open('backend/tests/test_ingestion.py', 'w') as f:
    f.write('''import pytest
from unittest.mock import patch
from backend.app.ingestion.orchestrator import orchestrate_ingestion
from backend.app.config import settings

@pytest.mark.asyncio
@patch('backend.app.ingestion.orchestrator.fetch_datagov_prices')
async def test_orchestrator_live(mock_fetch):
    mock_fetch.return_value = {"status": "ok", "rows": [{"price": 100}], "fetched_at": "now"}
    settings.DATA_MODE = "auto"
    
    result = await orchestrate_ingestion("State", "Market", "Crop")
    assert result["mode"] == "live"
    assert len(result["rows_raw"]) == 1

@pytest.mark.asyncio
@patch('backend.app.ingestion.orchestrator.fetch_datagov_prices')
async def test_orchestrator_synthetic_fallback(mock_fetch):
    mock_fetch.return_value = {"status": "failed", "error": "mock error"}
    settings.DATA_MODE = "auto"
    
    result = await orchestrate_ingestion("State", "Market", "Crop")
    assert result["mode"] in ["synthetic", "cached"]
''')

with open('backend/app/ingestion/weather.py', 'w') as f:
    f.write('''import httpx
from backend.app.db.connection import get_db_connection

async def fetch_open_meteo(lat: float, lon: float, location_id: str):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["precipitation_sum", "precipitation_probability_max", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            precips = daily.get("precipitation_sum", [])
            probs = daily.get("precipitation_probability_max", [])
            tmax = daily.get("temperature_2m_max", [])
            tmin = daily.get("temperature_2m_min", [])
            
            conn = get_db_connection()
            try:
                for i, d in enumerate(dates):
                    conn.execute("""
                        INSERT INTO weather_daily (location_id, date, precip_mm, precip_prob, temp_max, temp_min, is_forecast, source, fetched_at, data_origin)
                        VALUES (?, ?, ?, ?, ?, ?, true, 'open-meteo', CURRENT_TIMESTAMP, 'live')
                    """, (location_id, d, precips[i], probs[i], tmax[i], tmin[i]))
            finally:
                conn.close()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

def get_weather(location_id: str, days: int):
    warnings = []
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT date, precip_mm, precip_prob, temp_max, temp_min FROM weather_daily WHERE location_id=? ORDER BY date DESC LIMIT ?",
            (location_id, days)
        ).fetchall()
        
        if len(rows) > 0:
            warnings.append("Using cached/synthetic weather data")
            return {"status": "ok", "weather": rows, "warnings": warnings}
            
        warnings.append("Weather data unavailable")
        return {"status": "unavailable", "weather": [], "warnings": warnings}
    finally:
        conn.close()
''')

with open('backend/app/ingestion/routing.py', 'w') as f:
    f.write('''import httpx
from backend.app.config import settings
from backend.app.db.connection import get_db_connection

async def fetch_osrm_distance(lat1, lon1, lat2, lon2):
    url = f"{settings.OSRM_BASE_URL}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {"overview": "false"}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("code") == "Ok":
            route = data["routes"][0]
            return {
                "distance_km": route["distance"] / 1000.0,
                "duration_h": route["duration"] / 3600.0
            }
        raise Exception("OSRM returned non-Ok code")

async def get_distance(from_id: str, to_mandi_id: str):
    warnings = []
    
    conn = get_db_connection()
    try:
        if settings.USE_LIVE_OSRM:
            loc1 = conn.execute("SELECT lat, lon FROM mandis WHERE mandi_id=?", (from_id,)).fetchone()
            loc2 = conn.execute("SELECT lat, lon FROM mandis WHERE mandi_id=?", (to_mandi_id,)).fetchone()
            
            if loc1 and loc2:
                try:
                    res = await fetch_osrm_distance(loc1[0], loc1[1], loc2[0], loc2[1])
                    return {"status": "ok", "distance_km": res["distance_km"], "duration_h": res["duration_h"], "method": "osrm", "warnings": warnings}
                except Exception as e:
                    warnings.append(f"OSRM failed: {e}. Falling back to estimated distance.")
        
        est = conn.execute("SELECT distance_km, duration_h FROM distances WHERE from_id=? AND to_mandi_id=? AND method='estimated'", (from_id, to_mandi_id)).fetchone()
        if est:
            warnings.append("Using estimated distance")
            return {"status": "ok", "distance_km": est[0], "duration_h": est[1], "method": "estimated", "warnings": warnings}
            
        return {"status": "failed", "warnings": ["No distance data available"]}
    finally:
        conn.close()
''')

with open('backend/tests/test_weather_routing.py', 'w') as f:
    f.write('''import pytest
from unittest.mock import patch
from backend.app.ingestion.routing import get_distance
from backend.app.config import settings

@pytest.mark.asyncio
@patch('backend.app.ingestion.routing.fetch_osrm_distance')
async def test_get_distance_fallback(mock_osrm):
    mock_osrm.side_effect = Exception("Network error")
    settings.USE_LIVE_OSRM = True
    
    res = await get_distance("pune", "vashi")
    
    assert res["status"] == "ok"
    assert res["method"] == "estimated"
    assert "Using estimated distance" in res["warnings"] or any("OSRM failed" in w for w in res["warnings"])
''')
