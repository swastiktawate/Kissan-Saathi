from backend.app.assistant.providers.base import BaseProvider

class GeminiProvider(BaseProvider):
    async def chat(self, messages, tools):
        raise NotImplementedError("API keys unset or unavailable")
