import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.config import settings
from backend.app.services.cost_of_waiting import calculate_cost_of_waiting
from backend.app.services.recommend import recommend_action

router = APIRouter()

class RecommendRequest(BaseModel):
    crop: str
    home_mandi: str
    quantity_q: float = Field(..., ge=0.1, le=10000)
    horizon_days: int = Field(7, ge=1, le=7)
    risk_setting: str = "balanced"

@router.post("/recommend")
async def recommend_endpoint(req: RecommendRequest):
    origin = datetime.date.today().isoformat()
    try:
        rec = await recommend_action(req.crop, req.home_mandi, req.quantity_q, origin, req.risk_setting, req.horizon_days)
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
