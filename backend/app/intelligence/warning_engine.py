import pandas as pd
import uuid
from datetime import datetime

def generate_warnings(row: pd.Series, risk_data: dict) -> list:
    """
    Programmatically maps feature thresholds to explicit Early Warnings.
    """
    warnings = []
    project_id = row.get('id', 'Unknown')
    
    # Cost Warning
    if row.get('cost_escalation_ratio', 1.0) > 1.1:
        warnings.append({
            "id": str(uuid.uuid4()),
            "project_id": project_id,
            "severity": "HIGH",
            "warning_type": "COST_RISK",
            "trigger": f"Cost escalation of {round((row['cost_escalation_ratio']-1)*100, 1)}% detected.",
            "explanation": "The revised cost has significantly exceeded the original sanctioned cost.",
            "recommended_action": "Conduct immediate financial audit and require implementing agency to submit revised funding justification.",
            "created_at": datetime.utcnow().isoformat()
        })
        
    # Schedule Warning
    if row.get('schedule_elapsed_ratio', 0.0) > 1.0 and row.get('physicalProgress', 0) < 95:
        warnings.append({
            "id": str(uuid.uuid4()),
            "project_id": project_id,
            "severity": "HIGH",
            "warning_type": "SCHEDULE_RISK",
            "trigger": "Original planned duration elapsed but physical progress is incomplete.",
            "explanation": "The project is fundamentally delayed beyond its original sanctioned completion date.",
            "recommended_action": "Review critical path blockers and issue show-cause notice for delay.",
            "created_at": datetime.utcnow().isoformat()
        })
        
    # Divergence Warning
    gap = row.get('progress_gap', 0.0)
    if gap > 15:
        warnings.append({
            "id": str(uuid.uuid4()),
            "project_id": project_id,
            "severity": "MEDIUM",
            "warning_type": "PROGRESS_DIVERGENCE",
            "trigger": f"Financial progress ({row.get('financialProgress',0)}%) exceeds Physical progress ({row.get('physicalProgress',0)}%).",
            "explanation": "Fund utilization is outpacing actual ground implementation.",
            "recommended_action": "Pause next tranche release pending physical verification of works.",
            "created_at": datetime.utcnow().isoformat()
        })
        
    # Anomaly Warning
    anomaly = row.get('anomaly_score', 0.0)
    if anomaly > 0.75:
        warnings.append({
            "id": str(uuid.uuid4()),
            "project_id": project_id,
            "severity": "MEDIUM",
            "warning_type": "ANOMALY",
            "trigger": "Unusual implementation pattern detected by Isolation Forest.",
            "explanation": "The project's financial and physical metrics deviate significantly from standard baseline projects.",
            "recommended_action": "Conduct a manual review of project execution parameters.",
            "created_at": datetime.utcnow().isoformat()
        })
        
    return warnings
