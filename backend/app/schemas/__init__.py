from enum import Enum
from typing import Any, Dict, List, Optional, Union

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
    sources: list[SourceMeta]
    trust: TrustMeta
    warnings: list[str]
    llm_mode: str | None = None

class HealthResponse(BaseModel):
    status: str
    db: str
    sources: dict[str, str]
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
    arrivals_quintals: float | None
    data_origin: str

class PricesResponse(BaseModel):
    observations: list[PriceObservation]
    meta: Meta

class ForecastPoint(BaseModel):
    date: str
    horizon: int
    p10: float
    p50: float
    p90: float

class ForecastResponse(BaseModel):
    forecasts: list[ForecastPoint]
    method: str
    calibrated: bool
    diagnostics: dict[str, Any] | None
    meta: Meta

class TrustResponse(BaseModel):
    score: float
    label: str
    components: dict[str, float]
    reasons: list[str]
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
    options: list[CompareOption]
    meta: Meta

class Reason(BaseModel):
    key: str
    params: dict[str, Any]

class RiskFlag(BaseModel):
    code: str
    severity: str
    evidence: dict[str, Any]

class RecommendResponse(BaseModel):
    action: str
    headline_key: str
    params: dict[str, Any]
    confidence: str
    expected_gain_per_q: dict[str, float]
    expected_total: dict[str, Any]
    reference: dict[str, Any]
    best: dict[str, Any]
    split_plan: dict[str, Any] | None
    cost_of_waiting: list[dict[str, Any]]
    drivers: dict[str, float]
    reasons: list[Reason]
    flags: list[RiskFlag]
    assumptions: list[str]
    meta: Meta

class WhatIfRequestScenario(BaseModel):
    transport_multiplier: float | None = 1.0
    arrivals_change_pct: float | None = 0.0
    price_shock_pct: float | None = 0.0
    applies_to: str | None = "future"
    quantity_q: float | None = None
    risk_setting: str | None = None

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
    delta: dict[str, Any]
    assumptions: list[str]
    meta: Meta

class RiskResponse(BaseModel):
    flags: list[RiskFlag]
    radar: dict[str, Any]
    meta: Meta

class WeatherRiskResponse(BaseModel):
    daily_precip: list[dict[str, Any]]
    flag: RiskFlag | None
    meta: Meta

class FarmerInput(BaseModel):
    qty_q: float

class PoolRequest(BaseModel):
    mandi: str
    crop: str
    farmers: list[FarmerInput]
    vehicle: str | None = None

class PoolResponse(BaseModel):
    shares: list[dict[str, Any]]
    saving: float
    meta: Meta

class ChatRequest(BaseModel):
    message: str
    language: str
    session_context: dict[str, Any] | None = None

class ChatResponse(BaseModel):
    reply: str
    language: str
    tools_used: list[str]
    evidence: dict[str, Any]
    suggested_actions: list[str]
    meta: Meta

class BacktestResponse(BaseModel):
    metrics: dict[str, Any]
    caveats: list[str]
    data_origin_summary: str
    meta: Meta

class PolicyEventsResponse(BaseModel):
    connected: bool
    events: list[dict[str, Any]] | None = None
    meta: Meta

class ErrorDetail(BaseModel):
    code: str
    message_key: str
    details: str

class ErrorResponse(BaseModel):
    error: ErrorDetail
