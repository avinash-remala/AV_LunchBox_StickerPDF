#!/usr/bin/env python3
"""
Diagnostic script to see the exact structure of today's row in Google Sheet
"""

from google_sheets_handler import get_sheet_data_from_csv_export
from datetime import datetime

SPREADSHEET_ID = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"

print("Analyzing today's row structure...")
print("=" * 80)

rows = get_sheet_data_from_csv_export(SPREADSHEET_ID)

if rows:
    today = datetime.now()
    today_formats = [
        today.strftime("%m/%d/%Y"),
        today.strftime("%-m/%-d/%Y") if hasattr(today, 'strftime') else f"{today.month}/{today.day}/{today.year}"
    ]
    
    today_rows = [row for row in rows if 'Date' in row and row['Date'].strip() in today_formats]
    
    if today_rows:
        print(f"\nFound {len(today_rows)} row(s) for today")
        
        for row_idx, row in enumerate(today_rows):
            print(f"\n{'='*80}")
            print(f"Row {row_idx + 1}:")
            print(f"{'='*80}")
            
            # Get all columns
            all_cols = list(row.keys())
            print(f"\nTotal columns: {len(all_cols)}")
            print(f"\nAll columns:")
            for i, col in enumerate(all_cols, 1):
                value = row[col].strip() if row[col] else "(empty)"
                print(f"  {i:2d}. {col:30s} = {value}")
            
            print(f"\n\nData analysis:")
            print(f"Non-empty columns:")
            non_empty = [(col, row[col]) for col in all_cols if row[col] and row[col].strip()]
            for col, val in non_empty:
                print(f"  {col:30s} = {val.strip()}")
    else:
        print(f"No rows found for today's date: {today_formats}")

print("\n" + "=" * 80)
