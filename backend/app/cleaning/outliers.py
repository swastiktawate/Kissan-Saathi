import pandas as pd


def flag_outliers(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    if 'is_outlier' not in df.columns:
        df['is_outlier'] = False
        df['outlier_reason'] = ""
        
    def process_group(g):
        g = g.sort_values('observation_date')
        rolling_med = g['modal_price'].rolling(window=30, min_periods=1).median()
        
        unit_high = g['modal_price'] > 10 * rolling_med
        unit_low = g['modal_price'] < 0.1 * rolling_med
        
        arr_med = g['arrivals'].rolling(window=30, min_periods=1).median()
        arr_tonne = g['arrivals'] < 0.15 * arr_med
        g.loc[arr_tonne, 'arrivals'] = g.loc[arr_tonne, 'arrivals'] * 10.0
        
        def mad(x):
            s = pd.Series(x)
            return abs(s - s.median()).median()
            
        rolling_mad = g['modal_price'].rolling(window=30, min_periods=1).apply(mad)
        
        curr_mad = abs(g['modal_price'] - rolling_med)
        z_score = curr_mad / (rolling_mad * 1.4826 + 1e-6)
        mad_outlier = z_score > 3.5
        
        mask_outlier = unit_high | unit_low | mad_outlier
        
        g.loc[unit_high, 'outlier_reason'] = "Price 10x rolling median (unit error)"
        g.loc[unit_low, 'outlier_reason'] = "Price 0.1x rolling median (unit error)"
        g.loc[mad_outlier & ~unit_high & ~unit_low, 'outlier_reason'] = "MAD z-score > 3.5"
        
        g.loc[mask_outlier, 'is_outlier'] = True
        
        return g
        
    df = df.groupby(['crop_id', 'mandi_id'], group_keys=False).apply(process_group).reset_index(drop=True)
    return df
