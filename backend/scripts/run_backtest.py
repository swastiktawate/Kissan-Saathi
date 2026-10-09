import json

from backend.app.services.backtest import run_backtest_simulation

if __name__ == "__main__":
    res = run_backtest_simulation("tomato", "vashi", 180)
    print(json.dumps(res, indent=2))
