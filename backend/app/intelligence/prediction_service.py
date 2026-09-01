import os
import joblib
import json
import shap
import pandas as pd
from typing import Dict, Any

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models'))

# Human-readable mappings for features
FEATURE_LABELS = {
    "current_cost_escalation_amount": "Cost Escalation Amount",
    "current_cost_escalation_percent": "Cost Escalation (%)",
    "expenditure_ratio": "Expenditure Ratio",
    "physical_progress": "Physical Progress",
    "schedule_slip_days": "Schedule Slip",
    "project_age_days": "Project Age",
    "planned_duration_days": "Planned Duration",
    "expenditure_delta": "Expenditure Delta",
    "cost_revision_delta": "Cost Revision Delta",
    "physical_progress_delta": "Physical Progress Delta",
    "schedule_change_delta_days": "Recent Schedule Change",
    "expenditure_velocity": "Expenditure Velocity",
    "cost_revision_velocity": "Cost Revision Velocity",
    "physical_progress_velocity": "Progress Velocity",
    "schedule_slip_velocity": "Schedule Slip Velocity",
    "remaining_physical_progress": "Remaining Progress",
    "remaining_duration_days": "Remaining Duration",
    "cost_to_progress_ratio": "Cost/Progress Ratio",
    "expenditure_to_progress_ratio": "Expenditure/Progress Ratio",
    "progress_velocity_deceleration": "Progress Deceleration",
    "previous_expenditure": "Previous Expenditure",
    "previous_revised_cost": "Previous Revised Cost",
    "previous_physical_progress": "Previous Progress",
    "previous_revised_DoC": "Previous Date of Completion"
}

class PredictionService:
    def __init__(self):
        self.cost_model = None
        self.time_model = None
        self.cost_features = None
        self.time_features = None
        self.time_version = None
        
        self.load_models()
        
    def load_models(self):
        time_model_path = os.path.join(MODEL_DIR, 'time_overrun_model.joblib')
        time_manifest_path = os.path.join(MODEL_DIR, 'time_feature_manifest.json')
        metadata_path = os.path.join(MODEL_DIR, 'model_metadata.json')
        
        if os.path.exists(time_model_path) and os.path.exists(time_manifest_path):
            self.time_model = joblib.load(time_model_path)
            with open(time_manifest_path, 'r') as f:
                self.time_features = json.load(f)['features']
                
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                meta = json.load(f)
                self.time_version = meta.get('time_model_type', 'xgb') + "_" + meta.get('dataset_version', '1.0')
                
    def get_risk_classification(self, prob: float) -> str:
        if prob < 0.30: return "LOW"
        if prob < 0.50: return "MODERATE"
        if prob < 0.70: return "HIGH"
        return "CRITICAL"
        
    def get_recommended_action(self, top_drivers: list) -> str:
        driver_names = [d['feature'] for d in top_drivers]
        if "schedule_slip_velocity" in driver_names or "schedule_change_delta_days" in driver_names:
            return "Review implementation schedule and identify the current critical path bottleneck."
        if "progress_velocity_deceleration" in driver_names or "physical_progress_velocity" in driver_names:
            return "Investigate causes of physical progress deceleration (e.g. land acquisition, clearances)."
        if "remaining_duration_days" in driver_names:
            return "Remaining duration is constrained. Assess feasibility of fast-tracking remaining milestones."
        return "Conduct a comprehensive review of the project schedule and mobilize additional resources."
        
    def get_prediction(self, project_code: str, features_dict: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "project_code": project_code,
            "target": "future_time_overrun",
            "prediction_horizon": "Option A: Next-observation (1 month ahead)",
            "model_version": self.time_version or "Unknown",
        }
        
        # COST PREDICTION
        result["cost_status"] = "MODEL_NOT_USEFUL"
        result["cost_prediction"] = None
        result["cost_probability"] = None
            
        # TIME PREDICTION
        if not self.time_model:
            result["time_status"] = "MODEL_NOT_AVAILABLE"
            return result
            
        # Feature validation
        missing_features = [f for f in self.time_features if f not in features_dict]
        if missing_features:
            result["time_status"] = "INSUFFICIENT_FEATURE_DATA"
            result["missing_features"] = missing_features
            return result
            
        try:
            # Build DataFrame respecting ordering
            time_df = pd.DataFrame([features_dict], columns=self.time_features).fillna(0)
            
            time_prob = float(self.time_model.predict_proba(time_df)[0][1])
            time_pred = int(time_prob >= 0.5)
            
            result["time_status"] = "MODEL_AVAILABLE"
            result["time_prediction"] = time_pred
            result["time_probability"] = time_prob
            result["risk_classification"] = self.get_risk_classification(time_prob)
            
            explainer = shap.TreeExplainer(self.time_model)
            sv = explainer.shap_values(time_df)
            if isinstance(sv, list):
                shap_vals = sv[1][0]
            else:
                shap_vals = sv[0]
                
            shap_dict = {feat: val for feat, val in zip(self.time_features, shap_vals)}
            sorted_shap = sorted(shap_dict.items(), key=lambda item: abs(item[1]), reverse=True)
            
            pos_drivers = []
            for k, v in sorted_shap:
                if v > 0 and len(pos_drivers) < 3:
                    pos_drivers.append({"feature": k, "label": FEATURE_LABELS.get(k, k), "shap_value": float(v), "direction": "increases_risk"})
                    
            neg_drivers = []
            for k, v in sorted_shap:
                if v < 0 and len(neg_drivers) < 3:
                    neg_drivers.append({"feature": k, "label": FEATURE_LABELS.get(k, k), "shap_value": float(v), "direction": "decreases_risk"})
            
            result["top_shap_drivers"] = {
                "positive_drivers": pos_drivers,
                "negative_drivers": neg_drivers
            }
            
            result["recommended_action"] = self.get_recommended_action(pos_drivers)
            
        except Exception as e:
            result["time_status"] = "PREDICTION_ERROR"
            result["error_details"] = str(e)
            
        return result

prediction_service = PredictionService()
