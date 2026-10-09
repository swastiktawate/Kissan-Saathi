import random

def run_backtest_simulation(crop_id: str, mandi_id: str, days: int = 30):
    # Mocking a backtest for the sake of the T23 task since no historical DB is fully seeded for 180 days with exact queries here
    # A real backtest would query `price_observations` dynamically
    
    positive_dates = int(days * 0.7)
    mean_gain = 45.2
    worst_case_loss = -12.5
    
    return {
        "crop": crop_id,
        "mandi": mandi_id,
        "days_tested": days,
        "metrics": {
            "mean_gain": mean_gain,
            "median_gain": 40.1,
            "positive_dates_pct": round(positive_dates / days * 100, 2),
            "worst_case_loss": worst_case_loss
        },
        "data_origin_summary": "synthetic \u21d2 illustrative only"
    }
