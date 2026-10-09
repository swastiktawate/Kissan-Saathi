import json
import logging

import google.generativeai as genai

from backend.app.assistant.providers.base import BaseProvider
from backend.app.config import settings

logger = logging.getLogger(__name__)


class GeminiProvider(BaseProvider):
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-flash-lite-latest")
        logger.info("GeminiProvider initialized with model=gemini-flash-lite-latest")

    async def chat(self, messages, tools):
        """Send messages to Gemini and return structured response."""
        try:
            # Build conversation for Gemini
            system_prompt = (
                "You are Kisan Sathi, a helpful agricultural assistant for Indian farmers. "
                "You help farmers decide when and where to sell their crops. "
                "Always answer in a friendly, concise way. "
                "When asked about prices or selling, use the available tools. "
                "Always ground your answers in the tool results. Never fabricate numbers."
            )

            # Convert messages to Gemini format
            gemini_messages = []
            for m in messages:
                role = "user" if m.get("role") == "user" else "model"
                content = m.get("content", "")
                if content:
                    gemini_messages.append({"role": role, "parts": [content]})

            if not gemini_messages:
                return {"role": "assistant", "content": "", "tool_calls": []}

            # Check if this is a farming/price query from the user that needs tools
            is_user = messages and messages[-1].get("role") == "user"
            last_msg = messages[-1].get("content", "").lower() if is_user else ""
            needs_tools = is_user and any(kw in last_msg for kw in [
                "sell", "price", "mandi", "wait", "tomato", "onion",
                "tamatar", "pyaaz", "bechna", "kab", "kaha", "recommend",
                "forecast", "weather", "cost", "transport"
            ])

            if needs_tools:
                crop = "tomato"
                if any(k in last_msg for k in ["onion", "pyaaz"]):
                    crop = "onion"
                elif any(k in last_msg for k in ["potato", "aloo"]):
                    crop = "potato"
                elif any(k in last_msg for k in ["banana", "kela"]):
                    crop = "banana"
                    
                # Return a tool call for the recommend endpoint
                return {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{
                        "name": "recommend",
                        "arguments": {
                            "crop": crop,
                            "home_mandi": "vashi",
                            "quantity_q": 50,
                            "horizon_days": 7
                        }
                    }]
                }

            # If there is tool history, summarize it
            context_str = ""
            for m in messages:
                if m.get("role") == "tool":
                    context_str += f"\nData: {m.get('content')}"
                    
            prompt = system_prompt
            if context_str:
                prompt += f"\n\nHere is the data you requested. Summarize this nicely for the farmer in their language:\n{context_str}"
                
            prompt += f"\n\nUser: {gemini_messages[0]['parts'][0]}"

            # For general questions or summarization, use Gemini directly
            chat = self.model.start_chat(history=[])
            
            import asyncio
            response = await asyncio.to_thread(
                chat.send_message,
                prompt
            )

            return {
                "role": "assistant",
                "content": response.text,
                "tool_calls": []
            }

        except Exception as e:
            logger.error(f"GeminiProvider.chat failed: {type(e).__name__}: {e}")
            raise
