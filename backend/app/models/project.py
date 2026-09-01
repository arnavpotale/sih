from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    agency = Column(String)
    ministry = Column(String)
    sector = Column(String)
    hmlCategory = Column(String)
    state = Column(String)
    approvalDate = Column(String)
    startDate = Column(String)
    originalTargetDoC = Column(String)
    revisedDoC = Column(String)
    
    originalCostCr = Column(Float)
    revisedCostCr = Column(Float)
    expenditureCr = Column(Float)
    physicalProgress = Column(Float)
    financialProgress = Column(Float)
    
    delayMonths = Column(Integer)
    riskScore = Column(Integer)
    riskLevel = Column(String)
    isMega = Column(Boolean)
    
    cufAttributes = Column(JSON)
    primaryDrivers = Column(JSON)
    
    aiDiagnosis = Column(String)
    aiPrescription = Column(String)
