from fastapi import APIRouter

from backend.app.services.backtest import run_backtest_simulation

router = APIRouter()

@router.get("/backtest")
async def backtest_endpoint(crop: str = "tomato", mandi: str = "vashi", days: int = 30):
    res = run_backtest_simulation(crop, mandi, days)
    return res
