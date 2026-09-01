from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base

class ProjectSnapshot(Base):
    __tablename__ = "project_snapshots"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('reports.id'))
    project_code = Column(String, index=True)
    reporting_month = Column(String)
    reporting_year = Column(Integer)
    
    # Project Snapshot fields
    name = Column(String)
    sector = Column(String)
    ministry = Column(String)
    agency = Column(String)
    state = Column(String)
    
    start_date = Column(String, nullable=True)
    original_cost = Column(Float, nullable=True)
    revised_cost = Column(Float, nullable=True)
    expenditure = Column(Float, nullable=True)
    
    original_end_date = Column(String, nullable=True)
    revised_end_date = Column(String, nullable=True)
    
    physical_progress = Column(Float, nullable=True)
    financial_progress = Column(Float, nullable=True)
    
    status = Column(String, nullable=True)
