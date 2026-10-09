def calculate_net_return(
    price: float,
    qty_quintals: float,
    s_transit: float,
    s_hold: float,
    commission_rate: float,
    transport_cost_per_quintal: float,
    surcharge_per_quintal: float,
    rain_mult: float = 1.0
):
    
    effective_s_transit = min(1.0, s_transit * rain_mult)
    s_total = 1 - (1 - effective_s_transit) * (1 - s_hold)
    
    g = price * (1 - s_total)
    comm = commission_rate * g
    
    nr = g - comm - transport_cost_per_quintal - surcharge_per_quintal
    total_val = nr * qty_quintals
    
    spoilage_cost = price - g
    
    drivers = {
        "base_price": price,
        "spoilage_cost": -spoilage_cost,
        "commission": -comm,
        "transport": -transport_cost_per_quintal,
        "surcharge": -surcharge_per_quintal
    }
    
    assert abs(sum(drivers.values()) - nr) < 1e-6, "Drivers do not sum to NR exactly"
    
    return {
        "net_return_per_quintal": round(nr, 2),
        "total_net_return": round(total_val, 2),
        "gross_realized_price": round(g, 2),
        "spoilage_total_pct": round(s_total, 4),
        "drivers": {k: round(v, 2) for k, v in drivers.items()}
    }

def calculate_scenarios(price_p10, price_p50, price_p90, qty, params):
    return {
        "p10": calculate_net_return(price_p10, qty, **params),
        "p50": calculate_net_return(price_p50, qty, **params),
        "p90": calculate_net_return(price_p90, qty, **params),
    }
