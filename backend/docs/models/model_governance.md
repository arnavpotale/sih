# Model Governance Document (Sprint 5F)

## 1. Problem Definition
Predict near-term schedule deterioration to support early warning interventions.

## 2. Target Definition
- **Target:** Revised completion date at T+1 is strictly later than the revised completion date at T.

## 3. Prediction Horizon
Next observed reporting period (1 Month Ahead).

## 4. Data Source
Four monthly Flash Reports (April, May, June, July 2026) published by MoSPI.

## 5. Feature Engineering
26 temporal and dynamic features calculated representing current state, velocities, and ratios.

## 6. Leakage Prevention
Strict chronological validation to prevent peeking into the future (e.g. June data cannot be used to predict May outcomes). All future-looking variables were audited and stripped.

## 7. Temporal Split
- **Training Period:** April $\to$ May, May $\to$ June
- **Validation Period:** June $\to$ July

## 8. Model Selection & 9. Baseline Comparison
- **Cost:** NO USEFUL MODEL (Best ML scored F1=0.060, beaten by naive baseline F1=0.121).
- **Time:** XGBoost selected (F1=0.537, beating naive baseline F1=0.310).

## 10. XGBoost Performance (Time)
Precision = 0.464, Recall = 0.637, F1 = 0.537, ROC-AUC = 0.805

## 11. Rolling Validation (Time)
- April $\to$ May: F1=0.464, ROC-AUC=0.762
- May $\to$ June: F1=0.348, ROC-AUC=0.684

## 12. Threshold Selection
Threshold = 0.50 (Selected to maximize recall for early warning purposes).

## 13. SHAP Methodology
TreeExplainer is used to calculate marginal contributions. Top 3 positive and negative features are mapped to readable text.

## 14. Known Limitations
Four monthly reports provide an experimental temporal validation framework but are entirely insufficient for claiming production-grade generalization. Cost deterioration structurally occurs rarely over a 1-month horizon (2%). 

## 15. Intended Use
Early warning prioritization to assist human officials in determining which projects require manual intervention.

## 16. Prohibited Interpretation
Users and system integrators are strictly prohibited from:
- Treating prediction as certainty
- Using output as automated administrative action
- Claiming causal explanations
- Claiming production-grade accuracy
- Using model outputs without human review
