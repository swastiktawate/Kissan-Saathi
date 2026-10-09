from backend.app.assistant.providers.base import BaseProvider


class GroqProvider(BaseProvider):
    async def chat(self, messages, tools):
        raise NotImplementedError("API keys unset or unavailable")
