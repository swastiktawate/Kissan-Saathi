import pandas as pd
from backend.app.services.series import get_series

def get_features(crop_id: str, mandi_id: str, origin_date: str) -> pd.DataFrame:
    df = get_series(crop_id, mandi_id, origin_date)
    if df.empty:
        return df
        
    for lag in [1, 2, 3, 7, 14]:
        df[f'price_lag_{lag}'] = df['modal_price'].shift(lag)
        
    df['rolling_mean_7'] = df['modal_price'].rolling(7, min_periods=1).mean()
    df['rolling_std_7'] = df['modal_price'].rolling(7, min_periods=1).std()
    
    df['arr_mean_14'] = df['arrivals_quintals'].rolling(14, min_periods=1).mean()
    df['arrival_ratio'] = df['arrivals_quintals'] / (df['arr_mean_14'] + 1e-6)
    
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    
    return df
