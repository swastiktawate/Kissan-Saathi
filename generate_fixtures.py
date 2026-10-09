import json
import os
from backend.app.schemas import (
    HealthResponse, MetaResponse, PricesResponse, ForecastResponse,
    TrustResponse, CompareResponse, RecommendResponse, WhatIfResponse,
    RiskResponse, WeatherRiskResponse, PoolResponse, ChatResponse,
    BacktestResponse, PolicyEventsResponse, Meta, SourceMeta, TrustMeta
)

os.makedirs('backend/tests/fixtures/api_examples', exist_ok=True)

meta = Meta(
    data_mode="sample",
    as_of="2026-10-09T08:30:00+05:30",
    latest_observation_date="2026-10-08",
    sources=[SourceMeta(name="data.gov.in", origin="cached", fetched_at="2026-10-08T20:00:00Z")],
    trust=TrustMeta(score=72, label="High", calibrated=False),
    warnings=[],
    llm_mode="rule_based"
)

health = HealthResponse(
    status="ok",
    db="ok",
    sources={"datagov": "ok", "weather": "ok", "osrm": "unconfigured", "llm": "unconfigured"},
    data_mode="sample"
)
with open('backend/tests/fixtures/api_examples/health.json', 'w') as f:
    d = health.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

prices = PricesResponse(
    observations=[
        {"date": "2026-10-08", "crop_id": "tomato", "mandi_id": "Vashi", "min_price": 1800, "modal_price": 2000, "max_price": 2200, "arrivals_quintals": 500, "data_origin": "sample"}
    ],
    meta=meta
)
with open('backend/tests/fixtures/api_examples/prices.json', 'w') as f:
    d = prices.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

forecast = ForecastResponse(
    forecasts=[
        {"date": "2026-10-09", "horizon": 1, "p10": 1900, "p50": 2050, "p90": 2200}
    ],
    method="baseline_ewma_damped_trend",
    calibrated=False,
    diagnostics={"mae": 100},
    meta=meta
)
with open('backend/tests/fixtures/api_examples/forecast.json', 'w') as f:
    d = forecast.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

trust = TrustResponse(
    score=72.0,
    label="High",
    components={"freshness": 30.0, "completeness": 25.0},
    reasons=["Fresh data"],
    meta=meta
)
with open('backend/tests/fixtures/api_examples/trust.json', 'w') as f:
    d = trust.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

compare = CompareResponse(
    options=[
        {"mandi": "Vashi", "day": 0, "price": 2000.0, "transport": 100.0, "spoilage": 0.05, "commission": 100.0, "storage": 0.0, "nr_p10": 1700.0, "nr_p50": 1800.0, "nr_p90": 1900.0, "distance": 25.0, "distance_method": "estimated", "is_best": True}
    ],
    meta=meta
)
with open('backend/tests/fixtures/api_examples/compare.json', 'w') as f:
    d = compare.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

recommend = RecommendResponse(
    action="WAIT_N_DAYS",
    headline_key="rec.wait_n_days",
    params={"days": 3, "mandi": "Vashi"},
    confidence="Moderate",
    expected_gain_per_q={"p10": 120.0, "p50": 420.0, "p90": 690.0},
    expected_total={"p50": 21000.0, "unit": "INR"},
    reference={"mandi": "Vashi", "day": 0, "nr_p50": 1920.0},
    best={"mandi": "Vashi", "day": 3, "nr_p10": 1800.0, "nr_p50": 2340.0, "nr_p90": 2500.0},
    split_plan=None,
    cost_of_waiting=[{"day": 0, "gain_p50": 0.0, "gain_p10": 0.0, "gain_p90": 0.0}, {"day": 3, "gain_p50": 420.0}],
    drivers={"price_effect": 500.0, "spoilage": -50.0, "storage": -10.0, "transport": 0.0, "commission": -20.0},
    reasons=[{"key": "reason.price_up", "params": {"pct": 8}}],
    flags=[{"code": "ARRIVAL_SURGE", "severity": "warn", "evidence": {}}],
    assumptions=["Spoilage parameters are default estimates"],
    meta=meta
)
with open('backend/tests/fixtures/api_examples/recommend.json', 'w') as f:
    d = recommend.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

recommend_insufficient = RecommendResponse(
    action="INSUFFICIENT_DATA",
    headline_key="rec.insufficient",
    params={},
    confidence="Insufficient",
    expected_gain_per_q={"p10": 0.0, "p50": 0.0, "p90": 0.0},
    expected_total={"p50": 0.0, "unit": "INR"},
    reference={"mandi": "Vashi", "day": 0, "nr_p50": 0.0},
    best={"mandi": "Vashi", "day": 0, "nr_p10": 0.0, "nr_p50": 0.0, "nr_p90": 0.0},
    split_plan=None,
    cost_of_waiting=[],
    drivers={"price_effect": 0.0, "spoilage": 0.0, "storage": 0.0, "transport": 0.0, "commission": 0.0},
    reasons=[{"key": "reason.stale", "params": {"days": 6}}],
    flags=[],
    assumptions=[],
    meta=Meta(
        data_mode="sample",
        as_of="2026-10-09T08:30:00+05:30",
        latest_observation_date="2026-10-03",
        sources=[],
        trust=TrustMeta(score=30, label="Insufficient", calibrated=False),
        warnings=[],
        llm_mode="rule_based"
    )
)
with open('backend/tests/fixtures/api_examples/recommend_insufficient.json', 'w') as f:
    d = recommend_insufficient.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

whatif = WhatIfResponse(
    baseline=recommend,
    scenario=recommend,
    delta={"action_change": False, "nr_change": 0.0},
    assumptions=[],
    meta=meta
)
with open('backend/tests/fixtures/api_examples/whatif.json', 'w') as f:
    d = whatif.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

risk = RiskResponse(
    flags=[{"code": "PRICE_DROP", "severity": "warn", "evidence": {}}],
    radar={"direction": "up", "confidence": "low", "evidence": "something"},
    meta=meta
)
with open('backend/tests/fixtures/api_examples/risk.json', 'w') as f:
    d = risk.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

weather_risk = WeatherRiskResponse(
    daily_precip=[{"date": "2026-10-09", "precip_mm": 5.0}],
    flag=None,
    meta=meta
)
with open('backend/tests/fixtures/api_examples/weather_risk.json', 'w') as f:
    d = weather_risk.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

pool = PoolResponse(
    shares=[{"farmer_id": 1, "share": 50.0}],
    saving=10.0,
    meta=meta
)
with open('backend/tests/fixtures/api_examples/pool.json', 'w') as f:
    d = pool.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

chat = ChatResponse(
    reply="Wait 3 days.",
    language="en",
    tools_used=["forecast"],
    evidence={"forecast": "2050"},
    suggested_actions=[],
    meta=meta
)
with open('backend/tests/fixtures/api_examples/chat.json', 'w') as f:
    d = chat.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

backtest = BacktestResponse(
    metrics={"mean_gain": 150.0},
    caveats=["synthetic"],
    data_origin_summary="synthetic",
    meta=meta
)
with open('backend/tests/fixtures/api_examples/backtest.json', 'w') as f:
    d = backtest.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

policy = PolicyEventsResponse(
    connected=False,
    events=None,
    meta=meta
)
with open('backend/tests/fixtures/api_examples/policy_events.json', 'w') as f:
    d = policy.dict()
    d['_example'] = True
    json.dump(d, f, indent=2)

print("Generated fixtures.")
