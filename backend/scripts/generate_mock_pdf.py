from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def generate_mock_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    data = [
        ["Project Code", "Project Name", "Sector", "Original Cost", "Revised Cost", "Expenditure", "Original DoC", "Revised DoC"],
        ["PRJ-001", "Mumbai Metro Line 3", "Urban Transport", "23136", "37275", "25000", "2021-12", "2024-12"],
        ["PRJ-002", "NH-44 Expansion", "Roads", "4500", "4800", "3000", "2023-06", "2024-06"],
        ["PRJ-003", "Kudankulam Unit 3&4", "Atomic Energy", "39849", "39849", "20000", "2023-03", "2025-03"],
        ["PRJ-004", "Navi Mumbai Airport", "Civil Aviation", "16700", "19600", "8000", "2024-12", "2025-12"],
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)

if __name__ == "__main__":
    generate_mock_pdf("mock_report_july2026.pdf")
    print("Mock PDF generated.")
