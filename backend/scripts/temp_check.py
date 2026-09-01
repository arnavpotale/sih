import sys
import os
sys.path.append(os.path.abspath('backend'))
from app.db.database import SessionLocal
from app.models.project_snapshot import ProjectSnapshot
from app.models.report import Report
from collections import defaultdict
import pandas as pd

db = SessionLocal()

months = ['April', 'May', 'June', 'July']
snapshots_per_month = {}
projects_per_month = {}

for m in months:
    snaps = db.query(ProjectSnapshot).filter_by(reporting_month=m).all()
    snapshots_per_month[m] = len(snaps)
    projects_per_month[m] = set([s.project_code for s in snaps])
    print(f"{m}:")
    print(f"snapshot count: {snapshots_per_month[m]}")
    print(f"unique projects: {len(projects_per_month[m])}")
    print()

all_project_codes = set()
for s in projects_per_month.values():
    all_project_codes.update(s)

counts = defaultdict(int)
for code in all_project_codes:
    appearances = sum(1 for m in months if code in projects_per_month[m])
    counts[appearances] += 1

print(f"projects appearing in 2+ reports: {counts[2] + counts[3] + counts[4]}")
print(f"projects appearing in 3+ reports: {counts[3] + counts[4]}")
print(f"projects appearing in all 4 reports: {counts[4]}")
print()

print(f"April -> May overlap: {len(projects_per_month['April'].intersection(projects_per_month['May']))}")
print(f"May -> June overlap: {len(projects_per_month['May'].intersection(projects_per_month['June']))}")
print(f"June -> July overlap: {len(projects_per_month['June'].intersection(projects_per_month['July']))}")

four_month_intersection = projects_per_month['April'].intersection(projects_per_month['May']).intersection(projects_per_month['June']).intersection(projects_per_month['July'])
print(f"April ∩ May ∩ June ∩ July: {len(four_month_intersection)}")
print()

print("Project Identity Check:")
for code in ['705728', '705237', '705429', '705941', '705391']:
    print(f"Project: {code}")
    for m in months:
        snap = db.query(ProjectSnapshot).filter_by(project_code=code, reporting_month=m).first()
        if snap:
            print(f"  {m}: code={snap.project_code}, name={snap.name[:20] if snap.name else None}, orig_cost={snap.original_cost}, rev_cost={snap.revised_cost}, exp={snap.expenditure}, phys={snap.physical_progress}, orig_doc={snap.original_end_date}, rev_doc={snap.revised_end_date}")
        else:
            print(f"  {m}: Not found")
    print()
