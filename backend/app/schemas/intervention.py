from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InterventionBase(BaseModel):
    project_id: str
    title: str
    description: str
    priority: str
    assigned_to: str
    due_date: str

class InterventionCreate(InterventionBase):
    pass

class InterventionUpdate(BaseModel):
    status: Optional[str] = None
    response_notes: Optional[str] = None
    updated_physical_progress: Optional[str] = None
    updated_financial_progress: Optional[str] = None
    current_blocker: Optional[str] = None
    expected_resolution_date: Optional[str] = None
    evidence_filename: Optional[str] = None

class InterventionOut(InterventionBase):
    id: int
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    verified_at: Optional[datetime] = None
    
    response_notes: Optional[str] = None
    updated_physical_progress: Optional[str] = None
    updated_financial_progress: Optional[str] = None
    current_blocker: Optional[str] = None
    expected_resolution_date: Optional[str] = None
    evidence_filename: Optional[str] = None

    class Config:
        from_attributes = True
