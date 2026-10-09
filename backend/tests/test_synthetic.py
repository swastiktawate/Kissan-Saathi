import os
import pandas as pd
from backend.scripts.generate_synthetic_data import generate_synthetic_data
import argparse
from unittest.mock import patch

def test_synthetic_generation():
    args = argparse.Namespace(stale_series=False, sparse_series=False)
    generate_synthetic_data(args)
    
    assert os.path.exists('data/sample/synthetic_mandi_prices.csv')
    df = pd.read_csv('data/sample/synthetic_mandi_prices.csv')
    
    # Assert origin labels
    assert (df['data_origin'] == 'synthetic').all()
    
    # Assert injected defects
    # 5 duplicates
    assert df.duplicated().sum() == 5
    
    # 1 future date (last row)
    # the date format is dd/mm/yyyy
    df['arrival_date_obj'] = pd.to_datetime(df['arrival_date'], format='%d/%m/%Y')
    import datetime
    future_dates = df[df['arrival_date_obj'] > pd.Timestamp(datetime.date.today())]
    assert len(future_dates) == 1
    
    # Modal outside min/max
    bad_modals = df[(df['modal_price'] > df['max_price']) | (df['modal_price'] < df['min_price'])]
    assert len(bad_modals) >= 5 # 5 explicit + some maybe from price outlirer 10x
    
    # File size check (< 5MB)
    size_mb = os.path.getsize('data/sample/synthetic_mandi_prices.csv') / (1024 * 1024)
    assert size_mb < 5.0
