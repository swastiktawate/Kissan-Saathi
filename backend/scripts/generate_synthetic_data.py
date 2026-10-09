import os
import random
import argparse
import datetime
import pandas as pd
import numpy as np

def generate_synthetic_data(args):
    # Set fixed seed
    np.random.seed(42)
    random.seed(42)
    
    crops = [
        {"id": "tomato", "name": "Tomato", "base_price": 2000, "season_amp": 500, "volatility": 150},
        {"id": "onion", "name": "Onion", "base_price": 1500, "season_amp": 300, "volatility": 100},
        {"id": "potato", "name": "Potato", "base_price": 1000, "season_amp": 200, "volatility": 80},
        {"id": "banana", "name": "Banana", "base_price": 2500, "season_amp": 400, "volatility": 120},
    ]
    
    mandis = [
        {"id": "vashi", "name": "Vashi", "state": "Maharashtra", "district": "Thane"},
        {"id": "nerul", "name": "Nerul", "state": "Maharashtra", "district": "Thane"},
        {"id": "panvel", "name": "Panvel", "state": "Maharashtra", "district": "Raigad"},
        {"id": "pune", "name": "Pune", "state": "Maharashtra", "district": "Pune"},
        {"id": "nashik", "name": "Nashik", "state": "Maharashtra", "district": "Nashik"},
        {"id": "kalyan", "name": "Kalyan", "state": "Maharashtra", "district": "Thane"},
    ]
    
    # 180 days up to "today"
    end_date = datetime.date(2026, 10, 8)
    if args.stale_series:
        end_date = end_date - datetime.timedelta(days=6)
        
    start_date = end_date - datetime.timedelta(days=180)
    dates = [start_date + datetime.timedelta(days=i) for i in range(181)]
    
    rows = []
    
    # Neighbour lead-lag: Let Nashik lead Vashi by 1 day for Onion.
    # We will simulate a shock in Nashik at day 100, which propagates to Vashi at day 101.
    
    for crop in crops:
        # Generate base prices with seasonality
        base_series = np.array([
            crop["base_price"] + crop["season_amp"] * np.sin(2 * np.pi * i / 365.0) 
            for i in range(len(dates))
        ])
        
        for mandi in mandis:
            prices = base_series + np.random.normal(0, crop["volatility"], len(dates))
            
            # Weekly pattern: prices slightly higher on weekends
            for i, d in enumerate(dates):
                if d.weekday() >= 5:
                    prices[i] += 50
            
            # Arrivals-price inverse relation
            # Base arrivals ~ 500 q. 
            arrivals = 500 + np.random.normal(0, 50, len(dates))
            # Price drops when arrivals surge
            arrivals_noise = (arrivals - 500) * -1.5
            prices += arrivals_noise
            
            # Shocks (e.g. at day 100)
            if crop["id"] == "onion":
                if mandi["id"] == "nashik":
                    prices[100] += 800  # huge spike
                elif mandi["id"] == "vashi":
                    prices[101] += 700  # lagged spike
                    
            for i, d in enumerate(dates):
                if args.sparse_series and random.random() < 0.5:
                    continue  # 50% missing data
                    
                modal = max(100, int(prices[i]))
                min_p = int(modal * 0.9)
                max_p = int(modal * 1.1)
                arr = max(10, int(arrivals[i]))
                
                rows.append({
                    "state": mandi["state"],
                    "district": mandi["district"],
                    "market": mandi["name"],
                    "commodity": crop["name"],
                    "variety": "Other",
                    "grade": "FAQ",
                    "arrival_date": d.strftime("%d/%m/%Y"),
                    "min_price": min_p,
                    "max_price": max_p,
                    "modal_price": modal,
                    "arrivals": arr,
                    "data_origin": "synthetic"
                })

    df = pd.DataFrame(rows)
    
    # Inject defects (deliberate)
    # 2. Tonne vs Quintal (arrivals * 0.1 for a few rows)
    tonne_idx = df.sample(5, random_state=43).index
    df["arrivals"] = df["arrivals"].astype(float)
    df.loc[tonne_idx, "arrivals"] = df.loc[tonne_idx, "arrivals"] * 0.1
    
    # 3. Price outliers (10x price)
    outlier_idx = df.sample(5, random_state=44).index
    df.loc[outlier_idx, "modal_price"] = df.loc[outlier_idx, "modal_price"] * 10
    
    # 4. Unit errors (price 0.1x)
    unit_idx = df.sample(5, random_state=45).index
    df["modal_price"] = df["modal_price"].astype(float)
    df.loc[unit_idx, "modal_price"] = df.loc[unit_idx, "modal_price"] * 0.1
    
    # 5. Modal outside min/max
    bad_modal_idx = df.sample(5, random_state=46).index
    df.loc[bad_modal_idx, "modal_price"] = df.loc[bad_modal_idx, "max_price"] + 500
    
    # 6. Future date
    df.loc[0, "arrival_date"] = (datetime.date.today() + datetime.timedelta(days=10)).strftime("%d/%m/%Y")

    # 1. Duplicates (done last to not affect or be affected by other defects)
    df = pd.concat([df, df.sample(5, random_state=42)]).reset_index(drop=True)

    os.makedirs('data/sample', exist_ok=True)
    df.to_csv('data/sample/synthetic_mandi_prices.csv', index=False)
    
    # Synthetic weather
    weather_rows = []
    for mandi in mandis:
        for i, d in enumerate(dates):
            precip = 0
            if 110 <= i <= 112: # heavy rain episode
                precip = random.uniform(30, 80)
            elif random.random() < 0.1:
                precip = random.uniform(1, 10)
                
            weather_rows.append({
                "location_id": mandi["id"],
                "date": d.strftime("%Y-%m-%d"),
                "precip_mm": precip,
                "precip_prob": 100 if precip > 0 else 0,
                "temp_max": 32,
                "temp_min": 24,
                "is_forecast": False,
                "source": "synthetic_generator",
                "fetched_at": datetime.datetime.now().isoformat(),
                "data_origin": "synthetic"
            })
    pd.DataFrame(weather_rows).to_csv('data/sample/synthetic_weather.csv', index=False)
    print("Generated synthetic data in data/sample/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stale-series", action="store_true")
    parser.add_argument("--sparse-series", action="store_true")
    args = parser.parse_args()
    generate_synthetic_data(args)
