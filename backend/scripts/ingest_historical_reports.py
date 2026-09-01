import os
import sys
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

# Set up paths and database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.database import Base, engine, SessionLocal
from app.models.report import Report
from app.models.project_snapshot import ProjectSnapshot
from app.services.pdf_extractor import extract_project_snapshots_from_pdf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PDF_FILES = [
    'FlashReport_April2026.pdf',
    'FlashReport_May2026.pdf',
    'FlashReport_June_2026 (1).pdf',
    'FlashReport_July_2026 (1).pdf'
]

def parse_month_year(filename):
    if 'April' in filename: return 'April', 2026
    if 'May' in filename: return 'May', 2026
    if 'June' in filename: return 'June', 2026
    if 'July' in filename: return 'July', 2026
    return None, None

def ingest_reports():
    # Make sure DB schema is up to date
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        for pdf_file in PDF_FILES:
            pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', pdf_file))
            if not os.path.exists(pdf_path):
                logger.error(f"File not found: {pdf_path}")
                continue
                
            month, year = parse_month_year(pdf_file)
            if not month:
                logger.error(f"Could not parse month/year from {pdf_file}")
                continue
                
            # Check if report already exists
            existing_report = db.query(Report).filter_by(file_name=pdf_file).first()
            if existing_report and existing_report.processing_status == 'COMPLETED':
                logger.info(f"Report {pdf_file} already ingested. Skipping.")
                continue
                
            logger.info(f"Ingesting {pdf_file} for {month} {year}...")
            
            if not existing_report:
                report = Report(
                    report_type="MoSPI Flash Report",
                    reporting_month=month,
                    reporting_year=year,
                    file_name=pdf_file,
                    processing_status="PENDING"
                )
                db.add(report)
                db.commit()
                db.refresh(report)
            else:
                report = existing_report
                
            try:
                # Remove existing snapshots if any
                db.query(ProjectSnapshot).filter_by(report_id=report.id).delete()
                
                result = extract_project_snapshots_from_pdf(pdf_path, report.id, month, year, db)
                
                report.processing_status = "COMPLETED"
                db.commit()
                logger.info(f"Success for {pdf_file}: {result}")
            except Exception as e:
                report.processing_status = "FAILED"
                report.error_message = str(e)
                db.commit()
                logger.error(f"Failed to extract from {pdf_file}: {e}")
                
    finally:
        db.close()

if __name__ == "__main__":
    ingest_reports()
