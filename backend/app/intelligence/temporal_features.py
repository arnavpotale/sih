import pandas as pd
import numpy as np

def build_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    
    # Sort by project_code and reporting_month
    month_map = {'April': 4, 'May': 5, 'June': 6, 'July': 7}
    df['month_num'] = df['reporting_month'].map(month_map)
    df = df.sort_values(['project_code', 'reporting_year', 'month_num']).reset_index(drop=True)
    
    # Date parsing
    def parse_dt(series): return pd.to_datetime(series, format='%m/%Y', errors='coerce')
    df['prediction_date'] = pd.to_datetime(df['reporting_month'] + ' ' + df['reporting_year'].astype(str), format='%B %Y', errors='coerce')
    df['start_dt'] = parse_dt(df['start_date'])
    df['original_end_dt'] = parse_dt(df['original_end_date'])
    df['revised_end_dt'] = parse_dt(df['revised_end_date'])
    
    # Fill NAs mathematically defensible
    df['original_cost'] = df['original_cost'].fillna(1.0) # Avoid div by zero
    df['revised_cost'] = df['revised_cost'].fillna(df['original_cost'])
    df['expenditure'] = df['expenditure'].fillna(0.0)
    df['physical_progress'] = df['physical_progress'].fillna(0.0)
    
    # CURRENT STATE
    df['current_revised_cost'] = df['revised_cost']
    df['current_cost_escalation_amount'] = df['current_revised_cost'] - df['original_cost']
    df['current_cost_escalation_percent'] = (df['current_cost_escalation_amount'] / df['original_cost']).replace([np.inf, -np.inf], 0)
    df['cumulative_expenditure'] = df['expenditure']
    df['expenditure_ratio'] = (df['cumulative_expenditure'] / df['current_revised_cost']).replace([np.inf, -np.inf], 0)
    
    df['project_age_days'] = (df['prediction_date'] - df['start_dt']).dt.days.fillna(0)
    df['planned_duration_days'] = (df['original_end_dt'] - df['start_dt']).dt.days.fillna(365)
    df['schedule_slip_days'] = (df['revised_end_dt'] - df['original_end_dt']).dt.days.fillna(0)
    
    # LAG FEATURES
    grouped = df.groupby('project_code')
    df['previous_expenditure'] = grouped['cumulative_expenditure'].shift(1)
    df['previous_revised_cost'] = grouped['current_revised_cost'].shift(1)
    df['previous_physical_progress'] = grouped['physical_progress'].shift(1)
    df['previous_revised_DoC'] = grouped['revised_end_dt'].shift(1)
    
    # CHANGE FEATURES
    df['expenditure_delta'] = df['cumulative_expenditure'] - df['previous_expenditure'].fillna(df['cumulative_expenditure'])
    df['cost_revision_delta'] = df['current_revised_cost'] - df['previous_revised_cost'].fillna(df['current_revised_cost'])
    df['physical_progress_delta'] = df['physical_progress'] - df['previous_physical_progress'].fillna(df['physical_progress'])
    df['schedule_change_delta_days'] = (df['revised_end_dt'] - df['previous_revised_DoC'].fillna(df['revised_end_dt'])).dt.days.fillna(0)
    
    # TIME DELTA for velocity (approx months between reports, usually 1)
    df['previous_prediction_date'] = grouped['prediction_date'].shift(1)
    df['time_delta_months'] = (df['prediction_date'].dt.year - df['previous_prediction_date'].dt.year) * 12 + \
                              (df['prediction_date'].dt.month - df['previous_prediction_date'].dt.month)
    df['time_delta_months'] = df['time_delta_months'].replace(0, 1).fillna(1) # default to 1 month for initial row
    
    # VELOCITY
    df['expenditure_velocity'] = df['expenditure_delta'] / df['time_delta_months']
    df['cost_revision_velocity'] = df['cost_revision_delta'] / df['time_delta_months']
    df['physical_progress_velocity'] = df['physical_progress_delta'] / df['time_delta_months']
    df['schedule_slip_velocity'] = df['schedule_change_delta_days'] / df['time_delta_months']
    
    # DERIVED
    df['remaining_physical_progress'] = 100.0 - df['physical_progress']
    df['remaining_duration_days'] = (df['revised_end_dt'] - df['prediction_date']).dt.days.fillna(0)
    df['cost_to_progress_ratio'] = (df['expenditure_ratio'] / (df['physical_progress'] / 100.0).replace(0, 0.01)).replace([np.inf, -np.inf], 0)
    df['expenditure_to_progress_ratio'] = (df['cumulative_expenditure'] / df['physical_progress'].replace(0, 0.01)).replace([np.inf, -np.inf], 0)
    
    # Acceleration / Deceleration
    df['previous_progress_velocity'] = grouped['physical_progress_velocity'].shift(1).fillna(0)
    df['progress_velocity_deceleration'] = df['previous_progress_velocity'] - df['physical_progress_velocity']
    
    return df
