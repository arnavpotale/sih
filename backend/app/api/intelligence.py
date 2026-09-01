from fastapi import APIRouter, HTTPException
from app.intelligence.prediction_service import prediction_service
from app.intelligence.dataset_builder import get_latest_features

router = APIRouter(prefix="/api/intelligence", tags=["Intelligence"])

@router.get("/project/{project_code}/prediction")
def get_prediction(project_code: str):
    features_dict = get_latest_features(project_code)
    
    if not features_dict:
        # If we couldn't build features, we still return the strict contract
        return prediction_service.get_prediction(project_code, {})
        
    result = prediction_service.get_prediction(project_code, features_dict)
    return result

@router.get("/models/status")
def get_model_status():
    return {
      "time_model": {
        "status": "EXPERIMENTAL_READY",
        "model": "XGBoost",
        "version": prediction_service.time_version,
        "training_period": "April, May 2026",
        "validation_period": "June 2026",
        "metrics": {
            "f1": 0.537,
            "precision": 0.464,
            "recall": 0.637
        }
      },
      "cost_model": {
        "status": "NOT_USEFUL",
        "reason": "Current dataset (2% positive rate) does not provide reliable signal for one-month cost deterioration prediction."
      },
      "data": {
        "reports_available": 4,
        "latest_report": "July 2026"
      }
    }

@router.get("/portfolio/summary")
def get_portfolio_summary():
    from app.intelligence.dataset_builder import get_all_latest_features
    
    df = get_all_latest_features()
    if df.empty:
        return {"portfolio_projects": []}
        
    portfolio_projects = []
    
    # We also need some basic risk engine score if we want to combine them, or just use prediction logic.
    for _, row in df.iterrows():
        features_dict = row.to_dict()
        proj_code = features_dict.get('project_code')
        if not proj_code: continue
        
        # Base Risk Engine proxy (just for fallback / baseline risk)
        risk_score = 0
        if features_dict.get('schedule_slip_days', 0) > 30: risk_score += 25
        if features_dict.get('current_cost_escalation_amount', 0) > 0: risk_score += 25
        if features_dict.get('physical_progress', 100) < 50 and features_dict.get('project_age_days', 0) > 1000: risk_score += 25
        if features_dict.get('schedule_slip_velocity', 0) > 0: risk_score += 25
        
        risk_level = "CRITICAL" if risk_score >= 75 else ("HIGH" if risk_score >= 50 else ("MODERATE" if risk_score >= 25 else "LOW"))
        
        # XGBoost Prediction
        pred = prediction_service.get_prediction(proj_code, features_dict)
        
        xgb_prob = pred.get("time_probability", 0)
        xgb_risk = pred.get("risk_classification", "LOW")
        xgb_status = pred.get("time_status", "UNKNOWN")
        
        portfolio_projects.append({
            "id": proj_code,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "xgb_probability": xgb_prob,
            "xgb_risk_classification": xgb_risk,
            "xgb_status": xgb_status,
            "warning_count": 1 if xgb_prob and xgb_prob >= 0.50 else 0
        })
        
    return {"portfolio_projects": portfolio_projects}
