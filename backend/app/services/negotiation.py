import datetime
from backend.app.db.connection import get_db_connection
from backend.app.services.forecast import generate_forecast

def get_fair_price(crop_id: str, mandi_id: str):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT observation_date, min_price, modal_price, max_price
        FROM price_observations
        WHERE crop_id = ? AND mandi_id = ?
        ORDER BY observation_date DESC
        LIMIT 1
    """, (crop_id, mandi_id)).fetchone()
    
    if not row:
        return {"error": "No data found"}
        
    obs_date_str = row[0].isoformat() if hasattr(row[0], 'isoformat') else str(row[0])
    min_p, modal_p, max_p = row[1], row[2], row[3]
    
    # Fallbacks in case min/max are missing or 0
    if not min_p: min_p = modal_p * 0.9
    if not max_p: max_p = modal_p * 1.1
    
    forecast = generate_forecast(crop_id, mandi_id, obs_date_str, horizon_days=1)
    tomorrow_p50 = forecast[0]["p50"] if forecast else modal_p
    
    # Target Fair Price
    target_price = max(modal_p, tomorrow_p50)
    
    return {
        "date": obs_date_str,
        "min_price": min_p,
        "modal_price": modal_p,
        "max_price": max_p,
        "tomorrow_p50": tomorrow_p50,
        "target_fair_price": target_price
    }

def get_regret_analysis(crop_id: str, mandi_id: str, quantity_q: float, sold_date: str):
    conn = get_db_connection()
    
    sold_row = conn.execute("""
        SELECT modal_price FROM price_observations 
        WHERE crop_id=? AND mandi_id=? AND observation_date=?
    """, (crop_id, mandi_id, sold_date)).fetchone()
    
    today_row = conn.execute("""
        SELECT observation_date, modal_price FROM price_observations 
        WHERE crop_id=? AND mandi_id=? 
        ORDER BY observation_date DESC LIMIT 1
    """, (crop_id, mandi_id)).fetchone()
    
    if not sold_row or not today_row:
        return {"error": "Missing data for given dates"}
        
    sold_price = sold_row[0]
    today_date_val = today_row[0]
    today_price = today_row[1]
    
    # parse dates safely
    from datetime import datetime as dt
    s_d = dt.strptime(sold_date, "%Y-%m-%d") if isinstance(sold_date, str) else sold_date
    t_d = dt.strptime(str(today_date_val), "%Y-%m-%d") if isinstance(today_date_val, str) else today_date_val
    days_diff = (t_d - s_d).days
    
    if days_diff <= 0:
        return {"error": "Sold date must be before the latest recorded date"}
        
    cost_params = conn.execute("SELECT storage_rs_per_q_day, spoilage_daily_rate FROM cost_params WHERE crop_id=?", (crop_id,)).fetchone()
    if not cost_params:
        cost_params = (0.0, 0.005)
        
    storage_day, s_hold_day = cost_params
    
    ret_sold = sold_price * quantity_q
    
    spoilage = min(1.0, s_hold_day * days_diff)
    effective_qty = quantity_q * (1 - spoilage)
    storage_cost = storage_day * quantity_q * days_diff
    ret_today = (today_price * effective_qty) - storage_cost
    
    diff = ret_today - ret_sold
    is_loss = diff > 0
    
    return {
        "sold_date": str(sold_date),
        "today_date": str(today_date_val),
        "sold_price": sold_price,
        "today_price": today_price,
        "quantity": quantity_q,
        "days_held": days_diff,
        "return_if_sold_then": ret_sold,
        "return_if_sold_today": ret_today,
        "difference": diff,
        "result": "loss" if is_loss else "saved",
        "message": f"You could have made ₹{abs(diff):.2f} more today" if is_loss else f"You saved ₹{abs(diff):.2f} from price drops and spoilage"
    }
