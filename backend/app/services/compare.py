import pandas as pd
from backend.app.db.connection import get_db_connection
from backend.app.services.forecast import generate_forecast
from backend.app.services.net_return import calculate_scenarios
from backend.app.ingestion.routing import get_distance
from backend.app.ingestion.weather import get_weather

async def compare_mandis(crop_id: str, home_mandi_id: str, quantity_q: float, origin_date: str, horizon_days: int = 7) -> dict:
    conn = get_db_connection()
    try:
        mandis = conn.execute("SELECT mandi_id FROM mandis WHERE is_pilot = True").fetchall()
        pilot_mandis = [m[0] for m in mandis]
        
        # Load cost parameters
        cost_params = conn.execute("SELECT commission_rate, storage_rs_per_q_day, spoilage_transit_per_hour, spoilage_daily_rate FROM cost_params WHERE crop_id=?", (crop_id,)).fetchone()
        
        if not cost_params:
            cost_params = (0.06, 0.0, 0.001, 0.005) # fallbacks
            
        comm_rate, storage_day, s_transit_hr, s_hold_day = cost_params
        
    finally:
        conn.close()
        
    results = []
    
    for mandi_id in pilot_mandis:
        forecasts = generate_forecast(crop_id, mandi_id, origin_date, horizon_days)
        dist_res = await get_distance(home_mandi_id, mandi_id)
        dist_km = dist_res.get("distance_km", 0) if dist_res.get("status") == "ok" else 50.0
        dist_h = dist_res.get("duration_h", dist_km / 40.0) if dist_res.get("status") == "ok" else dist_km / 40.0
        
        weather_res = get_weather(mandi_id, horizon_days)
        weather_data = weather_res.get("weather", [])
        
        current_price = forecasts[0]["p50"] if forecasts else 1000.0
        full_forecasts = [{"horizon": 0, "p10": current_price, "p50": current_price, "p90": current_price}] + forecasts
        
        for f in full_forecasts:
            h = f["horizon"]
            rain_mult = 1.0
            if weather_data and h < len(weather_data):
                if weather_data[h][1] > 10:
                    rain_mult = 1.2
                    
            t_cost = dist_km * 2.0 # simplified from vehicle tiers
            s_transit = dist_h * s_transit_hr
            s_hold = h * s_hold_day
            surcharge = h * storage_day
            
            params = {
                "s_transit": s_transit,
                "s_hold": s_hold,
                "commission_rate": comm_rate,
                "transport_cost_per_quintal": t_cost,
                "surcharge_per_quintal": surcharge,
                "rain_mult": rain_mult
            }
            
            nr_scenarios = calculate_scenarios(f["p10"], f["p50"], f["p90"], quantity_q, params)
            
            results.append({
                "mandi_id": mandi_id,
                "horizon": h,
                "nr_p10": nr_scenarios["p10"]["net_return_per_quintal"],
                "nr_p50": nr_scenarios["p50"]["net_return_per_quintal"],
                "nr_p90": nr_scenarios["p90"]["net_return_per_quintal"],
                "nr_scenarios": nr_scenarios
            })
            
    return {"reference_mandi": home_mandi_id, "results": results}
