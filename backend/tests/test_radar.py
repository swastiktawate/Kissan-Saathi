import pytest
from backend.app.services.radar import check_price_wave_radar

def test_radar():
    neighbors = [{"id": "n1", "price": 80, "historical_corr": 0.8}]
    res = check_price_wave_radar("vashi", neighbors, 100)
    
    assert len(res["radar_alerts"]) == 1
    assert res["radar_alerts"][0]["neighbor"] == "n1"
    assert res["radar_alerts"][0]["price_diff_pct"] == -0.20
