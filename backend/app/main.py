from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import backtest, chat, health, meta, recommend, whatif, transcribe

app = FastAPI(title="Kisan Saathi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(meta.router, prefix="/api/v1")
app.include_router(recommend.router, prefix="/api/v1")
app.include_router(whatif.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(backtest.router, prefix="/api/v1")
app.include_router(transcribe.router, prefix="/api/v1")

from backend.app.api import negotiation, policy, pooling, voice, forecast
app.include_router(negotiation.router, prefix="/api/v1")
app.include_router(policy.router, prefix="/api/v1")
app.include_router(pooling.router, prefix="/api/v1")
app.include_router(voice.router, prefix="/api/v1/voice")
app.include_router(forecast.router, prefix="/api/v1/forecast")
