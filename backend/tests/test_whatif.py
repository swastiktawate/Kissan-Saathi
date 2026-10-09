import pytest

from backend.app.services.whatif import run_whatif_scenario


@pytest.mark.asyncio
async def test_run_whatif():
    base = {"crop_id": "tomato", "home_mandi_id": "vashi", "quantity_q": 50, "origin_date": "2023-01-01"}
    scene = {"transport_multiplier": 1.2}
    
    res = await run_whatif_scenario(base, scene)
    assert "delta" in res
    assert "baseline" in res
    assert "scenario" in res
