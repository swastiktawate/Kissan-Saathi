import re

from backend.app.assistant.providers.base import BaseProvider


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
