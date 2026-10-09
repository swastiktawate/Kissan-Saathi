import pytest
from backend.app.services.net_return import calculate_net_return

def test_worked_example():
    res = calculate_net_return(
        price=2000,
        qty_quintals=50,
        s_transit=0.03,
        s_hold=0.0,
        commission_rate=0.06,
        transport_cost_per_quintal=100,
        surcharge_per_quintal=0
    )
    
    assert res["net_return_per_quintal"] == 1723.60
    assert res["total_net_return"] == 86180.0
    
    d = res["drivers"]
    assert d["base_price"] == 2000
    assert d["spoilage_cost"] == -60
    assert d["commission"] == -116.40
    assert d["transport"] == -100
    assert d["surcharge"] == 0
