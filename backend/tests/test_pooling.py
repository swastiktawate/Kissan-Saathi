from backend.app.services.pooling import calculate_farmer_pool


def test_farmer_pool():
    farmers = [{"id": 1, "qty": 10}, {"id": 2, "qty": 40}]
    res = calculate_farmer_pool(farmers, 1723.60)
    
    assert res["total_pool_qty"] == 50
    assert res["total_pool_payout"] == 86180.0
    
    assert res["farmers"][0]["share_pct"] == 20.0
    assert res["farmers"][0]["payout"] == 17236.0
    
    assert res["farmers"][1]["share_pct"] == 80.0
    assert res["farmers"][1]["payout"] == 68944.0
