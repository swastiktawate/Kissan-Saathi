import pytest
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
