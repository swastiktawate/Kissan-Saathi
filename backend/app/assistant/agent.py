import asyncio
import logging

from backend.app.assistant.guardrails import (
    enforce_trust_gate,
    numeric_consistency_check,
)
from backend.app.assistant.providers.gemini import GeminiProvider
from backend.app.assistant.providers.rule_based import RuleBasedProvider
from backend.app.assistant.tools import execute_tool
from backend.app.config import settings

logger = logging.getLogger(__name__)


async def run_agent(message: str, language: str = "en"):
    provider_name = settings.LLM_PROVIDER
    provider = RuleBasedProvider()
    llm_mode = "rule_based"

    if provider_name == "gemini":
        try:
            provider = GeminiProvider()
            llm_mode = "gemini"
            logger.info("Using GeminiProvider for this request")
        except Exception as e:
            logger.warning(f"GeminiProvider init failed ({type(e).__name__}: {e}), falling back to rule_based")
            provider = RuleBasedProvider()
            llm_mode = "rule_based"

    messages = [{"role": "user", "content": message}]
    tools_used = []
    evidence = []

    try:
        async with asyncio.timeout(45.0):
            for round_num in range(4):
                resp = await provider.chat(messages, tools=[], language=language)
                messages.append(resp)

                if resp.get("tool_calls"):
                    for tc in resp["tool_calls"]:
                        tools_used.append(tc["name"])
                        logger.info(f"Executing tool: {tc['name']} with args: {tc['arguments']}")
                        tr = await execute_tool(tc["name"], tc["arguments"])
                        evidence.append(tr)
                        messages.append({"role": "tool", "name": tc["name"], "content": tr})
                else:
                    break

    except asyncio.TimeoutError:
        logger.warning("Agent timed out after 15s, returning timeout response")
        llm_mode = "timeout_fallback"
        messages.append({"role": "assistant", "content": "The system took too long to respond. Please try again."})
    except Exception as e:
        logger.error(f"Agent error ({type(e).__name__}: {e}), falling back to rule_based")
        llm_mode = "rule_based"
        # Re-run with rule based
        try:
            provider = RuleBasedProvider()
            resp = await provider.chat([{"role": "user", "content": message}], tools=[], language=language)
            messages.append(resp)
            if resp.get("tool_calls"):
                for tc in resp["tool_calls"]:
                    tools_used.append(tc["name"])
                    tr = await execute_tool(tc["name"], tc["arguments"])
                    evidence.append(tr)
                    import json
                    try:
                        data = json.loads(tr)
                        summary = f"Rule-based recommendation: {data.get('action')}. The best option is {data.get('best_option', {}).get('mandi_id')}."
                        messages.append({"role": "assistant", "content": summary})
                    except:
                        messages.append({"role": "assistant", "content": "Tool data retrieved."})
        except Exception as e2:
            logger.error(f"Rule-based fallback also failed: {e2}")
            messages.append({"role": "assistant", "content": "Sorry, I could not process your request right now."})

    final_reply = messages[-1].get("content", "")

    if "INSUFFICIENT_DATA" in str(evidence):
        final_reply = "I do not have enough reliable recent data to make a strong recommendation. Please refer to local traders or wait for data to refresh."
    else:
        if not final_reply and tools_used:
            final_reply = "Based on the tool results, here is your recommendation."

        final_reply = numeric_consistency_check(final_reply, evidence)
        final_reply = enforce_trust_gate(final_reply, evidence)

    logger.info(f"Agent response: mode={llm_mode}, tools={tools_used}")

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
