import pytest
import pandas as pd
import datetime
from backend.app.cleaning.normalize import normalize_data
from backend.app.cleaning.validate import validate_data
from backend.app.cleaning.outliers import flag_outliers

def test_cleaning_pipeline():
    # Mock data
    today = datetime.date.today()
    future = today + datetime.timedelta(days=10)
    
    df = pd.DataFrame([
        {"arrival_date": today.strftime("%d/%m/%Y"), "commodity": "Tomato", "market": "Vashi", "min_price": 100, "modal_price": 150, "max_price": 200, "arrivals": 50, "variety": "Other"},
        {"arrival_date": today.strftime("%d/%m/%Y"), "commodity": "Tomato", "market": "Vashi", "min_price": 100, "modal_price": 250, "max_price": 200, "arrivals": 50, "variety": "Desi"}, # modal out of bounds
        {"arrival_date": future.strftime("%d/%m/%Y"), "commodity": "Tomato", "market": "Vashi", "min_price": 100, "modal_price": 150, "max_price": 200, "arrivals": 50, "variety": "Other"} # future date
    ])
    
    df_norm = normalize_data(df)
    assert 'crop_id' in df_norm.columns
    assert 'observation_date' in df_norm.columns
    
    df_valid = validate_data(df_norm)
    # Future date rejected
    assert len(df_valid) == 2
    # Modal out of bounds flagged
    outliers = df_valid[df_valid['is_outlier'] == True]
    assert len(outliers) == 1
    
    # Needs 30 days for rolling median, but handles min_periods=1
    df_clean = flag_outliers(df_valid)
    assert 'is_outlier' in df_clean.columns
