# PAIMANA AI: Feature Catalog & Leakage Audit

This document outlines the variables intended for use in the PAIMANA ML Pipeline, categorizing them by source and explicitly identifying data leakage risks.

## Base / Demographics Features

| Feature | Source | Available at prediction time? | Leakage Reason |
| :--- | :--- | :--- | :--- |
| `originalCostCr` | DB / CUF | Yes | Static baseline budget. |
| `ministry` | DB | Yes | Known at project inception. |
| `sector` | DB | Yes | Known at project inception. |
| `isMega` | Derived (`originalCostCr` >= 1000) | Yes | Based purely on baseline budget. |
| `project_age_months` | Derived (Current Date - `startDate`) | Yes | Time elapsed is always known. |

## Financial Features

| Feature | Source | Available at prediction time? | Leakage Reason |
| :--- | :--- | :--- | :--- |
| `financialProgress` | DB | Yes | Current snapshot of disbursed funds vs original cost. |
| `expenditure_ratio` | Derived (`expenditureCr` / `originalCostCr`) | Yes | Uses only currently approved funds. |
| `revisedCostCr` | DB | **NO** | Leakage: This is the exact target variable for cost overruns. |

## Physical & Schedule Features

| Feature | Source | Available at prediction time? | Leakage Reason |
| :--- | :--- | :--- | :--- |
| `physicalProgress` | DB / CUF | Yes | Monthly snapshot reported by implementing agency. |
| `progress_gap` | Derived (`financialProgress` - `physicalProgress`) | Yes | Represents current burn rate vs actual ground completion. |
| `milestone_completion_rate` | Derived (`criticalMilestonesAchieved` / `criticalMilestonesTotal`) | Yes | Real-time metric of schedule friction. |
| `revisedDoC` | DB | **NO** | Leakage: Contains the final/current anticipated completion date. |
| `delayMonths` | DB | **NO** | Leakage: Exact target variable for time overruns. |

## External & Friction Features (CUF)

| Feature | Source | Available at prediction time? | Leakage Reason |
| :--- | :--- | :--- | :--- |
| `landAcquiredPct` | DB / CUF | Yes | Reported monthly snapshot representing site readiness. |
| `clearancesObtainedPct` | DB / CUF | Yes | Reported monthly snapshot of regulatory friction. |
| `contractorsActive` | DB / CUF | Yes | Represents current workforce scale/liquidity. |

## Post-Event Variables (Must Exclude)

| Feature | Source | Available at prediction time? | Leakage Reason |
| :--- | :--- | :--- | :--- |
| `riskScore` | API (Rule Engine) | **NO** | Heuristic derived from targets; causes cyclical leakage. |
| `riskLevel` | API (Rule Engine) | **NO** | Derived from `riskScore`. |
| `aiDiagnosis` | LLM / Static | **NO** | Written retrospectively referencing actual delays/costs. |
| `aiPrescription` | LLM / Static | **NO** | Written retrospectively referencing actual delays/costs. |

## Conclusion
To predict future events, we MUST use features that do not embed knowledge of the delay itself. 

The most powerful predictive features for our models will be:
1. `progress_gap` (Financial > Physical progress = cost leakage indicator).
2. `landAcquiredPct` & `clearancesObtainedPct` (Pre-requisites to heavy capital deployment).
3. `milestone_completion_rate` (Micro-timeline adherence).
