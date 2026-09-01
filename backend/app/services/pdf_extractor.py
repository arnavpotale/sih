import pdfplumber
import pandas as pd
from sqlalchemy.orm import Session
from app.models.project_snapshot import ProjectSnapshot
import re
import logging

logger = logging.getLogger(__name__)

def extract_project_snapshots_from_pdf(pdf_path: str, report_id: int, month: str, year: int, db: Session):
    """
    Extracts tabular data from MoSPI Flash Report PDF and inserts snapshots into DB.
    """
    snapshots_created = 0
    unique_projects = set()
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                        
                    # Basic heuristic: look for table with 'Cost' or 'Project' in header
                    header = [str(c).lower().strip() if c else "" for c in table[0]]
                    
                    # Convert to pandas for easier mapping
                    df = pd.DataFrame(table[1:], columns=header)
                    
                    # Fuzzy column mapping
                    code_col = next((c for c in header if 'code' in c), None)
                    name_col = next((c for c in header if 'name' in c or 'project' in c and c != code_col), None)
                    orig_cost_col = next((c for c in header if 'orig' in c and 'cost' in c), None)
                    rev_cost_col = next((c for c in header if 'revis' in c and 'cost' in c), None)
                    exp_col = next((c for c in header if 'expend' in c), None)
                    orig_date_col = next((c for c in header if 'orig' in c and ('date' in c or 'doc' in c)), None)
                    rev_date_col = next((c for c in header if 'revis' in c and ('date' in c or 'doc' in c)), None)
                    
                    if not code_col or not name_col:
                        continue # Not a project table
                        
                    for _, row in df.iterrows():
                        # The first column might contain: Name\n(Agency)\n(Project Code) ...
                        raw_name_col = str(row[name_col]) if pd.notnull(row[name_col]) else ""
                        lines = [line.strip() for line in raw_name_col.split('\n') if line.strip()]
                        
                        project_code = None
                        name = None
                        agency = None
                        
                        # Very simple heuristic for the 'All Ongoing Projects' table:
                        if len(lines) >= 3:
                            name = lines[0]
                            agency = lines[1].strip('()')
                            # Code is usually in the 3rd line like (705728)
                            code_match = re.search(r'\((\d+)\)', lines[2])
                            if code_match:
                                project_code = code_match.group(1)
                            else:
                                project_code = lines[2].strip('()')
                        
                        if not project_code or project_code == 'None' or project_code == "":
                            continue
                            
                        if project_code in unique_projects:
                            continue
                            
                        unique_projects.add(project_code)
                        
                        def parse_float_multiline(val, index):
                            try:
                                lines = [l.strip('() ') for l in str(val).split('\n') if l.strip()]
                                if len(lines) > index:
                                    # handle negative numbers or dashes
                                    v = lines[index].replace(',', '').strip()
                                    if v == '-' or not v: return None
                                    return float(v)
                                return None
                            except:
                                return None
                                
                        def parse_str_multiline(val, index):
                            try:
                                lines = [l.strip('() ') for l in str(val).split('\n') if l.strip()]
                                if len(lines) > index:
                                    v = lines[index].strip()
                                    if v == '-' or not v: return None
                                    return v
                                return None
                            except:
                                return None
                        
                        state_col = next((c for c in header if 'state' == c), None)
                        date_col = next((c for c in header if 'start date' in c or 'approval' in c), None)
                        phys_col = next((c for c in header if 'physical' in c), None)
                                
                        snapshot = ProjectSnapshot(
                            report_id=report_id,
                            project_code=project_code,
                            reporting_month=month,
                            reporting_year=year,
                            name=name,
                            agency=agency,
                            state=str(row[state_col]).replace('\n', ' ') if state_col and pd.notnull(row[state_col]) else None,
                            start_date=parse_str_multiline(row[date_col], 1) if date_col else parse_str_multiline(row[date_col], 0), # Usually (Start Date) is the second line
                            original_cost=parse_float_multiline(row[orig_cost_col], 0) if orig_cost_col else None,
                            revised_cost=parse_float_multiline(row[orig_cost_col], 1) if orig_cost_col else parse_float_multiline(row[orig_cost_col], 0), # Revised is usually second line
                            expenditure=parse_float_multiline(row[exp_col], 0) if exp_col else None,
                            original_end_date=parse_str_multiline(row[orig_date_col], 0) if orig_date_col else None,
                            revised_end_date=parse_str_multiline(row[orig_date_col], 1) if orig_date_col else parse_str_multiline(row[orig_date_col], 0),
                            physical_progress=parse_float_multiline(row[phys_col], 0) if phys_col else None
                        )
                        db.add(snapshot)
                        snapshots_created += 1
                        
        db.commit()
        return {"status": "success", "snapshots_extracted": snapshots_created, "unique_projects": len(unique_projects)}
    
    except Exception as e:
        logger.error(f"Failed to parse PDF {pdf_path}: {e}")
        db.rollback()
        raise e
