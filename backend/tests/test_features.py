import pytest
import pandas as pd
from ml.features import extract_features

def test_extract_features_empty():
    df = extract_features([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_extract_features_basic():
    sample_project = {
        "id": "101",
        "originalCostCr": 100.0,
        "revisedCostCr": 120.0,
        "physicalProgress": 40.0,
        "financialProgress": 60.0,
        "delayMonths": 8,
        "isMega": False,
        "sector": "Railways",
        "cufAttributes": {
            "landAcquiredPct": 50.0,
            "criticalMilestonesTotal": 10,
            "criticalMilestonesAchieved": 5
        }
    }
    
    df = extract_features([sample_project])
    
    assert len(df) == 1
    
    # Check basic assignments
    assert df.iloc[0]["originalCostCr"] == 100.0
    assert df.iloc[0]["isMega"] == 0
    assert df.iloc[0]["sector"] == "Railways"
    
    # Check derived fields
    assert df.iloc[0]["progress_gap"] == 20.0  # 60 - 40
    assert df.iloc[0]["milestone_completion_rate"] == 0.5  # 5 / 10
    
    # Check targets
    assert df.iloc[0]["target_cost_overrun"] == 1  # (120 - 100)/100 = 20% > 10%
    assert df.iloc[0]["target_time_overrun"] == 1  # 8 months > 6 months

def test_extract_features_no_progress_gap():
    # If physical > financial, gap should be 0, not negative
    sample_project = {
        "physicalProgress": 80.0,
        "financialProgress": 50.0
    }
    df = extract_features([sample_project])
    assert df.iloc[0]["progress_gap"] == 0.0
