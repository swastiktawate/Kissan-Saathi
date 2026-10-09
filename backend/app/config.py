from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATA_GOV_API_KEY: str = ""
    DATA_GOV_RESOURCE_ID: str = ""
    DATA_MODE: Literal["auto", "sample", "synthetic"] = "auto"
    DUCKDB_PATH: str = "data/kisan.duckdb"

    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    OSRM_BASE_URL: str = "https://router.project-osrm.org"
    USE_LIVE_OSRM: bool = False
    
    BHASHINI_API_KEY: str = ""
    BHASHINI_USER_ID: str = ""

    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = ""
    LLM_FALLBACK_PROVIDER: str = "rule_based"
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    LLM_TIMEOUT_SECONDS: int = 15

    CORS_ORIGINS: str = "http://localhost:5173"
    RATE_LIMIT_CHAT_PER_MIN: int = 20
    LOG_LEVEL: str = "INFO"

    # Tunable thresholds
    TRUST_THRESHOLD_HIGH: int = 70
    TRUST_THRESHOLD_MEDIUM: int = 40
    
    RISK_PRICE_DROP_WARN_PCT: float = 5.0
    RISK_PRICE_DROP_HIGH_PCT: float = 10.0
    RISK_ARRIVAL_SURGE_WARN_MULT: float = 1.3
    RISK_ARRIVAL_SURGE_HIGH_MULT: float = 1.6
    RISK_VOLATILITY_WARN_CV: float = 0.15
    RISK_VOLATILITY_HIGH_CV: float = 0.25
    RISK_STALE_WARN_DAYS: int = 2
    RISK_STALE_HIGH_DAYS: int = 4
    RISK_WEAK_FORECAST_WIDTH_PCT: float = 0.35
    RISK_HEAVY_RAIN_MM: float = 30.0

    LAMBDA_CAUTIOUS: float = 1.0
    LAMBDA_BALANCED: float = 0.5
    LAMBDA_AGGRESSIVE: float = 0.0

    MATERIALITY_MARGIN_MIN_RS: float = 25.0
    MATERIALITY_MARGIN_PCT: float = 0.015
    
    EWMA_ALPHA: float = 0.5
    TREND_DAMPING: float = 0.8
    MIN_RESIDUALS_FOR_EMPIRICAL_BAND: int = 30
    
    QTY_MIN_Q: float = 0.1
    QTY_MAX_Q: float = 10000.0
    HORIZON_MIN_DAYS: int = 1
    HORIZON_MAX_DAYS: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

settings = Settings()
