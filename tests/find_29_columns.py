#!/usr/bin/env python3
"""
Advanced diagnostic to check all sheet tabs and find the 29-column data
"""

import requests
from csv import DictReader
from io import StringIO
from datetime import datetime

SPREADSHEET_ID = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"

print("Searching for 29-column data structure...")
print("=" * 80)

# Try different sheet IDs (gid parameter)
# Common sheets: 0 (first), 1 (second), etc.

for sheet_id in range(0, 5):
    print(f"\n\nChecking Sheet ID: {sheet_id}")
    print("-" * 80)
    
    csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={sheet_id}"
    
    try:
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        
        csv_reader = DictReader(StringIO(response.text))
        rows = list(csv_reader)
        
        if not rows:
            print(f"Sheet {sheet_id}: No data or empty sheet")
            continue
        
        print(f"Sheet {sheet_id}: Found {len(rows)} rows")
        
        # Check first row
        first_row = rows[0]
        num_cols = len([k for k in first_row.keys() if k.strip()])
        print(f"  Columns: {num_cols}")
        
        if num_cols > 10:
            print(f"  ✓ This sheet has {num_cols} columns (more than typical!)")
            print(f"  Column names: {list(first_row.keys())}")
        
        # Find today's data
        today = datetime.now()
        today_formats = [
            today.strftime("%m/%d/%Y"),
            f"{today.month}/{today.day}/{today.year}"
        ]
        
        today_rows = [row for row in rows if 'Date' in row and row['Date'].strip() in today_formats]
        
        if today_rows:
            print(f"  ✓ Found {len(today_rows)} row(s) for today")
            for i, row in enumerate(today_rows):
                non_empty = {k: v for k, v in row.items() if v.strip()}
                print(f"    Row {i+1}: {len(non_empty)} non-empty columns")
                print(f"    Columns: {list(non_empty.keys())}")
        
    except Exception as e:
        print(f"Sheet {sheet_id}: Error - {e}")

print("\n" + "=" * 80)
print("\nIf you found a sheet with 29+ columns, please let me know the gid number!")
