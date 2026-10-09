import pytest

from backend.app.services.compare import compare_mandis


@pytest.mark.asyncio
async def test_compare_mandis():
    res = await compare_mandis("tomato", "vashi", 50, "2023-01-01", 2)
    assert "results" in res
    assert res["reference_mandi"] == "vashi"
    assert len(res["results"]) > 0
    assert "nr_p50" in res["results"][0]
