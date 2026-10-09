from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import health, meta, recommend, whatif, chat, backtest
from backend.app.config import settings

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
