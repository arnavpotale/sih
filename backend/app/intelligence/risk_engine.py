import pandas as pd
import numpy as np

def calculate_composite_risk(row: pd.Series) -> dict:
    """
    Calculates a transparent analytical risk score based on
    feature-engineered variables and anomaly scores.
    """
    score = 0.0
    indicators = []
    
    # 1. Cost Risk (0 to 30 points)
    cost_ratio = row.get('cost_escalation_ratio', 1.0)
    if cost_ratio > 1.2:
        score += 30
        indicators.append({"feature": "Cost Escalation", "impact": "+30", "direction": "High cost overrun detected"})
    elif cost_ratio > 1.05:
        score += 15
        indicators.append({"feature": "Cost Pressure", "impact": "+15", "direction": "Moderate cost pressure"})
        
    # 2. Schedule Risk (0 to 30 points)
    schedule_ratio = row.get('schedule_elapsed_ratio', 0.0)
    if schedule_ratio > 1.2:
        score += 30
        indicators.append({"feature": "Schedule Slippage", "impact": "+30", "direction": "Severe time overrun"})
    elif schedule_ratio > 0.9 and row.get('physicalProgress', 0) < 80:
        score += 20
        indicators.append({"feature": "Schedule Pressure", "impact": "+20", "direction": "High time elapsed vs progress"})

    # 3. Progress Divergence (0 to 20 points)
    gap = row.get('progress_gap', 0.0) # Financial - Physical
    if gap > 20:
        score += 20
        indicators.append({"feature": "Progress Divergence", "impact": "+20", "direction": "Financial progress exceeds physical by >20%"})
    elif gap > 10:
        score += 10
        indicators.append({"feature": "Progress Divergence", "impact": "+10", "direction": "Financial progress exceeds physical by >10%"})

    # 4. Anomaly Risk (0 to 20 points)
    anomaly = row.get('anomaly_score', 0.0)
    if anomaly > 0.8:
        score += 20
        indicators.append({"feature": "Anomaly Detected", "impact": "+20", "direction": "Unusual implementation pattern compared to peers"})
    elif anomaly > 0.6:
        score += 10
        indicators.append({"feature": "Elevated Anomaly Score", "impact": "+10", "direction": "Minor deviation in project parameters"})

    # Cap score at 100
    final_score = min(score, 100)
    
    # Determine level
    if final_score >= 70:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    elif final_score > 20:
        level = "WATCH"
    else:
        level = "LOW"
        
    return {
        "overall_score": int(final_score),
        "risk_level": level,
        "indicators": indicators,
        "cost_risk_probability": round(min(cost_ratio - 1, 1) * 100, 1) if cost_ratio > 1 else 0.0,
        "schedule_risk_probability": round(min(schedule_ratio - 1, 1) * 100, 1) if schedule_ratio > 1 else 0.0
    }
