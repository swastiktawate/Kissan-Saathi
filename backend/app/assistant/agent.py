import asyncio
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
