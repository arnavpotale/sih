# PAIMANA AI: ML Data Audit Report

## 1. Dataset Dimensions
* **Total unique projects:** 20 (Seed Dataset extracted from `paimanaData.js`)
* **Historical observations per project:** 0 (Only cross-sectional current state snapshots exist)
* **Total available observations:** 20
* **Available milestones tracking:** Aggregated metrics only (Total vs Achieved), no historical progression.
* **Available expenditure records:** Current cumulative `expenditureCr` only, no monthly drawdown history.
* **Available progress records:** Current cumulative `physicalProgress` and `financialProgress` only.

## 2. Available Fields (From PostgreSQL Schema & JSON)
* **Project Identifiers:** `id`, `name`, `agency`
* **Categorical/Grouping:** `ministry`, `sector`, `hmlCategory`, `state`, `isMega`
* **Financials (Snapshot):** `originalCostCr`, `revisedCostCr`, `expenditureCr`
* **Schedule (Snapshot):** `approvalDate`, `startDate`, `originalTargetDoC`, `revisedDoC`, `delayMonths`
* **Progress (Snapshot):** `physicalProgress`, `financialProgress`
* **CUF Specifics:** `landAcquiredPct`, `clearancesObtainedPct`, `contractorsActive`, `criticalMilestonesTotal`, `criticalMilestonesAchieved`
* **Text/AI Helpers:** `primaryDrivers`, `aiDiagnosis`, `aiPrescription` (Not usable as input features due to leakage/generation).

## 3. Missing Value Percentages
* Across the 20 sample projects, structural completeness is extremely high (0% missing for core financial/schedule/progress metrics).
* Minor missing values exist in `cufAttributes` across some non-infrastructure sectors (e.g. `landAcquiredPct` may be irrelevant/null for pure software/equipment rollouts), but it is heavily populated for major infra projects.

## 4. Potential Target Variables
* `cost_overrun_pct = (revisedCostCr - originalCostCr) / originalCostCr`
* `is_significant_cost_overrun = 1 if cost_overrun_pct > 0.10 else 0`
* `time_delay_months = delayMonths` (Derived target based on `revisedDoC` vs `originalTargetDoC`)
* `is_time_overrun = 1 if delayMonths > 6 else 0`

## 5. Potential Leakage Variables
* `revisedCostCr`: Cannot be used as an input feature for predicting cost overrun, as it *is* the target outcome.
* `revisedDoC`: Cannot be used to predict schedule delays (it implicitly holds the answer).
* `delayMonths`: Cannot be used to predict time overrun probability (it is the exact outcome variable).
* `riskScore` / `riskLevel`: Cannot be used as features; they are rule-based heuristics currently calculated using the targets.

## 6. Fields Usable for Prediction (Available at Time=T)
* **AVAILABLE:** `originalCostCr`, `agency`, `ministry`, `sector`, `hmlCategory`, `state`, `isMega`
* **AVAILABLE:** `physicalProgress`, `financialProgress`, `expenditureCr` (Assuming these represent Time=T snapshots)
* **AVAILABLE:** `landAcquiredPct`, `clearancesObtainedPct`, `contractorsActive`, `criticalMilestonesTotal`, `criticalMilestonesAchieved`
* **DERIVABLE:** `project_age_months` (Current Date - `startDate`), `progress_gap` (`financialProgress` - `physicalProgress`), `milestone_completion_rate` (`criticalMilestonesAchieved` / `criticalMilestonesTotal`)

## 7. Fields Unavailable & Data Requirements
* **UNAVAILABLE:** Historical monthly snapshots (e.g. "What was the physical progress at Month 12?").
* **UNAVAILABLE:** Feature velocity (e.g. `expenditure_velocity_3_months`).

## 8. Feasibility Analysis
* **Is cost-overrun prediction currently feasible?** Yes, as a cross-sectional classification task (Predicting which projects currently have high cost overruns based on their current progress gap and CUF metrics). However, genuine longitudinal *early-warning* prediction is impossible without historical snapshots.
* **Is time-overrun prediction currently feasible?** Yes, similarly as a cross-sectional task.
* **Is early-warning backtesting currently feasible?** **NO.** We have zero historical snapshot data. We cannot calculate "lead time" because we do not know at what month a project officially breached its baseline.
* **Recommended data requirements for production:** To satisfy SIH constraints, we MUST generate a **Synthetic Historical Longitudinal Dataset** simulating the monthly progression of these 20 projects over time (e.g. Month 1 to Month N) to train an authentic early-warning model that tests *future* outcomes based on *past* features.
