def audit_leakage(features: list, targets: list) -> tuple[list, list]:
    """
    Time-aware leakage audit.
    A feature is SAFE if it represents the state up to and including time T.
    A feature is UNSAFE if it depends on information occurring after T (T+1, etc.).
    """
    unsafe_keywords = [
        'future_',        # Future values
        'final_',         # Final outcomes
        'target'          # Target variables or derived from targets
    ]
    
    # We must also exclude non-feature columns that are metadata
    metadata_cols = [
        'project_code', 'reporting_month', 'reporting_year', 'name', 
        'agency', 'state', 'start_date', 'original_end_date', 'revised_end_date',
        'prediction_date', 'start_dt', 'original_end_dt', 'revised_end_dt',
        'previous_prediction_date', 'previous_revised_DoC'
    ]
    
    unsafe_features = []
    safe_features = []
    
    for f in features:
        if f in metadata_cols:
            continue
            
        if f in targets:
            unsafe_features.append(f)
            continue
            
        is_unsafe = any(kw in f for kw in unsafe_keywords)
        
        if is_unsafe:
            unsafe_features.append(f)
        else:
            safe_features.append(f)
            
    return safe_features, unsafe_features
