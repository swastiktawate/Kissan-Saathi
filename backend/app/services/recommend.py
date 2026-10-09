import math
from backend.app.services.compare import compare_mandis

async def recommend_action(crop_id: str, home_mandi_id: str, quantity_q: float, origin_date: str, risk_setting: str = "balanced", horizon_days: int = 7, trust_label: str = "High") -> dict:
    
    comp = await compare_mandis(crop_id, home_mandi_id, quantity_q, origin_date, horizon_days)
    results = comp["results"]
    
    lambdas = {"cautious": 1.0, "balanced": 0.5, "aggressive": 0.0}
    lam = lambdas.get(risk_setting, 0.5)
    
    for r in results:
        r["risk"] = max(0, r["nr_p50"] - r["nr_p10"])
        r["score"] = r["nr_p50"] - lam * r["risk"]
        
    ref_opt = next((r for r in results if r["mandi_id"] == home_mandi_id and r["horizon"] == 0), None)
    if not ref_opt:
        ref_opt = results[0]
        
    margin = max(25.0, 0.015 * abs(ref_opt["nr_p50"]))
    
    best_opt = max(results, key=lambda x: x["score"])
    
    # Split sale logic
    split_opt = None
    if lam > 0 and len(results) > 1:
        best_w = None
        best_split_score = -1e9
        best_pair = None
        
        top_opts = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
        for i in range(len(top_opts)):
            for j in range(i+1, len(top_opts)):
                A = top_opts[i]
                B = top_opts[j]
                
                for w_int in range(2, 9):
                    w = w_int / 10.0
                    nr_p50 = w * A["nr_p50"] + (1-w) * B["nr_p50"]
                    risk_A = A["risk"]
                    risk_B = B["risk"]
                    risk_P = math.sqrt((w**2 * risk_A**2) + ((1-w)**2 * risk_B**2) + (2 * 0.5 * w * (1-w) * risk_A * risk_B))
                    score = nr_p50 - lam * risk_P
                    
                    if score > best_split_score:
                        best_split_score = score
                        best_w = w
                        best_pair = (A, B)
                        
        if best_pair and best_split_score > best_opt["score"] + margin:
            split_opt = {
                "score": best_split_score,
                "A": best_pair[0],
                "B": best_pair[1],
                "w": best_w
            }
            
    reasons = []
    
    if trust_label == "Insufficient":
        action = "INSUFFICIENT_DATA"
        confidence = "Low"
        reasons.append("Trust score is Insufficient. We cannot confidently recommend an action.")
        best_opt = ref_opt
    else:
        if trust_label == "Medium":
            reasons.append("Caution: Data trust is Medium. Estimates may have higher uncertainty.")
            
        if split_opt:
            action = "SPLIT_SALE"
            confidence = "Moderate"
            best_opt = split_opt["A"] # For baseline comparisons
            reasons.append(f"Split sale recommended: {int(split_opt['w']*100)}% to {split_opt['A']['mandi_id']} at day {split_opt['A']['horizon']}, and {int((1-split_opt['w'])*100)}% to {split_opt['B']['mandi_id']} at day {split_opt['B']['horizon']}.")
        else:
            if best_opt["score"] <= ref_opt["score"] + margin:
                action = "SELL_NOW"
                best_opt = ref_opt
                confidence = "Clear"
                reasons.append(f"No option beats selling today at {home_mandi_id} by the margin of {margin:.2f} Rs/q.")
            else:
                if best_opt["mandi_id"] != home_mandi_id and best_opt["horizon"] == 0:
                    action = "ANOTHER_MANDI"
                    confidence = "Clear"
                    reasons.append(f"Selling today at {best_opt['mandi_id']} yields higher return.")
                elif best_opt["horizon"] > 0:
                    action = "WAIT_N_DAYS"
                    confidence = "Moderate"
                    reasons.append(f"Waiting {best_opt['horizon']} days yields higher expected returns.")
                    
    return {
        "action": action,
        "confidence": confidence,
        "best_option": best_opt,
        "reference_option": ref_opt,
        "margin_applied": margin,
        "reasons": reasons,
        "all_results": results
    }
