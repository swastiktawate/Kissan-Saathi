def check_price_wave_radar(mandi_id: str, neighbors: list, current_price: float):
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
