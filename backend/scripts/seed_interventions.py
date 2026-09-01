import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, Base, SessionLocal
from app.models.intervention import Intervention
from datetime import datetime, timedelta

def seed():
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(Intervention).count() > 0:
            print("Interventions already seeded.")
            return

        interventions = [
            Intervention(
                project_id="705728", # Mumbai-Ahmedabad High Speed Rail
                title="Review Undersea Tunneling Clearances",
                description="Investigate the delay in obtaining final environmental clearances for the BKC undersea section. Coordinate with State machinery.",
                priority="CRITICAL",
                status="OPEN",
                assigned_to="Project Manager",
                created_by="IPMD Official",
                due_date=(datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
            ),
            Intervention(
                project_id="101683", # Polavaram
                title="R&R Package Escalation Strategy",
                description="The R&R cost has heavily deviated from original estimates. Provide a revised breakdown and submit evidence of state government land handover.",
                priority="HIGH",
                status="IN_PROGRESS",
                assigned_to="Project Manager",
                created_by="IPMD Official",
                due_date=(datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d"),
                response_notes="Met with the State Revenue Department. 85% of affected families have received compensation. Final tranche awaiting finance ministry approval.",
                updated_physical_progress="38.5",
                updated_financial_progress="65.2",
                current_blocker="Finance Ministry Tranche Approval",
                expected_resolution_date=(datetime.utcnow() + timedelta(days=21)).strftime("%Y-%m-%d"),
                evidence_filename="Polavaram_RR_Status_Report.pdf"
            ),
            Intervention(
                project_id="125501", # Subansiri
                title="Geological Surprise Assessment",
                description="Landslides have caused repeated stoppage. Submit the revised geological stabilization plan.",
                priority="MEDIUM",
                status="AWAITING_VERIFICATION",
                assigned_to="Project Manager",
                created_by="IPMD Official",
                due_date=(datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d"),
                response_notes="Stabilization works completed on the right bank. Slope monitoring sensors installed. The work has resumed.",
                updated_physical_progress="84.0",
                updated_financial_progress="92.0",
                current_blocker="None",
                expected_resolution_date=(datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d"),
                evidence_filename="Slope_Stabilization_Certificate.pdf"
            )
        ]
        
        for inv in interventions:
            db.add(inv)
            
        db.commit()
        print("Successfully seeded 3 demo interventions.")
    
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
