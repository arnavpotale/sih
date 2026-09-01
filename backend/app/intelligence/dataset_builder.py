import pandas as pd
from app.db.database import SessionLocal
from app.models.project_snapshot import ProjectSnapshot
from app.intelligence.temporal_features import build_temporal_features
from app.intelligence.target_engine import build_targets
from app.intelligence.leakage_audit import audit_leakage

def load_snapshots() -> pd.DataFrame:
    db = SessionLocal()
    try:
        snapshots = db.query(ProjectSnapshot).all()
        data = [{
            'project_code': s.project_code,
            'reporting_month': s.reporting_month,
            'reporting_year': s.reporting_year,
            'name': s.name,
            'agency': s.agency,
            'state': s.state,
            'start_date': s.start_date,
            'original_cost': s.original_cost,
            'revised_cost': s.revised_cost,
            'expenditure': s.expenditure,
            'original_end_date': s.original_end_date,
            'revised_end_date': s.revised_end_date,
            'physical_progress': s.physical_progress
        } for s in snapshots]
        return pd.DataFrame(data)
    finally:
        db.close()

def build_datasets():
    """
    Builds the cost and time temporal ML datasets.
    Drops rows where the target is UNKNOWN (e.g., July).
    Returns cost_df, time_df, safe_features, metadata
    """
    df = load_snapshots()
    if df.empty:
        return df, df, [], {}
        
    df = build_temporal_features(df)
    df = build_targets(df)
    
    all_features = df.columns.tolist()
    safe_features, unsafe_features = audit_leakage(all_features, ['cost_target', 'time_target'])
    
    metadata = {
        "snapshots_processed": len(df),
        "unique_projects": df['project_code'].nunique(),
        "total_features_generated": len(all_features),
        "safe_features_count": len(safe_features),
        "unsafe_features_count": len(unsafe_features),
        "unsafe_features": unsafe_features,
        "prediction_horizon": "Option A: Next-observation (1 month ahead)",
        "cost_baseline_A": "Always predict 0 (no deterioration)",
        "cost_baseline_B": "Predict 1 if current_cost_escalation_amount > 0",
        "time_baseline_A": "Always predict 1 (delay)",
        "time_baseline_B": "Predict 1 if schedule_slip_days > 0",
        "temporal_split": {
            "train": ["April", "May"],
            "validation": ["June"],
            "test": "EXPERIMENTAL_VALIDATION_ONLY (Insufficient out-of-time data)"
        }
    }
    
    # Cost dataset
    cost_df = df.dropna(subset=['cost_target']).copy()
    cost_metadata = {
        "rows": len(cost_df),
        "positive_cases": int(cost_df['cost_target'].sum()),
        "negative_cases": int(len(cost_df) - cost_df['cost_target'].sum())
    }
    metadata["cost_dataset"] = cost_metadata
    
    # Time dataset
    time_df = df.dropna(subset=['time_target']).copy()
    time_metadata = {
        "rows": len(time_df),
        "positive_cases": int(time_df['time_target'].sum()),
        "negative_cases": int(len(time_df) - time_df['time_target'].sum())
    }
    metadata["time_dataset"] = time_metadata
    
    # Return the datasets keeping safe features and target, plus project code/month for tracking
    cost_cols = ['project_code', 'reporting_month', 'reporting_year'] + safe_features + ['cost_target']
    time_cols = ['project_code', 'reporting_month', 'reporting_year'] + safe_features + ['time_target']
    
    return cost_df[cost_cols], time_df[time_cols], safe_features, metadata

def get_latest_features(project_code: str) -> dict:
    """
    Retrieves the latest available observation for a project and calculates
    all temporal features natively, returning a dictionary.
    Returns None if the project does not exist or has insufficient data.
    """
    df = load_snapshots()
    if df.empty:
        return None
        
    project_df = df[df['project_code'] == project_code].copy()
    if len(project_df) == 0:
        return None
        
    # We must calculate features on the whole df to ensure lags are correct for all time,
    # but to be efficient, we could just filter to this project_code before building features.
    project_df = build_temporal_features(project_df)
    
    # We only care about the most recent observation
    latest = project_df.sort_values(['reporting_year', 'month_num']).iloc[-1]
    
    return latest.to_dict()

def get_all_latest_features() -> pd.DataFrame:
    """
    Efficiently computes the latest features for all projects.
    """
    df = load_snapshots()
    if df.empty:
        return df
        
    df = build_temporal_features(df)
    # Sort and take the last observation per project
    latest_df = df.sort_values(['reporting_year', 'month_num']).groupby('project_code').tail(1)
    return latest_df
