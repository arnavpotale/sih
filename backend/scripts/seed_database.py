import json
import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.project import Project

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def seed_database():
    print("Loading detailed_projects.json...")
    file_path = os.path.join(os.path.dirname(__file__), "..", "detailed_projects.json")
    
    try:
        with open(file_path, "r") as f:
            projects_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return

    db: Session = SessionLocal()
    
    try:
        # Clear existing data for idempotency in Phase 1
        db.query(Project).delete()
        
        projects_to_insert = []
        for p in projects_data:
            project_db = Project(
                id=p.get("id"),
                name=p.get("name"),
                agency=p.get("agency"),
                ministry=p.get("ministry"),
                sector=p.get("sector"),
                hmlCategory=p.get("hmlCategory"),
                state=p.get("state"),
                approvalDate=p.get("approvalDate"),
                startDate=p.get("startDate"),
                originalTargetDoC=p.get("originalTargetDoC"),
                revisedDoC=p.get("revisedDoC"),
                originalCostCr=float(p.get("originalCostCr", 0) or 0),
                revisedCostCr=float(p.get("revisedCostCr", 0) or 0),
                expenditureCr=float(p.get("expenditureCr", 0) or 0),
                physicalProgress=float(p.get("physicalProgress", 0) or 0),
                financialProgress=float(p.get("financialProgress", 0) or 0),
                delayMonths=int(p.get("delayMonths", 0) or 0),
                riskScore=int(p.get("riskScore", 0) or 0),
                riskLevel=p.get("riskLevel"),
                isMega=bool(p.get("isMega", False)),
                cufAttributes=p.get("cufAttributes", {}),
                primaryDrivers=p.get("primaryDrivers", []),
                aiDiagnosis=p.get("aiDiagnosis"),
                aiPrescription=p.get("aiPrescription"),
            )
            projects_to_insert.append(project_db)
            
        db.bulk_save_objects(projects_to_insert)
        db.commit()
        print(f"Successfully seeded {len(projects_to_insert)} projects into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
