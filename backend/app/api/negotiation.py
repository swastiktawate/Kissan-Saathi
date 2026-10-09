from fastapi import APIRouter, HTTPException, Query
from backend.app.services.negotiation import get_fair_price, get_regret_analysis

router = APIRouter()

@router.get("/fair-price")
async def fair_price_endpoint(
    crop: str = Query(..., description="Crop ID"),
    mandi: str = Query(..., description="Mandi ID")
):
    try:
        result = get_fair_price(crop, mandi)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regret-analysis")
async def regret_analysis_endpoint(
    crop: str = Query(..., description="Crop ID"),
    mandi: str = Query(..., description="Mandi ID"),
    quantity: float = Query(..., description="Quantity sold in quintals", gt=0),
    sold_date: str = Query(..., description="Date crop was sold (YYYY-MM-DD)")
):
    try:
        result = get_regret_analysis(crop, mandi, quantity, sold_date)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
