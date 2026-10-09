from unittest.mock import patch

import pytest

from backend.app.config import settings
from backend.app.ingestion.routing import get_distance


@pytest.mark.asyncio
@patch('backend.app.ingestion.routing.fetch_osrm_distance')
async def test_get_distance_fallback(mock_osrm):
    mock_osrm.side_effect = Exception("Network error")
    settings.USE_LIVE_OSRM = True
    
    res = await get_distance("pune", "vashi")
    
    assert res["status"] == "ok"
    assert res["method"] == "estimated"
    assert "Using estimated distance" in res["warnings"] or any("OSRM failed" in w for w in res["warnings"])
