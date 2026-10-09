-- Idempotent DDL for Kisan Saathi
CREATE TABLE IF NOT EXISTS crops (
    crop_id VARCHAR PRIMARY KEY,
    name_en VARCHAR,
    name_hi VARCHAR,
    name_mr VARCHAR,
    name_pa VARCHAR,
    name_hr VARCHAR,
    unit_basis VARCHAR,
    perishability_class VARCHAR,
    max_wait_days INTEGER,
    spoilage_params JSON
);

CREATE TABLE IF NOT EXISTS mandis (
    mandi_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    district VARCHAR,
    state VARCHAR,
    lat DOUBLE,
    lon DOUBLE,
    is_pilot BOOLEAN,
    aliases VARCHAR[]
);

CREATE TABLE IF NOT EXISTS price_observations (
    obs_id VARCHAR PRIMARY KEY,
    crop_id VARCHAR,
    mandi_id VARCHAR,
    observation_date DATE,
    min_price DOUBLE,
    modal_price DOUBLE,
    max_price DOUBLE,
    arrivals_quintals DOUBLE,
    variety VARCHAR,
    source VARCHAR,
    source_ref VARCHAR,
    fetched_at TIMESTAMP,
    data_origin VARCHAR,
    ingestion_run_id VARCHAR,
    is_outlier BOOLEAN,
    outlier_reason VARCHAR,
    is_imputed BOOLEAN
);

CREATE TABLE IF NOT EXISTS weather_daily (
    location_id VARCHAR,
    date DATE,
    precip_mm DOUBLE,
    precip_prob DOUBLE,
    temp_max DOUBLE,
    temp_min DOUBLE,
    is_forecast BOOLEAN,
    source VARCHAR,
    fetched_at TIMESTAMP,
    data_origin VARCHAR
);

CREATE TABLE IF NOT EXISTS distances (
    from_id VARCHAR,
    to_mandi_id VARCHAR,
    distance_km DOUBLE,
    duration_h DOUBLE,
    method VARCHAR,
    computed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS forecasts (
    forecast_id VARCHAR PRIMARY KEY,
    run_id VARCHAR,
    crop_id VARCHAR,
    mandi_id VARCHAR,
    origin_date DATE,
    target_date DATE,
    horizon_days INTEGER,
    p10 DOUBLE,
    p50 DOUBLE,
    p90 DOUBLE,
    method VARCHAR,
    calibrated BOOLEAN,
    model_version VARCHAR,
    generated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS forecast_diagnostics (
    run_id VARCHAR PRIMARY KEY,
    crop_id VARCHAR,
    mandi_id VARCHAR,
    horizon INTEGER,
    mae DOUBLE,
    pinball_loss DOUBLE,
    empirical_coverage_p10_p90 DOUBLE,
    n_eval INTEGER,
    vs_naive_skill DOUBLE
);

CREATE TABLE IF NOT EXISTS cost_params (
    crop_id VARCHAR PRIMARY KEY,
    commission_rate DOUBLE,
    hamali_rs_per_q DOUBLE,
    storage_rs_per_q_day DOUBLE,
    spoilage_transit_per_hour DOUBLE,
    spoilage_daily_rate DOUBLE,
    vehicle_tiers JSON,
    diesel_index DOUBLE,
    assumption BOOLEAN,
    notes VARCHAR
);

CREATE TABLE IF NOT EXISTS trust_scores (
    crop_id VARCHAR,
    mandi_id VARCHAR,
    computed_at TIMESTAMP,
    total DOUBLE,
    components JSON,
    label VARCHAR,
    reasons VARCHAR[]
);

CREATE TABLE IF NOT EXISTS policy_events (
    event_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    summary VARCHAR,
    category VARCHAR,
    crops VARCHAR[],
    published_at TIMESTAMP,
    source_url VARCHAR,
    data_origin VARCHAR
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id VARCHAR PRIMARY KEY,
    source VARCHAR,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    status VARCHAR,
    rows_in INTEGER,
    rows_valid INTEGER,
    rows_flagged INTEGER,
    mode VARCHAR,
    error VARCHAR
);

CREATE TABLE IF NOT EXISTS backtest_runs (
    run_id VARCHAR PRIMARY KEY,
    crop_id VARCHAR,
    "window" INTEGER,
    strategy_params JSON,
    results JSON,
    data_origin_summary VARCHAR,
    created_at TIMESTAMP
);
