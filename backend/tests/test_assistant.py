import pytest

from backend.app.assistant.agent import run_agent
from backend.app.assistant.guardrails import numeric_consistency_check


@pytest.mark.asyncio
async def test_rule_based_fallback():
    res = await run_agent("Should I sell my tomatoes today or wait three days? 50 quintal Vashi")
    assert res["meta"]["llm_mode"] == "rule_based"
    assert "recommend" in res["tools_used"]
    assert len(res["evidence"]) > 0

def test_numeric_consistency():
    draft = "The expected gain is 999 Rs."
    tools = ['{"gain": 50}']
    out = numeric_consistency_check(draft, tools)
    assert "cannot safely confirm those numbers" in out
    
    draft_valid = "The expected gain is 50 Rs."
    out_valid = numeric_consistency_check(draft_valid, tools)
    assert out_valid == draft_valid
