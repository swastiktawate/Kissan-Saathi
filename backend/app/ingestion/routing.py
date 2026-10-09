import httpx
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
