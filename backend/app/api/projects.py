from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectResponse, DashboardSummaryResponse

router = APIRouter(prefix="/api", tags=["Projects"])

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = Query(default=100, le=2000),
    ministry: str = None,
    sector: str = None
):
    query = db.query(Project)
    if ministry:
        query = query.filter(Project.ministry == ministry)
    if sector:
        query = query.filter(Project.sector == sector)
        
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    # Basic aggregation logic using DB counts (Phase 1)
    projects = db.query(Project).all()
    
    total_projects = len(projects)
    total_ministries = len(set(p.ministry for p in projects))
    
    original_cost = sum(p.originalCostCr for p in projects)
    revised_cost = sum(p.revisedCostCr for p in projects)
    expenditure = sum(p.expenditureCr for p in projects)
    
    mega_projects = sum(1 for p in projects if p.isMega)
    
    return DashboardSummaryResponse(
        totalProjects=total_projects,
        totalMinistries=total_ministries,
        originalCostCr=original_cost,
        revisedCostCr=revised_cost,
        costOverrunCr=revised_cost - original_cost,
        expenditureCr=expenditure,
        megaProjectsCount=mega_projects
    )
