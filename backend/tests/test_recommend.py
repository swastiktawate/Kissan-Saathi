import pytest
from backend.app.services.recommend import recommend_action

@pytest.mark.asyncio
async def test_recommend_action_insufficient_trust():
    res = await recommend_action("tomato", "vashi", 50, "2023-01-01", trust_label="Insufficient")
    assert res["action"] == "INSUFFICIENT_DATA"

@pytest.mark.asyncio
async def test_recommend_action_sell_now():
    # Force sell now by setting aggressive risk to trigger the margin check (margin won't be beaten if all forecasts flat)
    res = await recommend_action("tomato", "vashi", 50, "2023-01-01", risk_setting="aggressive")
    assert "action" in res
    assert res["margin_applied"] >= 25.0
