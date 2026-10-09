import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.whatif import run_whatif_scenario

router = APIRouter()

class WhatifRequest(BaseModel):
    base: dict
    scenario: dict

@router.post("/whatif")
async def whatif_endpoint(req: WhatifRequest):
    base_params = {
        "crop_id": req.base.get("crop"),
        "home_mandi_id": req.base.get("home_mandi"),
        "quantity_q": req.base.get("quantity_q", 50),
        "origin_date": datetime.date.today().isoformat(),
        "risk_setting": req.base.get("risk_setting", "balanced")
    }
    res = await run_whatif_scenario(base_params, req.scenario)
    return res
