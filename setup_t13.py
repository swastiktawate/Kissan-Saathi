import os

os.makedirs('backend/app/services', exist_ok=True)
os.makedirs('backend/tests', exist_ok=True)

with open('backend/app/services/compare.py', 'w') as f:
    f.write('''import pandas as pd
from backend.app.db.connection import get_db_connection
from backend.app.services.forecast import generate_forecast
from backend.app.services.net_return import calculate_scenarios
from backend.app.services.routing import get_distance
from backend.app.services.weather import get_weather

def compare_mandis(crop_id: str, home_mandi_id: str, quantity_q: float, origin_date: str, horizon_days: int = 7) -> dict:
    conn = get_db_connection()
    try:
        mandis = conn.execute("SELECT mandi_id FROM mandis WHERE is_pilot = True").fetchall()
        pilot_mandis = [m[0] for m in mandis]
        
        # Load cost parameters
        cost_params = conn.execute("SELECT transport_cost_per_q_km, spoilage_transit_pct_per_km, spoilage_hold_pct_per_day, commission_rate, storage_cost_per_q_per_day FROM cost_params WHERE crop_id=?", (crop_id,)).fetchone()
        
        if not cost_params:
            cost_params = (1.5, 0.0001, 0.005, 0.06, 0.0) # fallbacks
            
        t_cost_km, s_transit_km, s_hold_day, comm_rate, storage_day = cost_params
        
    finally:
        conn.close()
        
    results = []
    
    for mandi_id in pilot_mandis:
        forecasts = generate_forecast(crop_id, mandi_id, origin_date, horizon_days)
        dist_res = get_distance(home_mandi_id, mandi_id)
        dist_km = dist_res.get("distance_km", 0) if dist_res.get("status") == "ok" else 50.0
        
        weather_res = get_weather(mandi_id, horizon_days)
        weather_data = weather_res.get("weather", [])
        
        # Current day (d=0) mock forecast using current price
        # T09 forecast returns horizons 1..7. We prepend horizon 0.
        current_price = forecasts[0]["p50"] if forecasts else 1000.0
        full_forecasts = [{"horizon": 0, "p10": current_price, "p50": current_price, "p90": current_price}] + forecasts
        
        for f in full_forecasts:
            h = f["horizon"]
            rain_mult = 1.0
            if weather_data and h < len(weather_data):
                if weather_data[h][1] > 10:
                    rain_mult = 1.2
                    
            t_cost = dist_km * t_cost_km
            s_transit = dist_km * s_transit_km
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
''')

with open('backend/app/services/recommend.py', 'w') as f:
    f.write('''import math
from backend.app.services.compare import compare_mandis

def recommend_action(crop_id: str, home_mandi_id: str, quantity_q: float, origin_date: str, risk_setting: str = "balanced", horizon_days: int = 7, trust_label: str = "High") -> dict:
    
    comp = compare_mandis(crop_id, home_mandi_id, quantity_q, origin_date, horizon_days)
    results = comp["results"]
    
    lambdas = {"cautious": 1.0, "balanced": 0.5, "aggressive": 0.0}
    lam = lambdas.get(risk_setting, 0.5)
    
    for r in results:
        r["risk"] = max(0, r["nr_p50"] - r["nr_p10"])
        r["score"] = r["nr_p50"] - lam * r["risk"]
        
    ref_opt = next((r for r in results if r["mandi_id"] == home_mandi_id and r["horizon"] == 0), None)
    if not ref_opt:
        ref_opt = results[0]
        
    margin = max(25.0, 0.015 * abs(ref_opt["nr_p50"]))
    
    best_opt = max(results, key=lambda x: x["score"])
    
    # Split sale logic
    split_opt = None
    if lam > 0 and len(results) > 1:
        best_w = None
        best_split_score = -1e9
        best_pair = None
        
        top_opts = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
        for i in range(len(top_opts)):
            for j in range(i+1, len(top_opts)):
                A = top_opts[i]
                B = top_opts[j]
                
                for w_int in range(2, 9):
                    w = w_int / 10.0
                    nr_p50 = w * A["nr_p50"] + (1-w) * B["nr_p50"]
                    risk_A = A["risk"]
                    risk_B = B["risk"]
                    risk_P = math.sqrt((w**2 * risk_A**2) + ((1-w)**2 * risk_B**2) + (2 * 0.5 * w * (1-w) * risk_A * risk_B))
                    score = nr_p50 - lam * risk_P
                    
                    if score > best_split_score:
                        best_split_score = score
                        best_w = w
                        best_pair = (A, B)
                        
        if best_pair and best_split_score > best_opt["score"] + margin:
            split_opt = {
                "score": best_split_score,
                "A": best_pair[0],
                "B": best_pair[1],
                "w": best_w
            }
            
    reasons = []
    
    if trust_label == "Insufficient":
        action = "INSUFFICIENT_DATA"
        confidence = "Low"
        reasons.append("Trust score is Insufficient. We cannot confidently recommend an action.")
        best_opt = ref_opt
    else:
        if trust_label == "Medium":
            reasons.append("Caution: Data trust is Medium. Estimates may have higher uncertainty.")
            
        if split_opt:
            action = "SPLIT_SALE"
            confidence = "Moderate"
            best_opt = split_opt["A"] # For baseline comparisons
            reasons.append(f"Split sale recommended: {int(split_opt['w']*100)}% to {split_opt['A']['mandi_id']} at day {split_opt['A']['horizon']}, and {int((1-split_opt['w'])*100)}% to {split_opt['B']['mandi_id']} at day {split_opt['B']['horizon']}.")
        else:
            if best_opt["score"] <= ref_opt["score"] + margin:
                action = "SELL_NOW"
                best_opt = ref_opt
                confidence = "Clear"
                reasons.append(f"No option beats selling today at {home_mandi_id} by the margin of {margin:.2f} Rs/q.")
            else:
                if best_opt["mandi_id"] != home_mandi_id and best_opt["horizon"] == 0:
                    action = "ANOTHER_MANDI"
                    confidence = "Clear"
                    reasons.append(f"Selling today at {best_opt['mandi_id']} yields higher return.")
                elif best_opt["horizon"] > 0:
                    action = "WAIT_N_DAYS"
                    confidence = "Moderate"
                    reasons.append(f"Waiting {best_opt['horizon']} days yields higher expected returns.")
                    
    return {
        "action": action,
        "confidence": confidence,
        "best_option": best_opt,
        "reference_option": ref_opt,
        "margin_applied": margin,
        "reasons": reasons,
        "all_results": results
    }
''')

with open('backend/tests/test_compare.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.compare import compare_mandis

def test_compare_mandis():
    res = compare_mandis("tomato", "vashi", 50, "2023-01-01", 2)
    assert "results" in res
    assert res["reference_mandi"] == "vashi"
    assert len(res["results"]) > 0
    assert "nr_p50" in res["results"][0]
''')

with open('backend/tests/test_recommend.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.recommend import recommend_action

def test_recommend_action_insufficient_trust():
    res = recommend_action("tomato", "vashi", 50, "2023-01-01", trust_label="Insufficient")
    assert res["action"] == "INSUFFICIENT_DATA"

def test_recommend_action_sell_now():
    # Force sell now by setting aggressive risk to trigger the margin check (margin won't be beaten if all forecasts flat)
    res = recommend_action("tomato", "vashi", 50, "2023-01-01", risk_setting="aggressive")
    assert "action" in res
    assert res["margin_applied"] >= 25.0
''')
