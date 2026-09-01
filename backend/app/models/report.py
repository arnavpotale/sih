from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_type = Column(String, default="MoSPI Flash Report")
    reporting_month = Column(String)  # e.g., "April", "May"
    reporting_year = Column(Integer)  # e.g., 2026
    file_name = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    processing_status = Column(String, default="PENDING")  # PENDING, COMPLETED, FAILED
    error_message = Column(String, nullable=True)
