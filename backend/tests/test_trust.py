import pytest
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
