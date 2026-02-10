#!/usr/bin/env python3
"""
Debug script to see what dates are in the sheet
"""

import sys
from pathlib import Path

# Add src directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from google_sheets_handler import get_sheet_data_from_csv_export
from datetime import datetime

SPREADSHEET_ID = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"

print(f"Checking available dates in Google Sheet")
print("=" * 60)

rows = get_sheet_data_from_csv_export(SPREADSHEET_ID)

if rows:
    # Get unique dates
    dates = set()
    for row in rows:
        if 'Date' in row and row['Date'].strip():
            dates.add(row['Date'].strip())
    
    dates = sorted(list(dates))
    print(f"\nFound {len(dates)} unique dates in the sheet:")
    
    for i, date in enumerate(dates[-20:], 1):  # Show last 20
        print(f"  {date}")
    
    today = datetime.now().strftime("%m/%d/%Y")
    print(f"\nToday's date: {today}")
    
    if today in dates:
        print("✓ Today's date is in the sheet!")
    else:
        print("✗ Today's date is NOT in the sheet")
        print(f"\nMost recent date: {dates[-1] if dates else 'N/A'}")
        
        # Find the closest date
        from datetime import datetime as dt
        today_obj = dt.strptime(today, "%m/%d/%Y")
        closest_date = None
        closest_diff = float('inf')
        
        for date_str in dates:
            try:
                date_obj = dt.strptime(date_str, "%m/%d/%Y")
                diff = abs((date_obj - today_obj).days)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_date = date_str
            except:
                pass
        
        if closest_date:
            print(f"Closest date: {closest_date} ({closest_diff} days away)")

print("=" * 60)
