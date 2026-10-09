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
        return json.dumps(res)
    elif tool_name == "run_whatif":
        # simple mock
        return json.dumps({"status": "whatif_executed"})
    return json.dumps({"error": "tool not found"})
