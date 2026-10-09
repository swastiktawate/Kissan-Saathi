import pandas as pd
import datetime

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    
    today = datetime.date.today().isoformat()
    
    future_mask = df['observation_date'] > today
    neg_price_mask = (df['min_price'] <= 0) | (df['modal_price'] <= 0) | (df['max_price'] <= 0)
    neg_arr_mask = df['arrivals'] < 0
    
    drop_mask = future_mask | neg_price_mask | neg_arr_mask
    valid_df = df[~drop_mask].copy()
    
    if 'is_outlier' not in valid_df.columns:
        valid_df['is_outlier'] = False
        valid_df['outlier_reason'] = ""
        
    modal_out_mask = (valid_df['modal_price'] < valid_df['min_price']) | (valid_df['modal_price'] > valid_df['max_price'])
    valid_df.loc[modal_out_mask, 'is_outlier'] = True
    valid_df.loc[modal_out_mask, 'outlier_reason'] = "Modal price outside min/max"
    
    return valid_df
