import json
from backend.app.db.connection import get_db_connection

def calculate_pool_savings(farmers: list, mandi_id: str, vehicle_type: str = None, crop_id: str = 'tomato'):
    conn = get_db_connection()
    
    # Get distance
    dist_row = conn.execute("SELECT distance_km FROM distances WHERE to_mandi_id = ? LIMIT 1", (mandi_id,)).fetchone()
    distance_km = dist_row[0] if dist_row else 50.0  # Fallback 50km
    
    # Get vehicle tiers
    cost_row = conn.execute("SELECT vehicle_tiers FROM cost_params WHERE crop_id = ?", (crop_id,)).fetchone()
    if cost_row and cost_row[0]:
        tiers = json.loads(cost_row[0])
    else:
        # Fallback tiers
        tiers = [
            {"capacity_q": 10, "base_fare": 500, "rate_per_km": 15, "name": "Tempo"},
            {"capacity_q": 30, "base_fare": 1000, "rate_per_km": 25, "name": "Pickup"},
            {"capacity_q": 90, "base_fare": 2500, "rate_per_km": 40, "name": "Truck"}
        ]
        
    # Ensure tiers have names
    tier_names = ["Tempo", "Pickup", "Truck"]
    for i, t in enumerate(tiers):
        t["name"] = tier_names[i] if i < len(tier_names) else f"Vehicle_{i}"
        
    total_qty = sum(f.get("qty", 0) for f in farmers)
    if total_qty <= 0:
        return {"error": "Total quantity must be greater than 0"}

    # Determine Shared Vehicle
    optimal_tier = None
    if vehicle_type and vehicle_type.lower() != "auto":
        optimal_tier = next((t for t in tiers if t["name"].lower() == vehicle_type.lower()), tiers[-1])
    else:
        optimal_tier = next((t for t in tiers if t["capacity_q"] >= total_qty), tiers[-1])
        
    vehicles_needed = max(1, int((total_qty + optimal_tier["capacity_q"] - 1) // optimal_tier["capacity_q"]))
    
    total_shared_cost = (optimal_tier["base_fare"] + optimal_tier["rate_per_km"] * distance_km) * vehicles_needed
    shared_cost_per_q = total_shared_cost / total_qty
    
    breakdown = []
    primary_savings_per_q = 0
    
    for idx, farmer in enumerate(farmers):
        qty = farmer.get("qty", 0)
        if qty <= 0:
            continue
            
        alone_tier = next((t for t in tiers if t["capacity_q"] >= qty), tiers[-1])
        alone_vehicles_needed = max(1, int((qty + alone_tier["capacity_q"] - 1) // alone_tier["capacity_q"]))
        alone_total_cost = (alone_tier["base_fare"] + alone_tier["rate_per_km"] * distance_km) * alone_vehicles_needed
        alone_cost_per_q = alone_total_cost / qty
        
        shared_payment = shared_cost_per_q * qty
        savings = alone_total_cost - shared_payment
        savings_per_q = alone_cost_per_q - shared_cost_per_q
        
        if idx == 0:
            primary_savings_per_q = savings_per_q
            
        breakdown.append({
            "name": farmer.get("name", f"Farmer {idx+1}"),
            "qty": qty,
            "alone_cost": alone_total_cost,
            "shared_cost": shared_payment,
            "savings": savings,
            "savings_per_q": savings_per_q
        })
        
    return {
        "total_qty": total_qty,
        "optimal_vehicle": optimal_tier["name"],
        "vehicles_needed": vehicles_needed,
        "total_cost": total_shared_cost,
        "shared_cost_per_q": shared_cost_per_q,
        "primary_savings_per_q": primary_savings_per_q,
        "breakdown": breakdown
    }
