import pandas as pd
from typing import List, Dict, Any

def extract_features(projects: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transforms raw project dictionaries into a feature matrix suitable for ML.
    Safely handles missing values and derives calculated fields while avoiding data leakage.
    """
    df = pd.DataFrame(projects)

    # If empty, return empty dataframe
    if df.empty:
        return pd.DataFrame()

    features_list = []

    for _, row in df.iterrows():
        # Base attributes
        original_cost = float(row.get('originalCostCr') or 0.0)
        
        # We cap financial progress at 150% to prevent extreme outliers skewing models
        financial_progress = min(float(row.get('financialProgress') or 0.0), 150.0)
        physical_progress = float(row.get('physicalProgress') or 0.0)
        
        # Core derived feature: Progress Gap
        # High gap (Financial >> Physical) implies heavy cost leakage without ground completion.
        progress_gap = max(0.0, financial_progress - physical_progress)

        # CUF Attributes Extraction
        cuf = row.get('cufAttributes') or {}
        land_acquired_pct = float(cuf.get('landAcquiredPct') or 0.0)
        clearances_pct = float(cuf.get('clearancesObtainedPct') or 0.0)
        
        # Milestone tracking
        milestones_total = int(cuf.get('criticalMilestonesTotal') or 1)
        milestones_achieved = int(cuf.get('criticalMilestonesAchieved') or 0)
        milestone_completion_rate = milestones_achieved / max(1, milestones_total)

        # Categorical features can be label-encoded or one-hot encoded later, 
        # but we extract them cleanly here.
        sector = row.get('sector', 'Unknown')
        is_mega = int(row.get('isMega', False))

        # Target definitions (Included here for training pipeline convenience, 
        # but NOT used as inputs for prediction).
        # In a real setup, labels.py would handle this separately, but we include targets 
        # in the extracted dataframe for easy train_test_split downstream.
        revised_cost = float(row.get('revisedCostCr') or original_cost)
        cost_overrun_pct = (revised_cost - original_cost) / max(1.0, original_cost)
        
        delay_months = int(row.get('delayMonths') or 0)

        # We define a "significant cost overrun" as > 10%
        target_cost_overrun = 1 if cost_overrun_pct > 0.10 else 0
        
        # We define a "significant time delay" as > 6 months
        target_time_overrun = 1 if delay_months > 6 else 0

        features = {
            'project_id': row.get('id'),
            
            # Features
            'originalCostCr': original_cost,
            'isMega': is_mega,
            'physicalProgress': physical_progress,
            'financialProgress': financial_progress,
            'progress_gap': progress_gap,
            
            'landAcquiredPct': land_acquired_pct,
            'clearancesObtainedPct': clearances_pct,
            'milestone_completion_rate': milestone_completion_rate,
            
            # Categoricals to encode downstream
            'sector': sector,
            
            # Targets (Do NOT use as inputs)
            'target_cost_overrun': target_cost_overrun,
            'target_time_overrun': target_time_overrun,
            'actual_delay_months': delay_months,
            'actual_cost_overrun_pct': cost_overrun_pct
        }
        
        features_list.append(features)

    return pd.DataFrame(features_list)
