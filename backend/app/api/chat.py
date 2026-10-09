from fastapi import APIRouter
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
