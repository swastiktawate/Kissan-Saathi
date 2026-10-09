import datetime

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
