import pandas as pd

def build_targets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs Option A (next-observation) targets for Cost and Time.
    T is current observation. T+1 is next observation.
    """
    if df.empty: return df
    
    # Ensure ordered by time
    grouped = df.groupby('project_code')
    
    # Future features (ONLY USED FOR TARGET CONSTRUCTION)
    df['future_revised_cost'] = grouped['current_revised_cost'].shift(-1)
    df['future_revised_end_dt'] = grouped['revised_end_dt'].shift(-1)
    
    # COST TARGET
    # 1 if future revised cost > current revised cost
    df['cost_target'] = (df['future_revised_cost'] > df['current_revised_cost']).astype(float)
    # NaN if no future observation
    df.loc[df['future_revised_cost'].isna(), 'cost_target'] = float('nan')
    
    # TIME TARGET
    # 1 if future revised end date > current revised end date
    df['time_target'] = (df['future_revised_end_dt'] > df['revised_end_dt']).astype(float)
    df.loc[df['future_revised_end_dt'].isna(), 'time_target'] = float('nan')
    
    return df
