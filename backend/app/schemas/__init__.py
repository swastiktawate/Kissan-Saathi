from enum import Enum
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
