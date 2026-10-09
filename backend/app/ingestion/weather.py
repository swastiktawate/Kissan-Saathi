import httpx
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
