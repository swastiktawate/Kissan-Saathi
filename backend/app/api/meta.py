from fastapi import APIRouter
router = APIRouter()
@router.get("/meta")
def get_meta():
    return {"supported_crops": ["tomato", "onion", "potato"], "risk_settings": ["cautious", "balanced", "aggressive"]}
