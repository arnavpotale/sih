import pandas as pd
import numpy as np

def generate_features(projects: list[dict]) -> pd.DataFrame:
    """
    Given a list of project dictionaries, engineers meaningful features 
    for anomaly detection and risk scoring.
    """
    if not projects:
        return pd.DataFrame()
        
    df = pd.DataFrame(projects)
    
    # Fill defaults
    df['physicalProgress'] = df['physicalProgress'].fillna(0.0)
    df['financialProgress'] = df['financialProgress'].fillna(0.0)
    df['originalCostCr'] = df['originalCostCr'].fillna(1.0)
    df['revisedCostCr'] = df['revisedCostCr'].fillna(df['originalCostCr'])
    
    # 1. Progress Divergence (Financial Progress vs Physical Progress)
    df['progress_gap'] = df['financialProgress'] - df['physicalProgress']
    
    # 2. Cost Pressure (Revised / Original)
    # Avoid zero division
    df['originalCostCr'] = np.where(df['originalCostCr'] == 0, 1.0, df['originalCostCr'])
    df['cost_escalation_ratio'] = df['revisedCostCr'] / df['originalCostCr']
    
    # 3. Time Parsing
    def parse_months(date_str):
        if pd.isna(date_str):
            return pd.NaT
        try:
            return pd.to_datetime(date_str, format='%m/%Y')
        except:
            return pd.NaT

    df['start_dt'] = df['startDate'].apply(parse_months)
    df['original_end_dt'] = df['originalTargetDoC'].apply(parse_months)
    df['revised_end_dt'] = df['revisedDoC'].apply(parse_months)
    
    # Current date assumption (for prototyping we use a fixed max or current time)
    current_date = pd.to_datetime('2026-09-01')
    
    # 4. Schedule Pressure
    # Elapsed duration in months
    df['elapsed_months'] = ((current_date - df['start_dt']) / pd.Timedelta(days=30)).fillna(0)
    df['elapsed_months'] = np.maximum(df['elapsed_months'], 0) # Prevent negative
    
    # Planned duration in months
    df['planned_months'] = ((df['original_end_dt'] - df['start_dt']) / pd.Timedelta(days=30)).fillna(1)
    df['planned_months'] = np.maximum(df['planned_months'], 1) # Prevent zero
    
    df['schedule_elapsed_ratio'] = df['elapsed_months'] / df['planned_months']
    
    # Calculate milestone completion ratio if cufAttributes exist
    def get_milestone_ratio(cuf):
        if isinstance(cuf, dict):
            total = cuf.get('criticalMilestonesTotal', 0)
            achieved = cuf.get('criticalMilestonesAchieved', 0)
            if total > 0:
                return achieved / total
        return 0.0

    df['milestone_ratio'] = df['cufAttributes'].apply(get_milestone_ratio)
    
    return df
