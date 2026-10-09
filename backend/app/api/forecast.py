import os
import joblib
import pandas as pd
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models")
MODEL_PATH = os.path.join(MODEL_DIR, "forecast_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoders.pkl")

# Global variables for caching the model in memory
_model = None
_encoders = None

def load_artifacts():
    global _model, _encoders
    if _model is None or _encoders is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
            raise HTTPException(status_code=500, detail="ML Models not found. Run training script first.")
        _model = joblib.load(MODEL_PATH)
        _encoders = joblib.load(ENCODER_PATH)

class ForecastRequest(BaseModel):
    commodity: str
    market: str
    variety: str = "Other"
    district: str = "Mumbai"
    start_date: str  # YYYY-MM-DD

@router.post("/predict")
async def predict_forecast(req: ForecastRequest):
    load_artifacts()
    
    try:
        start_dt = datetime.datetime.strptime(req.start_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="start_date must be in YYYY-MM-DD format")
        
    # Generate 365 dates
    dates = [start_dt + datetime.timedelta(days=i) for i in range(365)]
    
    # Prepare DataFrame
    df = pd.DataFrame({'Price Date': dates})
    df['month'] = df['Price Date'].dt.month
    df['day_of_year'] = df['Price Date'].dt.dayofyear
    df['day_of_week'] = df['Price Date'].dt.dayofweek
    
    # Add categoricals
    df['District'] = req.district
    df['Market'] = req.market
    df['Commodity'] = req.commodity
    df['Variety'] = req.variety
    
    # Encode categoricals using the loaded encoders
    # If a category was unseen during training, we must handle it gracefully.
    # The simplest fallback is to use the most frequent class (e.g. class 0) or handle via a custom fallback.
    for col in ['District', 'Market', 'Commodity', 'Variety']:
        le = _encoders[col]
        # We handle unseen labels by mapping them to a known label (e.g., the first one), 
        # or we could skip encoding and let HistGradientBoosting handle nans if we used integer casting,
        # but since we used LabelEncoder, we need integer IDs.
        known_classes = list(le.classes_)
        # map input to string
        val = str(df[col].iloc[0])
        if val in known_classes:
            encoded_val = le.transform([val])[0]
        else:
            # Fallback to the first known class
            encoded_val = 0
            
        df[col] = encoded_val
        
    features = ['District', 'Market', 'Commodity', 'Variety', 'month', 'day_of_year', 'day_of_week']
    X = df[features]
    
    # Predict
    preds = _model.predict(X)
    
    # Build response array
    results = []
    for i in range(365):
        results.append({
            "date": dates[i].strftime("%Y-%m-%d"),
            "predicted_price": round(float(preds[i]), 2)
        })
        
    return {"forecast": results}
