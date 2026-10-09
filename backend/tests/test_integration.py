"""Integration tests with failure injection for API fallbacks."""
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_recommend_endpoint_returns_200():
    """Full recommend call must never 500."""
    res = client.post("/api/v1/recommend", json={
        "crop": "tomato", "home_mandi": "vashi",
        "quantity_q": 50, "horizon_days": 7, "risk_setting": "balanced"
    })
    assert res.status_code == 200
    body = res.json()
    assert "action" in body


def test_chat_endpoint_rule_based():
    """With LLM keys unset, chat must return rule_based mode, never 500."""
    res = client.post("/api/v1/chat", json={
        "message": "Should I sell my tomatoes today?",
        "language": "en"
    })
    assert res.status_code == 200
    body = res.json()
    assert body["meta"]["llm_mode"] == "rule_based"


def test_whatif_endpoint_returns_200():
    res = client.post("/api/v1/whatif", json={
        "base": {"crop": "tomato", "home_mandi": "vashi", "quantity_q": 50,
                 "risk_setting": "balanced"},
        "scenario": {"transport_multiplier": 1.3}
    })
    assert res.status_code == 200
    body = res.json()
    assert "delta" in body


def test_backtest_endpoint():
    res = client.get("/api/v1/backtest?crop=tomato&mandi=vashi&days=30")
    assert res.status_code == 200
    body = res.json()
    assert "synthetic" in body["data_origin_summary"]


def test_health_reports_ok():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
