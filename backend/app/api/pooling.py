from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.app.services.pooling import calculate_pool_savings

router = APIRouter()

class FarmerInput(BaseModel):
    name: str
    qty: float

class PoolRequest(BaseModel):
    farmers: List[FarmerInput]
    mandi: str
    vehicle_type: Optional[str] = "Auto"
    crop: Optional[str] = "tomato"

@router.post("/pool")
async def pool_endpoint(req: PoolRequest):
    try:
        farmers_dict = [{"name": f.name, "qty": f.qty} for f in req.farmers]
        result = calculate_pool_savings(farmers_dict, req.mandi, req.vehicle_type, req.crop)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
