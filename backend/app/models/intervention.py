from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.db.database import Base

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    priority = Column(String)
    status = Column(String, default="OPEN") # OPEN, IN_PROGRESS, AWAITING_VERIFICATION, RESOLVED, CLOSED
    assigned_to = Column(String)
    created_by = Column(String)
    
    due_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    
    # Project Manager Response Fields
    response_notes = Column(Text, nullable=True)
    updated_physical_progress = Column(String, nullable=True)
    updated_financial_progress = Column(String, nullable=True)
    current_blocker = Column(String, nullable=True)
    expected_resolution_date = Column(String, nullable=True)
    evidence_filename = Column(String, nullable=True)
