from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def chat(self, messages, tools, language="en"):
        pass
