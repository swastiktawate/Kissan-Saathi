import datetime
import json

from backend.app.services.recommend import recommend_action


async def execute_tool(tool_name: str, arguments: dict):
    origin = datetime.date.today().isoformat()
    if tool_name == "recommend":
        res = await recommend_action(
            crop_id=arguments.get("crop", "tomato"),
            home_mandi_id=arguments.get("home_mandi", "vashi"),
            quantity_q=arguments.get("quantity_q", 50),
            origin_date=origin,
            risk_setting=arguments.get("risk_setting", "balanced"),
            horizon_days=arguments.get("horizon_days", 7)
        )
        if "all_results" in res:
            del res["all_results"]
        return json.dumps(res)
    elif tool_name == "run_whatif":
        # simple mock
        return json.dumps({"status": "whatif_executed"})
    elif tool_name == "forecast_price":
        # Call the forecast endpoint logic directly
        try:
            from backend.app.api.forecast import ForecastRequest, predict_forecast
            req = ForecastRequest(
                commodity=arguments.get("crop", "tomato").capitalize(),
                market=arguments.get("market", "Vashi").capitalize(),
                district=arguments.get("district", "Mumbai").capitalize(),
                start_date=origin
            )
            res = await predict_forecast(req)
            # Return the full forecast so the LLM can answer long-term queries (e.g. 6 months out)
            forecast_data = res.get("forecast", [])
            return json.dumps({"forecast": forecast_data})
        except Exception as e:
            return json.dumps({"error": f"Forecast failed: {e}"})
    return json.dumps({"error": "tool not found"})
