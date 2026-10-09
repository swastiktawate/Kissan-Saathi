import os
import glob
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

DATASET_DIR = r"C:\Users\VEDANT\Documents\antigravity\hopeful-bose\dataset"
MODEL_DIR = r"C:\Users\VEDANT\Documents\antigravity\hopeful-bose\backend\app\ml_models"

def load_data(data_dir):
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not csv_files:
        raise ValueError(f"No CSV files found in {data_dir}")
        
    dfs = []
    for file in csv_files:
        try:
            # First row is metadata, second row is the header
            df = pd.read_csv(file, header=1)
            dfs.append(df)
        except Exception as e:
            print(f"Failed to read {file}: {e}")
            
    if not dfs:
        raise ValueError("Could not read any files.")
        
    return pd.concat(dfs, ignore_index=True)

def clean_data(df):
    # Ensure expected columns exist
    expected_cols = ['State/UT', 'District', 'Market', 'Commodity', 'Variety', 'Min Price', 'Max Price', 'Modal Price', 'Price Date']
    for col in expected_cols:
        if col not in df.columns:
            raise KeyError(f"Missing expected column: {col}")
            
    # Drop rows where critical columns are NaN
    df = df.dropna(subset=['Market', 'Commodity', 'Variety', 'District', 'Modal Price', 'Price Date'])
    
    # Clean prices (remove commas and parse to float)
    for col in ['Min Price', 'Max Price', 'Modal Price']:
        df[col] = df[col].astype(str).str.replace(',', '').str.replace(' ', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Drop if prices couldn't be parsed
    df = df.dropna(subset=['Modal Price'])
    
    # Parse dates
    df['Price Date'] = pd.to_datetime(df['Price Date'], format='%d-%m-%Y', errors='coerce')
    df = df.dropna(subset=['Price Date'])
    
    # Extract temporal features
    df['month'] = df['Price Date'].dt.month
    df['day_of_year'] = df['Price Date'].dt.dayofyear
    df['day_of_week'] = df['Price Date'].dt.dayofweek
    
    return df

def train_model():
    print("Loading data...")
    df = load_data(DATASET_DIR)
    
    print(f"Loaded {len(df)} rows. Cleaning data...")
    df = clean_data(df)
    print(f"After cleaning: {len(df)} rows.")
    
    # Define categoricals
    categorical_cols = ['District', 'Market', 'Commodity', 'Variety']
    encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        # Ensure string type
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    features = ['District', 'Market', 'Commodity', 'Variety', 'month', 'day_of_year', 'day_of_week']
    X = df[features]
    y = df['Modal Price']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    # HistGradientBoostingRegressor natively supports missing values, but we already dropped them
    # It also has good performance for tabular data
    model = HistGradientBoostingRegressor(random_state=42, max_iter=200)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    print(f"Model saved successfully with R2 Score: {score:.2f}")
    
    # Ensure model dir exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save model and encoders
    joblib.dump(model, os.path.join(MODEL_DIR, "forecast_model.pkl"))
    joblib.dump(encoders, os.path.join(MODEL_DIR, "encoders.pkl"))
    print("Artifacts saved to backend/app/ml_models/")

if __name__ == "__main__":
    train_model()
