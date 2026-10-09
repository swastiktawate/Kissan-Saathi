import pytest
from unittest.mock import patch
from backend.app.ingestion.orchestrator import orchestrate_ingestion
from backend.app.config import settings

@pytest.mark.asyncio
@patch('backend.app.ingestion.orchestrator.fetch_datagov_prices')
async def test_orchestrator_live(mock_fetch):
    mock_fetch.return_value = {"status": "ok", "rows": [{"price": 100}], "fetched_at": "now"}
    settings.DATA_MODE = "auto"
    
    result = await orchestrate_ingestion("State", "Market", "Crop")
    assert result["mode"] == "live"
    assert len(result["rows_raw"]) == 1

@pytest.mark.asyncio
@patch('backend.app.ingestion.orchestrator.fetch_datagov_prices')
async def test_orchestrator_synthetic_fallback(mock_fetch):
    mock_fetch.return_value = {"status": "failed", "error": "mock error"}
    settings.DATA_MODE = "auto"
    
    result = await orchestrate_ingestion("State", "Market", "Crop")
    assert result["mode"] in ["synthetic", "cached"]
