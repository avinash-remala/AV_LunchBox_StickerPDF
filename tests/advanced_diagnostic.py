#!/usr/bin/env python3
"""
Advanced diagnostic to show ALL columns in the Google Sheet
"""

import requests
import csv
from io import StringIO
from datetime import datetime

SPREADSHEET_ID = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"

print("Advanced Google Sheets Diagnostic")
print("=" * 80)

# Fetch the raw CSV
csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=0"

try:
    response = requests.get(csv_url, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Error fetching sheet: {e}")
    exit(1)

# Parse CSV
csv_reader = csv.DictReader(StringIO(response.text))
rows = list(csv_reader)

print(f"\nTotal rows in sheet: {len(rows)}")

# Find today's rows
today = datetime.now()
today_formats = [today.strftime("%m/%d/%Y"), f"{today.month}/{today.day}/{today.year}"]

today_rows = [row for row in rows if 'Date' in row and row['Date'].strip() in today_formats]

print(f"Rows for today: {len(today_rows)}")
print(f"\nToday's date formats: {today_formats}")

if today_rows:
    print(f"\n{'=' * 80}")
    print("TODAY'S ROWS DETAILED VIEW")
    print(f"{'=' * 80}")
    
    for row_num, row in enumerate(today_rows, 1):
        print(f"\n📍 Row #{row_num} for today:")
        print(f"{'-' * 80}")
        
        # Get all columns
        all_cols = list(row.keys())
        print(f"Total columns in this row: {len(all_cols)}\n")
        
        # Display each column
        for i, col in enumerate(all_cols, 1):
            value = row[col].strip() if row[col] else ""
            
            # Truncate long values
            if len(value) > 50:
                display_val = value[:47] + "..."
            else:
                display_val = value
            
            # Highlight non-empty columns
            status = "✓" if value else "  "
            print(f"{status} [{i:2d}] {col:30s} = {display_val}")
        
        print(f"\n{'-' * 80}")
        print("NON-EMPTY COLUMNS ONLY:")
        print(f"{'-' * 80}")
        
        non_empty = {k: v for k, v in row.items() if v.strip()}
        for i, (col, val) in enumerate(non_empty.items(), 1):
            print(f"{i}. {col:30s} = {val}")

print(f"\n{'=' * 80}")
print("EXPECTED COLUMN PATTERNS FOR HORIZONTAL FORMAT:")
print(f"{'=' * 80}")
print("""
If you have 29 columns with horizontal layout, it might be:

Pattern A (7 orders × 4 columns each = 28 columns + Date):
  Name1, Address1, Box1, Rice1, Name2, Address2, Box2, Rice2, ...

Pattern B (Different naming):
  Full Name, Address, Type of Food, Type of Rice (repeated)

Please describe your Google Sheet layout:
- How many orders are in today's row?
- What are the column names?
- Share a screenshot or describe the structure
""")

print("=" * 80)
