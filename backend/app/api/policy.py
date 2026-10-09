from fastapi import APIRouter, HTTPException
from backend.app.services.policy import get_policy_alerts

router = APIRouter()

@router.get("/policy-alerts")
async def policy_alerts_endpoint():
    try:
        alerts = get_policy_alerts()
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
