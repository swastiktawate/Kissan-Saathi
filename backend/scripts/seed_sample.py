import os
import shutil

def seed_sample():
    os.makedirs('data/raw', exist_ok=True)
    
    # Just copy the sample files to raw so they can be processed by ingestion/cleaning
    if os.path.exists('data/sample/synthetic_mandi_prices.csv'):
        shutil.copy('data/sample/synthetic_mandi_prices.csv', 'data/raw/')
        print("Staged synthetic_mandi_prices.csv to data/raw/")
        
    if os.path.exists('data/sample/synthetic_weather.csv'):
        shutil.copy('data/sample/synthetic_weather.csv', 'data/raw/')
        print("Staged synthetic_weather.csv to data/raw/")

if __name__ == '__main__':
    seed_sample()
