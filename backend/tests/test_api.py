from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_recommend_validation():
    # Quantity too large
    res = client.post("/api/v1/recommend", json={
        "crop": "tomato", "home_mandi": "vashi", "quantity_q": 50000, "horizon_days": 7, "risk_setting": "balanced"
    })
    assert res.status_code == 422
