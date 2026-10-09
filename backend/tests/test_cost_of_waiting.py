import pytest
from backend.app.services.cost_of_waiting import calculate_cost_of_waiting

def test_cost_of_waiting_decomposition():
    all_results = [
        {
            "mandi_id": "vashi", "horizon": 0, "nr_p50": 1000, "nr_p10": 900, "nr_p90": 1100,
            "nr_scenarios": {"p50": {"drivers": {"base_price": 1100, "spoilage_cost": -10, "commission": -50, "transport": -40, "surcharge": 0}}}
        },
        {
            "mandi_id": "vashi", "horizon": 1, "nr_p50": 1050, "nr_p10": 950, "nr_p90": 1150,
            "nr_scenarios": {"p50": {"drivers": {"base_price": 1160, "spoilage_cost": -20, "commission": -50, "transport": -40, "surcharge": 0}}}
        }
    ]
    
    cow = calculate_cost_of_waiting(all_results, "vashi")
    assert cow["optimal_day"] == 1
    
    curve1 = cow["curve"][1]
    assert curve1["gain_p50"] == 50
    assert curve1["drivers"]["price_effect"] == 60
    assert curve1["drivers"]["spoilage_diff"] == -10
    # sum of drivers = 60 - 10 + 0 + 0 + 0 = 50
