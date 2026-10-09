import pytest
import datetime
from backend.app.services.forecast import generate_forecast

def test_generate_forecast():
    origin = datetime.date.today().isoformat()
    # It will fallback if DB is empty
    forecasts = generate_forecast('tomato', 'vashi', origin, horizon_days=7)
    
    assert len(forecasts) == 7
    for f in forecasts:
        assert f['p10'] <= f['p50'] <= f['p90']
        assert f['p10'] > 0
