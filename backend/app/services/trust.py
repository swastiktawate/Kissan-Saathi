def calculate_trust_score(
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
