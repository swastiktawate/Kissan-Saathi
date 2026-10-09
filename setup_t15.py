import os

os.makedirs('backend/app/api', exist_ok=True)

with open('backend/app/api/health.py', 'w') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter()
@router.get("/health")
def health():
    return {"status": "ok", "dependencies": {"db": "ok"}}
''')

with open('backend/app/api/meta.py', 'w') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter()
@router.get("/meta")
def get_meta():
    return {"supported_crops": ["tomato", "onion", "potato"], "risk_settings": ["cautious", "balanced", "aggressive"]}
''')

with open('backend/app/api/recommend.py', 'w') as f:
    f.write('''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import datetime
from backend.app.services.recommend import recommend_action
from backend.app.services.cost_of_waiting import calculate_cost_of_waiting
from backend.app.config import settings

router = APIRouter()

class RecommendRequest(BaseModel):
    crop: str
    home_mandi: str
    quantity_q: float = Field(..., ge=0.1, le=10000)
    horizon_days: int = Field(7, ge=1, le=7)
    risk_setting: str = "balanced"

@router.post("/recommend")
def recommend_endpoint(req: RecommendRequest):
    origin = datetime.date.today().isoformat()
    try:
        rec = recommend_action(req.crop, req.home_mandi, req.quantity_q, origin, req.risk_setting, req.horizon_days)
        cow = calculate_cost_of_waiting(rec["all_results"], req.home_mandi)
        
        return {
            "meta": {
                "data_mode": settings.DATA_MODE,
                "trust": "High"
            },
            "action": rec["action"],
            "expected_gain_per_q": rec["best_option"]["nr_p50"] - rec["reference_option"]["nr_p50"] if "nr_p50" in rec["best_option"] else 0,
            "cost_of_waiting": cow,
            "drivers": rec["best_option"].get("nr_scenarios", {}).get("p50", {}).get("drivers", {}) if "nr_scenarios" in rec["best_option"] else {},
            "reasons": rec["reasons"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
''')

with open('backend/app/api/whatif.py', 'w') as f:
    f.write('''from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.whatif import run_whatif_scenario
import datetime

router = APIRouter()

class WhatifRequest(BaseModel):
    base: dict
    scenario: dict

@router.post("/whatif")
def whatif_endpoint(req: WhatifRequest):
    base_params = {
        "crop_id": req.base.get("crop"),
        "home_mandi_id": req.base.get("home_mandi"),
        "quantity_q": req.base.get("quantity_q", 50),
        "origin_date": datetime.date.today().isoformat(),
        "risk_setting": req.base.get("risk_setting", "balanced")
    }
    res = run_whatif_scenario(base_params, req.scenario)
    return res
''')

with open('backend/app/main.py', 'w') as f:
    f.write('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import health, meta, recommend, whatif
from backend.app.config import settings

app = FastAPI(title="Kisan Saathi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(meta.router, prefix="/api/v1")
app.include_router(recommend.router, prefix="/api/v1")
app.include_router(whatif.router, prefix="/api/v1")
''')

with open('backend/tests/test_api.py', 'w') as f:
    f.write('''from fastapi.testclient import TestClient
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
''')
