import os
import json
import pytest
from backend.app.schemas import (
    HealthResponse, PricesResponse, ForecastResponse, TrustResponse,
    CompareResponse, RecommendResponse, WhatIfResponse, RiskResponse,
    WeatherRiskResponse, PoolResponse, ChatResponse, BacktestResponse,
    PolicyEventsResponse
)

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures', 'api_examples')

SCHEMA_MAP = {
    'health.json': HealthResponse,
    'prices.json': PricesResponse,
    'forecast.json': ForecastResponse,
    'trust.json': TrustResponse,
    'compare.json': CompareResponse,
    'recommend.json': RecommendResponse,
    'recommend_insufficient.json': RecommendResponse,
    'whatif.json': WhatIfResponse,
    'risk.json': RiskResponse,
    'weather_risk.json': WeatherRiskResponse,
    'pool.json': PoolResponse,
    'chat.json': ChatResponse,
    'backtest.json': BacktestResponse,
    'policy_events.json': PolicyEventsResponse
}

def test_fixtures_validate_against_schemas():
    for filename, schema_cls in SCHEMA_MAP.items():
        filepath = os.path.join(FIXTURE_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # ensure _example is removed before validation if it causes issues,
        # but pydantic should ignore extra fields if configured or we can pop it.
        data.pop('_example', None)
        
        # This will raise ValidationError if invalid
        schema_cls(**data)
