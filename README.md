# 🇮🇳 PAIMANA AI: Smart Project Monitoring & Decision-Support System
### Ministry of Statistics and Programme Implementation (MoSPI / IPMD)
**Smart India Hackathon (SIH 2026) | Problem Statement ID: SIH26103**

---

## 📌 Executive Summary

The **Infrastructure & Project Monitoring Division (IPMD)** of **MoSPI** monitors Central Sector Infrastructure Projects costing **₹150 crore and above** across 17 infrastructural Ministries/Departments.

Originally monitored via the **Online Computerised Monitoring System (OCMS)** since 2006, the platform transitioned into **Project Assessment, Infrastructure Monitoring and Analytics for Nation-building (PAIMANA)**.

This repository implements an **AI-powered decision-support system** that shifts project monitoring from *passive descriptive reporting* to *proactive predictive and prescriptive intelligence*:
1. **Predicts** which infrastructure projects will experience schedule delays before they compound.
2. **Explains root-cause drivers** via SHAP feature attributions (e.g., schedule slip velocity, progress divergence).
3. **Prescribes administrative interventions** for line ministries and cabinet committees.

---

## 🚦 Current Status of the Project

The project is currently in a **stable, fully integrated state** following a selective feature merge and repository recovery. The system successfully binds a rich React frontend with a robust Python/FastAPI backend, operating against a real historical database (4 months of MoSPI Flash Reports). 

Recent milestones achieved:
- 3-Stakeholder Role Architecture (Govt, Bidder, Citizen) has been fully implemented.
- The PAI AI Copilot has been integrated with the Google Gemini API.
- The ML prediction pipeline (XGBoost + SHAP) has been restored and wired to the React UI, delivering live, data-driven insights without relying on mock data.

---

## 🌟 Core Features

### 1. 3-Role Gateway Architecture
A centralized entry portal routing users to specialized dashboards based on their roles:
- **Government Official Portal:** Executive oversight, AI risk radar, interventions, and GIS mapping.
- **Company / Bidder Portal:** Live E-Tender discovery, bidding criteria analysis, and project awards tracking.
- **Public Citizen Portal:** Transparency dashboards, civic feedback logging, and localized infrastructure impact mapping.

### 2. 🔴 AI Early Warning Risk Radar
- Real-time predictive risk scoring powered by an **XGBoost time-overrun model**.
- **SHAP (SHapley Additive exPlanations)** integration to surface top positive and negative drivers influencing a project's risk.
- Automated anomaly detection via **Isolation Forest** algorithms.

### 3. 🤖 PAI AI Assistant (Gemini LLM Copilot)
- Conversational intelligent assistant utilizing **Google's Gemini 2.5 Flash API**.
- Capable of answering complex infrastructure queries, filtering live E-Tenders, and drafting executive cabinet briefs by synthesizing real-time database context.

### 4. 🗺️ National Infrastructure GIS Map
- High-detail vector map of India highlighting regional infrastructure density.
- Interactive choropleth metrics for project counts, capital outlay, and cumulative disbursals.

### 5. 📋 Projects Registry & S-Curve Dossiers (Project X-Ray)
- Searchable ledger of all 1,981 central sector projects.
- "Project X-Ray" view detailing financial progress versus physical progress, schedule slippage, and AI-prescribed recommended actions.

### 6. 🛠️ Intervention Centre
- Closed-loop workflow allowing officials to create, track, and manage administrative interventions based on AI early warnings.

---

## 🏗️ System Architecture

PAIMANA AI follows a decoupled Client-Server architecture designed for scalability, real-time inference, and modularity.

1. **Presentation Layer (Frontend):** 
   - A Single Page Application (SPA) built with React and Vite. It manages localized state and role-based routing natively.
2. **Application Layer (Backend):** 
   - A high-performance Python FastAPI server acting as the central intelligence hub. It handles REST API routing (`/api/projects`, `/api/intelligence`), CORS, and request validation.
3. **Intelligence Layer (ML Engine):**
   - Embedded within the backend, this pipeline extracts temporal features from historical snapshots (`temporal_features.py`), feeds them into pre-trained Joblib models (`time_overrun_model.joblib`), and calculates SHAP attributions in real-time (`prediction_service.py`).
4. **Data Layer (Database):**
   - SQLite database managed via SQLAlchemy ORM, housing thousands of historical Flash Report snapshots, project metadata, and intervention logs.

---

## 🔄 User Flow (Government Official)

1. **Role Selection:** User arrives at the Landing Page and selects the "Government Official" role.
2. **Command Centre:** User is directed to the Executive Dashboard containing macro KPIs and the AI Predictive Radar.
3. **Prioritization:** The AI Risk Radar flags projects with a "HIGH" or "CRITICAL" risk of schedule deterioration.
4. **Project X-Ray:** The user clicks on a flagged project and enters the detailed dossier. 
5. **AI Early Warning Assessment:** The UI displays the precise XGBoost probability score and the SHAP Key Risk Drivers explaining *why* the project is delayed.
6. **Action Execution:** Based on the AI's prescriptive recommendation, the official clicks "Create Intervention" to dispatch a formal taskforce directive.

---

## 🛠️ Technology Stack

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Routing & State:** React Router / React Hooks
- **Styling:** CSS3, Sovereign GoI Design System themes
- **Icons:** Lucide React

### Backend
- **Framework:** FastAPI (Python 3.x)
- **ASGI Server:** Uvicorn
- **ORM:** SQLAlchemy
- **Database:** SQLite (`paimana.db`)
- **Data Processing:** Pandas, NumPy
- **PDF Extraction:** PDFPlumber

### Artificial Intelligence & Machine Learning
- **Predictive Modeling:** XGBoost (`xgboost`)
- **Model Interpretability:** SHAP (`shap` TreeExplainer)
- **Anomaly Detection:** Scikit-Learn (`IsolationForest`)
- **Large Language Model (LLM):** Google Gemini 2.5 Flash API (via REST Payload)
- **Model Serialization:** Joblib

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/arnavpotale/sih.git
cd PAIMANA-AI-SIH2026-main
```

### 2. Frontend Setup
```bash
# Install NPM dependencies
npm install

# Run the React development server
npm run dev
```

### 3. Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python requirements
pip install -r requirements.txt

# Start the FastAPI server (Runs on http://localhost:8000)
uvicorn app.main:app --reload
```

---

## 👥 Collaboration & Contributing

1. Fork or clone the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add feature description"`
4. Push to branch: `git push origin feature/your-feature-name`
5. Submit a Pull Request.

---

## 📜 License & Acknowledgements
Developed for **Smart India Hackathon (SIH 2026)**.  
Data referenced from **Ministry of Statistics and Programme Implementation (MoSPI / IPMD)**.
