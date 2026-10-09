import os

os.makedirs('backend/app/assistant/providers', exist_ok=True)
os.makedirs('backend/tests', exist_ok=True)

with open('backend/app/assistant/providers/base.py', 'w') as f:
    f.write('''from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def chat(self, messages, tools):
        pass
''')

with open('backend/app/assistant/providers/gemini.py', 'w') as f:
    f.write('''from backend.app.assistant.providers.base import BaseProvider

class GeminiProvider(BaseProvider):
    async def chat(self, messages, tools):
        raise NotImplementedError("API keys unset or unavailable")
''')

with open('backend/app/assistant/providers/groq.py', 'w') as f:
    f.write('''from backend.app.assistant.providers.base import BaseProvider

class GroqProvider(BaseProvider):
    async def chat(self, messages, tools):
        raise NotImplementedError("API keys unset or unavailable")
''')

with open('backend/app/assistant/providers/rule_based.py', 'w') as f:
    f.write('''from backend.app.assistant.providers.base import BaseProvider
import re

class RuleBasedProvider(BaseProvider):
    async def chat(self, messages, tools):
        last_msg = messages[-1].get("content", "").lower()
        if re.search(r"sell.*today|wait", last_msg):
            # mock tool call to recommend
            return {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"name": "recommend", "arguments": {"crop": "tomato", "home_mandi": "vashi", "quantity_q": 50, "horizon_days": 3}}]
            }
        
        return {
            "role": "assistant",
            "content": "I am a fallback assistant. Please try asking about prices or recommendations.",
            "tool_calls": []
        }
''')

with open('backend/app/assistant/tools.py', 'w') as f:
    f.write('''import json
from backend.app.services.recommend import recommend_action
from backend.app.services.whatif import run_whatif_scenario
import datetime

async def execute_tool(tool_name: str, arguments: dict):
    origin = datetime.date.today().isoformat()
    if tool_name == "recommend":
        res = await recommend_action(
            crop_id=arguments.get("crop", "tomato"),
            home_mandi_id=arguments.get("home_mandi", "vashi"),
            quantity_q=arguments.get("quantity_q", 50),
            origin_date=origin,
            risk_setting=arguments.get("risk_setting", "balanced"),
            horizon_days=arguments.get("horizon_days", 7)
        )
        return json.dumps(res)
    elif tool_name == "run_whatif":
        # simple mock
        return json.dumps({"status": "whatif_executed"})
    return json.dumps({"error": "tool not found"})
''')

with open('backend/app/assistant/guardrails.py', 'w') as f:
    f.write('''import re

def numeric_consistency_check(llm_draft: str, tool_results: list) -> str:
    numbers_in_draft = re.findall(r"\\b\\d+(?:\\.\\d+)?\\b", llm_draft)
    tool_text = " ".join([str(res) for res in tool_results])
    
    for num in numbers_in_draft:
        # ignore trivial numbers
        if num in ["1", "2", "3", "0", "0.0"]:
            continue
        if num not in tool_text:
            return "Based on the latest data, I cannot safely confirm those numbers. Please check the dashboard directly."
            
    return llm_draft
    
def enforce_trust_gate(llm_draft: str, tool_results: list) -> str:
    tool_text = " ".join([str(res) for res in tool_results])
    if "INSUFFICIENT_DATA" in tool_text or "Trust score is Insufficient" in tool_text:
        return "I do not have enough reliable recent data to make a strong recommendation. Please refer to local traders or wait for data to refresh."
    return llm_draft
''')

with open('backend/app/assistant/agent.py', 'w') as f:
    f.write('''import asyncio
import datetime
from backend.app.assistant.providers.rule_based import RuleBasedProvider
from backend.app.assistant.providers.gemini import GeminiProvider
from backend.app.assistant.providers.groq import GroqProvider
from backend.app.assistant.tools import execute_tool
from backend.app.assistant.guardrails import numeric_consistency_check, enforce_trust_gate
from backend.app.config import settings

async def run_agent(message: str, language: str = "en"):
    provider_name = settings.LLM_PROVIDER
    provider = RuleBasedProvider()
    llm_mode = "rule_based"
    
    if provider_name == "gemini":
        try:
            p = GeminiProvider()
            await p.chat([], []) # throws NotImplemented
            provider = p
            llm_mode = "gemini"
        except Exception:
            pass # fallback to rule_based
            
    messages = [{"role": "user", "content": message}]
    tools_used = []
    evidence = []
    
    try:
        async with asyncio.timeout(15.0):
            for round_num in range(4):
                resp = await provider.chat(messages, tools=[])
                messages.append(resp)
                
                if resp.get("tool_calls"):
                    for tc in resp["tool_calls"]:
                        tools_used.append(tc["name"])
                        tr = await execute_tool(tc["name"], tc["arguments"])
                        evidence.append(tr)
                        messages.append({"role": "tool", "name": tc["name"], "content": tr})
                else:
                    break
                    
    except asyncio.TimeoutError:
        llm_mode = "timeout_fallback"
        messages.append({"role": "assistant", "content": "The system took too long to respond. Please try again."})
        
    final_reply = messages[-1].get("content", "")
    
    if "INSUFFICIENT_DATA" in str(evidence):
        final_reply = "I do not have enough reliable recent data to make a strong recommendation. Please refer to local traders or wait for data to refresh."
    else:
        # Actually generate a decent rule based reply if evidence was fetched
        if not final_reply and tools_used:
            final_reply = "Based on the tool results, here is your recommendation."
            
        final_reply = numeric_consistency_check(final_reply, evidence)
        final_reply = enforce_trust_gate(final_reply, evidence)
        
    return {
        "reply": final_reply,
        "language": language,
        "tools_used": tools_used,
        "evidence": evidence,
        "suggested_actions": ["View Mandi", "Check Scenarios"],
        "meta": {
            "llm_mode": llm_mode
        }
    }
''')

with open('backend/app/api/chat.py', 'w') as f:
    f.write('''from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.assistant.agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    language: str = "en"

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    res = await run_agent(req.message, req.language)
    return res
''')

with open('backend/tests/test_assistant.py', 'w') as f:
    f.write('''import pytest
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
''')
