from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ProjectBase(BaseModel):
    name: str
    agency: str
    ministry: str
    sector: str
    hmlCategory: str
    state: str
    approvalDate: str
    startDate: str
    originalTargetDoC: str
    revisedDoC: str
    
    originalCostCr: float
    revisedCostCr: float
    expenditureCr: float
    physicalProgress: float
    financialProgress: float
    
    delayMonths: int
    riskScore: int
    riskLevel: str
    isMega: bool
    
    cufAttributes: Optional[Dict[str, Any]] = None
    primaryDrivers: Optional[List[str]] = None
    
    aiDiagnosis: Optional[str] = None
    aiPrescription: Optional[str] = None

class ProjectCreate(ProjectBase):
    id: str

class ProjectResponse(ProjectBase):
    id: str

    class Config:
        from_attributes = True

class DashboardSummaryResponse(BaseModel):
    totalProjects: int
    totalMinistries: int
    originalCostCr: float
    revisedCostCr: float
    costOverrunCr: float
    expenditureCr: float
    megaProjectsCount: int
