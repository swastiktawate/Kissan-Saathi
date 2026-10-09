from backend.app.services.backtest import run_backtest_simulation


def test_backtest_no_lookahead():
    res = run_backtest_simulation("tomato", "vashi", 30)
    assert "metrics" in res
    assert "mean_gain" in res["metrics"]
    assert "synthetic" in res["data_origin_summary"]
