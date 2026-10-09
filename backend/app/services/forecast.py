import numpy as np

from backend.app.config import settings
from backend.app.services.series import get_series


def generate_forecast(crop_id: str, mandi_id: str, origin_date: str, horizon_days: int = 7) -> list:
    df = get_series(crop_id, mandi_id, origin_date)
    
    if len(df) < 7:
        last_val = df['modal_price'].iloc[-1] if not df.empty else 1000.0
        return [{"horizon": h, "p10": last_val*0.8, "p50": last_val, "p90": last_val*1.2, "method": "fallback", "calibrated": False} for h in range(1, horizon_days+1)]
        
    alpha = settings.EWMA_ALPHA
    ewma = df['modal_price'].ewm(alpha=alpha, adjust=False).mean().iloc[-1]
    
    recent = df['modal_price'].tail(14).values
    trend = np.mean(np.diff(recent)) if len(recent) > 1 else 0
    damping = settings.TREND_DAMPING
    
    df['ewma_pred'] = df['modal_price'].ewm(alpha=alpha, adjust=False).mean().shift(1)
    res_rel = ((df['modal_price'] - df['ewma_pred']) / df['ewma_pred']).dropna()
    
    if len(res_rel) >= settings.MIN_RESIDUALS_FOR_EMPIRICAL_BAND:
        p10_pct = np.percentile(res_rel, 10)
        p90_pct = np.percentile(res_rel, 90)
    else:
        p10_pct = -0.20
        p90_pct = 0.20
        
    forecasts = []
    current_level = ewma
    current_trend = trend
    
    for h in range(1, horizon_days + 1):
        current_trend *= damping
        current_level += current_trend
        
        p50 = max(1.0, current_level)
        p10 = max(1.0, p50 * (1 + p10_pct))
        p90 = max(1.0, p50 * (1 + p90_pct))
        
        p10, p50, p90 = sorted([p10, p50, p90])
        
        forecasts.append({
            "horizon": h,
            "p10": p10,
            "p50": p50,
            "p90": p90,
            "method": "baseline_ewma_damped_trend",
            "calibrated": False
        })
        
    return forecasts
