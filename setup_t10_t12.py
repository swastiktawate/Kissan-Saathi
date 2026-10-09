import os

os.makedirs('backend/app/services', exist_ok=True)
os.makedirs('backend/tests', exist_ok=True)

with open('backend/app/services/trust.py', 'w') as f:
    f.write('''def calculate_trust_score(
    days_since_last_fetch: int, 
    missing_ratio: float, 
    history_days: int, 
    forecast_mape: float, 
    data_origin: str
) -> dict:
    
    freshness = max(0.0, 30.0 * (1 - (days_since_last_fetch / 7.0)))
    completeness = max(0.0, 25.0 * (1 - (missing_ratio / 0.2)))
    history = min(15.0, 15.0 * (history_days / 180.0))
    forecast = max(0.0, 20.0 * (1 - ((forecast_mape - 0.1) / 0.4))) if forecast_mape >= 0.1 else 20.0
    source = 10.0 if data_origin == 'live' else (5.0 if data_origin == 'cached' else 0.0)
    
    raw_score = freshness + completeness + history + forecast + source
    
    reasons = []
    if days_since_last_fetch > 3:
        reasons.append("Data is stale (>3 days old).")
    if missing_ratio > 0.1:
        reasons.append("High missing data ratio.")
    if history_days < 90:
        reasons.append("Insufficient history (<90 days).")
        
    score = round(raw_score)
    if data_origin in ['sample', 'synthetic']:
        if score > 60:
            score = 60
            reasons.append("Score capped at 60 due to synthetic/sample origin.")
            
    if score >= 70:
        label = "High"
    elif score >= 40:
        label = "Medium"
    else:
        label = "Insufficient"
        
    return {
        "score": score,
        "label": label,
        "components": {
            "freshness": round(freshness, 1),
            "completeness": round(completeness, 1),
            "history": round(history, 1),
            "forecast": round(forecast, 1),
            "source": round(source, 1)
        },
        "reasons": reasons,
        "calibrated": False
    }
''')

with open('backend/app/services/net_return.py', 'w') as f:
    f.write('''def calculate_net_return(
    price: float,
    qty_quintals: float,
    s_transit: float,
    s_hold: float,
    commission_rate: float,
    transport_cost_per_quintal: float,
    surcharge_per_quintal: float,
    rain_mult: float = 1.0
):
    
    effective_s_transit = min(1.0, s_transit * rain_mult)
    s_total = 1 - (1 - effective_s_transit) * (1 - s_hold)
    
    g = price * (1 - s_total)
    comm = commission_rate * g
    
    nr = g - comm - transport_cost_per_quintal - surcharge_per_quintal
    total_val = nr * qty_quintals
    
    spoilage_cost = price - g
    
    drivers = {
        "base_price": price,
        "spoilage_cost": -spoilage_cost,
        "commission": -comm,
        "transport": -transport_cost_per_quintal,
        "surcharge": -surcharge_per_quintal
    }
    
    assert abs(sum(drivers.values()) - nr) < 1e-6, "Drivers do not sum to NR exactly"
    
    return {
        "net_return_per_quintal": round(nr, 2),
        "total_net_return": round(total_val, 2),
        "gross_realized_price": round(g, 2),
        "spoilage_total_pct": round(s_total, 4),
        "drivers": {k: round(v, 2) for k, v in drivers.items()}
    }

def calculate_scenarios(price_p10, price_p50, price_p90, qty, params):
    return {
        "p10": calculate_net_return(price_p10, qty, **params),
        "p50": calculate_net_return(price_p50, qty, **params),
        "p90": calculate_net_return(price_p90, qty, **params),
    }
''')

with open('backend/app/services/pooling.py', 'w') as f:
    f.write('''def calculate_farmer_pool(farmers: list, nr_result_per_quintal: float):
    total_qty = sum(f["qty"] for f in farmers)
    
    pool_results = []
    for f in farmers:
        share = f["qty"] / total_qty if total_qty > 0 else 0
        payout = nr_result_per_quintal * f["qty"]
        pool_results.append({
            "farmer_id": f["id"],
            "qty": f["qty"],
            "share_pct": round(share * 100, 2),
            "payout": round(payout, 2)
        })
        
    return {
        "total_pool_qty": total_qty,
        "total_pool_payout": round(nr_result_per_quintal * total_qty, 2),
        "farmers": pool_results
    }
''')

with open('backend/app/services/risk_flags.py', 'w') as f:
    f.write('''import datetime

def evaluate_risk_flags(context: dict) -> list:
    flags = []
    as_of = datetime.datetime.now().isoformat()
    
    if context.get('price_drop_pct', 0) > 0.15:
        flags.append({
            "code": "PRICE_DROP",
            "severity": "high",
            "evidence": f"Price dropped {context['price_drop_pct']*100}% in 7 days",
            "source": "price_series",
            "as_of": as_of
        })
        
    if context.get('arrival_z_score', 0) > 2.0:
        flags.append({
            "code": "ARRIVAL_SURGE",
            "severity": "medium",
            "evidence": f"Arrival surge with z-score {context['arrival_z_score']}",
            "source": "arrival_series",
            "as_of": as_of
        })
        
    if context.get('volatility', 0) > 0.2:
        flags.append({
            "code": "VOLATILITY",
            "severity": "medium",
            "evidence": f"High volatility {context['volatility']}",
            "source": "price_series",
            "as_of": as_of
        })
        
    if context.get('days_stale', 0) > 3:
        flags.append({
            "code": "STALE_DATA",
            "severity": "medium",
            "evidence": f"Data is {context['days_stale']} days stale",
            "source": "ingestion",
            "as_of": as_of
        })
        
    if context.get('forecast_spread_pct', 0) > 0.4:
        flags.append({
            "code": "WEAK_FORECAST",
            "severity": "medium",
            "evidence": "Wide P10-P90 forecast spread indicates uncertainty",
            "source": "forecast_engine",
            "as_of": as_of
        })
        
    if context.get('rain_mm', 0) > 20:
        flags.append({
            "code": "HEAVY_RAIN",
            "severity": "high",
            "evidence": f"Heavy rain forecasted: {context['rain_mm']}mm",
            "source": "weather_api",
            "as_of": as_of
        })
        
    return flags
''')

with open('backend/app/services/radar.py', 'w') as f:
    f.write('''def check_price_wave_radar(mandi_id: str, neighbors: list, current_price: float):
    alerts = []
    
    for n in neighbors:
        if n.get("historical_corr", 0) > 0.6:
            price_diff_pct = (n.get("price", current_price) - current_price) / current_price
            if price_diff_pct < -0.10:
                alerts.append({
                    "neighbor": n["id"],
                    "lead_lag_alert": "neighbor_dropped",
                    "price_diff_pct": price_diff_pct
                })
                
    return {
        "mandi_id": mandi_id,
        "radar_alerts": alerts,
        "wave_risk_score": len(alerts) * 0.2
    }
''')

with open('backend/app/services/policy.py', 'w') as f:
    f.write('''def get_policy_events():
    return [
        {
            "event_id": "pol_001",
            "title": "Onion Export Ban Rumour",
            "date": "2023-12-01",
            "impact_direction": "negative",
            "data_origin": "sample"
        },
        {
            "event_id": "pol_002",
            "title": "New subsidy for tomato transport",
            "date": "2024-01-15",
            "impact_direction": "positive",
            "data_origin": "sample"
        }
    ]
''')

with open('backend/tests/test_trust.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.trust import calculate_trust_score

def test_trust_score_fresh():
    res = calculate_trust_score(0, 0.0, 180, 0.1, "live")
    assert res["score"] == 100
    assert res["label"] == "High"

def test_trust_score_stale():
    res = calculate_trust_score(7, 0.0, 180, 0.1, "live")
    assert res["components"]["freshness"] == 0.0
    assert "Data is stale (>3 days old)." in res["reasons"]

def test_trust_score_synthetic_cap():
    res = calculate_trust_score(0, 0.0, 180, 0.1, "synthetic")
    assert res["score"] == 60
    assert res["label"] == "Medium"
    assert "Score capped at 60 due to synthetic/sample origin." in res["reasons"]
''')

with open('backend/tests/test_net_return.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.net_return import calculate_net_return

def test_worked_example():
    res = calculate_net_return(
        price=2000,
        qty_quintals=50,
        s_transit=0.03,
        s_hold=0.0,
        commission_rate=0.06,
        transport_cost_per_quintal=100,
        surcharge_per_quintal=0
    )
    
    assert res["net_return_per_quintal"] == 1723.60
    assert res["total_net_return"] == 86180.0
    
    d = res["drivers"]
    assert d["base_price"] == 2000
    assert d["spoilage_cost"] == -60
    assert d["commission"] == -116.40
    assert d["transport"] == -100
    assert d["surcharge"] == 0
''')

with open('backend/tests/test_pooling.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.pooling import calculate_farmer_pool

def test_farmer_pool():
    farmers = [{"id": 1, "qty": 10}, {"id": 2, "qty": 40}]
    res = calculate_farmer_pool(farmers, 1723.60)
    
    assert res["total_pool_qty"] == 50
    assert res["total_pool_payout"] == 86180.0
    
    assert res["farmers"][0]["share_pct"] == 20.0
    assert res["farmers"][0]["payout"] == 17236.0
    
    assert res["farmers"][1]["share_pct"] == 80.0
    assert res["farmers"][1]["payout"] == 68944.0
''')

with open('backend/tests/test_risk_flags.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.risk_flags import evaluate_risk_flags

def test_risk_flags():
    # Only triggers on edge cases
    flags = evaluate_risk_flags({
        "price_drop_pct": 0.20,
        "rain_mm": 5
    })
    
    assert len(flags) == 1
    assert flags[0]["code"] == "PRICE_DROP"

    flags2 = evaluate_risk_flags({
        "price_drop_pct": 0.0,
        "rain_mm": 50
    })
    assert len(flags2) == 1
    assert flags2[0]["code"] == "HEAVY_RAIN"
''')

with open('backend/tests/test_radar.py', 'w') as f:
    f.write('''import pytest
from backend.app.services.radar import check_price_wave_radar

def test_radar():
    neighbors = [{"id": "n1", "price": 80, "historical_corr": 0.8}]
    res = check_price_wave_radar("vashi", neighbors, 100)
    
    assert len(res["radar_alerts"]) == 1
    assert res["radar_alerts"][0]["neighbor"] == "n1"
    assert res["radar_alerts"][0]["price_diff_pct"] == -0.20
''')
