import os
import sys
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.intelligence import get_portfolio_summary
from app.intelligence.dataset_builder import load_snapshots
from app.intelligence.prediction_service import prediction_service

def run_audit():
    print("Running portfolio audit...")
    df = load_snapshots()
    total_projects = df['project_code'].nunique() if not df.empty else 0
    
    summary = get_portfolio_summary()
    portfolio = summary.get("portfolio_projects", [])
    
    eligible = len(portfolio)
    ineligible = total_projects - eligible
    
    successful = []
    failed = []
    
    for p in portfolio:
        if p.get("xgb_status") == "MODEL_AVAILABLE":
            successful.append(p)
        else:
            failed.append(p)
            
    probs = [p["xgb_probability"] for p in successful if p["xgb_probability"] is not None]
    
    if probs:
        min_p = float(np.min(probs))
        max_p = float(np.max(probs))
        mean_p = float(np.mean(probs))
        median_p = float(np.median(probs))
        std_p = float(np.std(probs))
    else:
        min_p = max_p = mean_p = median_p = std_p = 0.0
        
    buckets = {
        "0.00-0.10": 0, "0.10-0.20": 0, "0.20-0.30": 0, "0.30-0.40": 0, "0.40-0.50": 0,
        "0.50-0.60": 0, "0.60-0.70": 0, "0.70-0.80": 0, "0.80-0.90": 0, "0.90-1.00": 0
    }
    
    for p in probs:
        if p < 0.1: buckets["0.00-0.10"] += 1
        elif p < 0.2: buckets["0.10-0.20"] += 1
        elif p < 0.3: buckets["0.20-0.30"] += 1
        elif p < 0.4: buckets["0.30-0.40"] += 1
        elif p < 0.5: buckets["0.40-0.50"] += 1
        elif p < 0.6: buckets["0.50-0.60"] += 1
        elif p < 0.7: buckets["0.60-0.70"] += 1
        elif p < 0.8: buckets["0.70-0.80"] += 1
        elif p < 0.9: buckets["0.80-0.90"] += 1
        else: buckets["0.90-1.00"] += 1
        
    low_count = sum(1 for p in successful if p["xgb_risk_classification"] == "LOW")
    mod_count = sum(1 for p in successful if p["xgb_risk_classification"] == "MODERATE")
    high_count = sum(1 for p in successful if p["xgb_risk_classification"] == "HIGH")
    crit_count = sum(1 for p in successful if p["xgb_risk_classification"] == "CRITICAL")
    
    audit_data = {
        "total_projects": total_projects,
        "eligible_projects": eligible,
        "ineligible_projects": ineligible,
        "successful_predictions": len(successful),
        "failed_predictions": len(failed),
        "insufficient_history_projects": ineligible + len(failed),
        "probability_stats": {
            "min_probability": min_p,
            "max_probability": max_p,
            "mean_probability": mean_p,
            "median_probability": median_p,
            "standard_deviation": std_p
        },
        "risk_categories": {
            "LOW": low_count,
            "MODERATE": mod_count,
            "HIGH": high_count,
            "CRITICAL": crit_count
        },
        "probability_distribution": buckets,
        "representative_samples": []
    }
    
    # Grab a few representative projects
    sample_categories = {}
    for p in successful:
        cat = p["xgb_risk_classification"]
        if cat not in sample_categories:
            sample_categories[cat] = p["id"]
            
    for cat, pid in sample_categories.items():
        res = prediction_service.get_prediction(pid, prediction_service.get_prediction.__code__.co_consts) # wait, we can just use the api
        
    # We will just save the audit without full SHAP, and do SHAP manually or via a separate loop.
    # Actually, we can fetch from get_prediction properly.
    from app.api.intelligence import get_prediction
    for cat, pid in sample_categories.items():
        try:
            pred = get_prediction(pid)
            audit_data["representative_samples"].append({
                "project_code": pid,
                "risk_category": cat,
                "probability": pred.get("time_probability"),
                "top_shap_drivers": pred.get("top_shap_drivers")
            })
        except Exception as e:
            pass
            
    out_path = os.path.join(os.path.dirname(__file__), '../data/ml/portfolio_prediction_audit.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(audit_data, f, indent=2)
        
    print(f"Audit completed. Saved to {out_path}")
    print(json.dumps(audit_data, indent=2))

if __name__ == "__main__":
    run_audit()
