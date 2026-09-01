import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100, 
            max_samples='auto', 
            contamination=0.1, # Assume 10% of projects are highly anomalous
            random_state=42
        )
        self.is_trained = False
        
    def train(self, df: pd.DataFrame):
        """Trains the isolation forest on numerical features."""
        features = self._extract_features(df)
        if len(features) > 0:
            self.model.fit(features)
            self.is_trained = True
            
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """Returns the anomaly scores. Lower/negative scores indicate higher abnormality."""
        if not self.is_trained:
            self.train(df) # Auto-train on available dataset if not trained
            
        features = self._extract_features(df)
        if len(features) == 0:
            df['anomaly_score'] = 1.0
            return df
            
        # score_samples returns the opposite of the anomaly score defined in the original paper.
        # lower values indicates abnormality
        scores = self.model.score_samples(features)
        
        # Normalize scores to 0-1 range where 1 is highly anomalous
        # scores typically range from -1.0 to 0.5 depending on dataset
        min_score, max_score = min(scores), max(scores)
        if max_score > min_score:
            # Invert so higher = more anomalous
            normalized_scores = 1.0 - ((scores - min_score) / (max_score - min_score))
        else:
            normalized_scores = np.zeros(len(scores))
            
        df['anomaly_score'] = np.clip(normalized_scores, 0, 1)
        return df
        
    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        # Select columns that exist in the dataframe
        cols = ['progress_gap', 'cost_escalation_ratio', 'schedule_elapsed_ratio', 'milestone_ratio']
        available_cols = [c for c in cols if c in df.columns]
        
        if not available_cols:
            return np.array([])
            
        # Fill NA with medians to prevent training crash
        X = df[available_cols].copy()
        X = X.fillna(X.median())
        return X.values

anomaly_detector = AnomalyDetector()
