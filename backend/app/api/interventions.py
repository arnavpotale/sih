from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.intervention import Intervention
from app.schemas.intervention import InterventionCreate, InterventionUpdate, InterventionOut
from datetime import datetime

router = APIRouter(
    prefix="/api/interventions",
    tags=["interventions"]
)

@router.get("/", response_model=List[InterventionOut])
def get_interventions(db: Session = Depends(get_db)):
    return db.query(Intervention).order_by(Intervention.created_at.desc()).all()

@router.get("/project/{project_id}", response_model=List[InterventionOut])
def get_project_interventions(project_id: str, db: Session = Depends(get_db)):
    return db.query(Intervention).filter(Intervention.project_id == project_id).order_by(Intervention.created_at.desc()).all()

@router.get("/{id}", response_model=InterventionOut)
def get_intervention(id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Intervention).filter(Intervention.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Intervention not found")
    return db_obj

@router.post("/", response_model=InterventionOut)
def create_intervention(intervention: InterventionCreate, db: Session = Depends(get_db)):
    db_obj = Intervention(**intervention.dict(), created_by="IPMD Official")
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.patch("/{id}", response_model=InterventionOut)
def update_intervention(id: int, update_data: InterventionUpdate, db: Session = Depends(get_db)):
    db_obj = db.query(Intervention).filter(Intervention.id == id).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Intervention not found")
    
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_obj, key, value)
        
    if update_dict.get("status") == "CLOSED":
        db_obj.verified_at = datetime.utcnow()
        
    db.commit()
    db.refresh(db_obj)
    return db_obj
