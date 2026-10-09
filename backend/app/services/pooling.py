def calculate_farmer_pool(farmers: list, nr_result_per_quintal: float):
    total_qty = sum(f["qty"] for f in farmers)
    
    pool_results = []
    for f in farmers:
        share = f["qty"] / total_qty if total_qty > 0 else 0
        payout = nr_result_per_quintal * f["qty"]
        pool_results.append({
            "farmer_id": f["id"],
            "qty": f["qty"],
            "share_pct": round(share * 100, 2),
            "payout": round(payout, 2)
        })
        
    return {
        "total_pool_qty": total_qty,
        "total_pool_payout": round(nr_result_per_quintal * total_qty, 2),
        "farmers": pool_results
    }
