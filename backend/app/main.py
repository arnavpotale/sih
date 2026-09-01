from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import projects, interventions, intelligence, reports
from app.models.report import Report
from app.models.project_snapshot import ProjectSnapshot
from app.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PAIMANA AI Backend API",
    version="1.0.0"
)

# Setup CORS to allow React frontend (running on port 5173/5174) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(projects.router)
app.include_router(interventions.router)
app.include_router(intelligence.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "Welcome to PAIMANA AI API"}
