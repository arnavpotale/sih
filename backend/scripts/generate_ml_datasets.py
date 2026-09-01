import os
import sys
import json
import logging
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.intelligence.dataset_builder import build_datasets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_datasets():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/ml'))
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info("Building datasets...")
    cost_df, time_df, safe_features, metadata = build_datasets()
    
    if cost_df.empty or time_df.empty:
        logger.error("Failed to build datasets. Missing data.")
        return
        
    cost_csv = os.path.join(output_dir, 'cost_dataset.csv')
    time_csv = os.path.join(output_dir, 'time_dataset.csv')
    meta_json = os.path.join(output_dir, 'dataset_metadata.json')
    
    logger.info(f"Saving {cost_csv}...")
    cost_df.to_csv(cost_csv, index=False)
    
    logger.info(f"Saving {time_csv}...")
    time_df.to_csv(time_csv, index=False)
    
    metadata['creation_timestamp'] = datetime.utcnow().isoformat()
    logger.info(f"Saving {meta_json}...")
    with open(meta_json, 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print("\n--- LABEL VALIDATION ---")
    
    def validate_random(df, target_col, name, condition, count=10):
        subset = df[df[target_col] == condition]
        if subset.empty: return
        sample = subset.sample(min(len(subset), count))
        print(f"\n{name} ({len(subset)} total):")
        for _, row in sample.iterrows():
            print(f"  Project: {row['project_code']} | Month: {row['reporting_month']} | Target: {row[target_col]}")
            
    print("\nCOST LABELS:")
    validate_random(cost_df, 'cost_target', 'Positive Cost Deterioration (1.0)', 1.0)
    validate_random(cost_df, 'cost_target', 'Negative Cost Deterioration (0.0)', 0.0)
    
    print("\nTIME LABELS:")
    validate_random(time_df, 'time_target', 'Positive Schedule Deterioration (1.0)', 1.0)
    validate_random(time_df, 'time_target', 'Negative Schedule Deterioration (0.0)', 0.0)
    
    print("\n--- CLASS DISTRIBUTION ---")
    print(f"Cost Dataset Total Rows: {len(cost_df)}")
    print(f" Positive (1.0): {cost_df['cost_target'].sum()} ({cost_df['cost_target'].mean()*100:.2f}%)")
    print(f" Negative (0.0): {len(cost_df) - cost_df['cost_target'].sum()}")
    
    print(f"\nTime Dataset Total Rows: {len(time_df)}")
    print(f" Positive (1.0): {time_df['time_target'].sum()} ({time_df['time_target'].mean()*100:.2f}%)")
    print(f" Negative (0.0): {len(time_df) - time_df['time_target'].sum()}")
    
    print("\n--- TEMPORAL FEASIBILITY ---")
    print(f"Train: April, May")
    print(f"Validation: June")
    print(f"Test: {metadata['temporal_split']['test']}")

if __name__ == "__main__":
    generate_datasets()
