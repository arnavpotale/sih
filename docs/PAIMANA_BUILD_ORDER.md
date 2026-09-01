# PAIMANA BUILD ORDER (Executive Summary)

This document dictates the exact phased build sequence to transform PAIMANA AI from a static frontend prototype into a predictive intelligence platform.

### PHASE 0 — Planning
* **Objective:** Establish a unified product vision and technical constraints.
* **Features:** N/A
* **Dependencies:** Deep audit of existing React/FastAPI codebase and data schemas.
* **Deliverables:** `PAIMANA_MASTER_IMPLEMENTATION_PLAN.md` and this document.
* **Completion Criteria:** Approval of the technical roadmap.

### PHASE 1 — Product Restructuring
* **Objective:** Shift the UI focus from "data-heavy reporting" to "action-oriented decision support."
* **Features:** Redesign Command Centre; restructure Navigation.
* **Dependencies:** None.
* **Deliverables:** Cleaned up UI components, removal of bloated statistics.
* **Completion Criteria:** A user landing on the dashboard immediately sees Priority Alerts rather than just a total project count.

### PHASE 2 — Backend/Data
* **Objective:** Prepare the data foundation for genuine Machine Learning.
* **Features:** Synthetic Longitudinal Data Generator, Database Schema expansion (Alerts, Interventions).
* **Dependencies:** SQLAlchemy, existing 20-project dataset.
* **Deliverables:** Python script outputting monthly historical snapshots for the 20 baseline projects.
* **Completion Criteria:** A robust dataset exists capable of proving "Early Warning Lead Time."

### PHASE 3 — ML (Machine Learning)
* **Objective:** Replace heuristic fake AI with authentic predictive models.
* **Features:** XGBoost Cost/Time Overrun models, SHAP explanations, Model evaluation metrics.
* **Dependencies:** Phase 2 (Data).
* **Deliverables:** `backend/ml/` pipeline, trained `.pkl` artifacts, Prediction API endpoints.
* **Completion Criteria:** `ProjectXRay` UI renders SHAP feature contributions fetched directly from Python.

### PHASE 4 — Risk/Anomaly
* **Objective:** Implement unsupervised anomaly detection to flag irregular project behaviour.
* **Features:** Isolation Forest model, Risk aggregation engine.
* **Dependencies:** Phase 3.
* **Deliverables:** Anomaly detection API, integrated "Overall Risk Score".
* **Completion Criteria:** System can flag a project where financial progress drastically outweighs physical progress as an anomaly.

### PHASE 5 — Alerts/Intervention
* **Objective:** Turn ML predictions into actionable workflows.
* **Features:** Early Warning Alert generator, Intervention CRUD system.
* **Dependencies:** Phase 2, Phase 3, Phase 4.
* **Deliverables:** Alert tables, Intervention assignment UI.
* **Completion Criteria:** An official can assign a "Review Required" task to an agency based on an ML alert.

### PHASE 6 — Roles/Project Updates
* **Objective:** Allow closed-loop resolution of interventions.
* **Features:** Role-based views (Official vs Agency), Evidence upload, Progress update forms.
* **Dependencies:** Phase 5.
* **Deliverables:** Project Manager UI, file/evidence submission endpoints.
* **Completion Criteria:** A project manager can upload a clearance certificate and mark an intervention as resolved.

### PHASE 7 — Drishti/Simulation
* **Objective:** Implement the final AI polish securely.
* **Features:** CUF What-If Python Simulator, Drishti LLM Tool Calling.
* **Dependencies:** Phase 3 (for running what-if through the model), Phase 5 (for Drishti to read alerts).
* **Deliverables:** Langchain/Agent integration restricted to API tools.
* **Completion Criteria:** Drishti can accurately answer "Which projects in Maharashtra have active interventions?" without hallucinating.

### PHASE 8 — Testing/Polish
* **Objective:** Ensure extreme technical credibility for SIH judges.
* **Features:** End-to-end testing, error handling, final UI polish.
* **Dependencies:** Phase 1-7.
* **Deliverables:** Presentation-ready application, clean console, error boundaries.
* **Completion Criteria:** A judge can click through the entire intervention lifecycle flawlessly, and all ML numbers are technically defensible.
