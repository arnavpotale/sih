import sys
import os
import pdfplumber

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

pdf_path = '../FlashReport_April2026.pdf'
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text and '705728' in text:
            print(f"Page {i+1} has 705728:")
            print(text)
            tables = page.extract_tables()
            print("Tables found:", len(tables))
            for t in tables:
                print(t[0])
