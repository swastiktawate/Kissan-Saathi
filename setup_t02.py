import os
import json

os.makedirs('backend/app/schemas', exist_ok=True)
os.makedirs('backend/tests/fixtures/api_examples', exist_ok=True)

with open('backend/app/config.py', 'w') as f:
    f.write('''from pydantic_settings import BaseSettings
from typing import Literal

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
''')

with open('.env.example', 'w') as f:
    f.write('''DATA_GOV_API_KEY=
DATA_GOV_RESOURCE_ID=
DATA_MODE=auto
DUCKDB_PATH=data/kisan.duckdb
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1
OSRM_BASE_URL=https://router.project-osrm.org
USE_LIVE_OSRM=false
BHASHINI_API_KEY=
BHASHINI_USER_ID=
LLM_PROVIDER=gemini
LLM_MODEL=
LLM_FALLBACK_PROVIDER=rule_based
GEMINI_API_KEY=
GROQ_API_KEY=
LLM_TIMEOUT_SECONDS=15
CORS_ORIGINS=http://localhost:5173
RATE_LIMIT_CHAT_PER_MIN=20
LOG_LEVEL=INFO
''')

with open('backend/app/schemas/__init__.py', 'w') as f:
    f.write('''from enum import Enum
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field

class DataOrigin(str, Enum):
    live = "live"
    cached = "cached"
    sample = "sample"
    synthetic = "synthetic"
    user_input = "user_input"

class Action(str, Enum):
    SELL_NOW = "SELL_NOW"
    WAIT_N_DAYS = "WAIT_N_DAYS"
    ANOTHER_MANDI = "ANOTHER_MANDI"
    SPLIT_SALE = "SPLIT_SALE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"

class Severity(str, Enum):
    info = "info"
    warn = "warn"
    high = "high"

class RiskSetting(str, Enum):
    cautious = "cautious"
    balanced = "balanced"
    aggressive = "aggressive"

class DataMode(str, Enum):
    live = "live"
    cached = "cached"
    sample = "sample"
    synthetic = "synthetic"
    mixed = "mixed"

class SourceMeta(BaseModel):
    name: str
    origin: str
    fetched_at: str

class TrustMeta(BaseModel):
    score: float
    label: str
    calibrated: bool

class Meta(BaseModel):
    data_mode: str
    as_of: str
    latest_observation_date: str
    sources: List[SourceMeta]
    trust: TrustMeta
    warnings: List[str]
    llm_mode: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    db: str
    sources: Dict[str, str]
    data_mode: str

class MetaResponse(BaseModel):
    meta: Meta

class PriceObservation(BaseModel):
    date: str
    crop_id: str
    mandi_id: str
    min_price: float
    modal_price: float
    max_price: float
    arrivals_quintals: Optional[float]
    data_origin: str

class PricesResponse(BaseModel):
    observations: List[PriceObservation]
    meta: Meta

class ForecastPoint(BaseModel):
    date: str
    horizon: int
    p10: float
    p50: float
    p90: float

class ForecastResponse(BaseModel):
    forecasts: List[ForecastPoint]
    method: str
    calibrated: bool
    diagnostics: Optional[Dict[str, Any]]
    meta: Meta

class TrustResponse(BaseModel):
    score: float
    label: str
    components: Dict[str, float]
    reasons: List[str]
    meta: Meta

class CompareOption(BaseModel):
    mandi: str
    day: int
    price: float
    transport: float
    spoilage: float
    commission: float
    storage: float
    nr_p10: float
    nr_p50: float
    nr_p90: float
    distance: float
    distance_method: str
    is_best: bool

class CompareResponse(BaseModel):
    options: List[CompareOption]
    meta: Meta

class Reason(BaseModel):
    key: str
    params: Dict[str, Any]

class RiskFlag(BaseModel):
    code: str
    severity: str
    evidence: Dict[str, Any]

class RecommendResponse(BaseModel):
    action: str
    headline_key: str
    params: Dict[str, Any]
    confidence: str
    expected_gain_per_q: Dict[str, float]
    expected_total: Dict[str, Any]
    reference: Dict[str, Any]
    best: Dict[str, Any]
    split_plan: Optional[Dict[str, Any]]
    cost_of_waiting: List[Dict[str, Any]]
    drivers: Dict[str, float]
    reasons: List[Reason]
    flags: List[RiskFlag]
    assumptions: List[str]
    meta: Meta

class WhatIfRequestScenario(BaseModel):
    transport_multiplier: Optional[float] = 1.0
    arrivals_change_pct: Optional[float] = 0.0
    price_shock_pct: Optional[float] = 0.0
    applies_to: Optional[str] = "future"
    quantity_q: Optional[float] = None
    risk_setting: Optional[str] = None

class RecommendRequest(BaseModel):
    crop: str = Field(..., min_length=1)
    quantity_q: float = Field(..., ge=0.1, le=10000.0)
    home_mandi: str = Field(..., min_length=1)
    horizon_days: int = Field(..., ge=1, le=7)
    risk_setting: RiskSetting

class WhatIfRequest(BaseModel):
    base: RecommendRequest
    scenario: WhatIfRequestScenario

class WhatIfResponse(BaseModel):
    baseline: RecommendResponse
    scenario: RecommendResponse
    delta: Dict[str, Any]
    assumptions: List[str]
    meta: Meta

class RiskResponse(BaseModel):
    flags: List[RiskFlag]
    radar: Dict[str, Any]
    meta: Meta

class WeatherRiskResponse(BaseModel):
    daily_precip: List[Dict[str, Any]]
    flag: Optional[RiskFlag]
    meta: Meta

class FarmerInput(BaseModel):
    qty_q: float

class PoolRequest(BaseModel):
    mandi: str
    crop: str
    farmers: List[FarmerInput]
    vehicle: Optional[str] = None

class PoolResponse(BaseModel):
    shares: List[Dict[str, Any]]
    saving: float
    meta: Meta

class ChatRequest(BaseModel):
    message: str
    language: str
    session_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    language: str
    tools_used: List[str]
    evidence: Dict[str, Any]
    suggested_actions: List[str]
    meta: Meta

class BacktestResponse(BaseModel):
    metrics: Dict[str, Any]
    caveats: List[str]
    data_origin_summary: str
    meta: Meta

class PolicyEventsResponse(BaseModel):
    connected: bool
    events: Optional[List[Dict[str, Any]]] = None
    meta: Meta

class ErrorDetail(BaseModel):
    code: str
    message_key: str
    details: str

class ErrorResponse(BaseModel):
    error: ErrorDetail
''')

with open('backend/app/logging_conf.py', 'w') as f:
    f.write('''import logging
import sys

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(ch)
''')
