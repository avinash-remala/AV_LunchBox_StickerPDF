#!/usr/bin/env python3
"""
Read data from Google Sheets without authentication (public sheets).
Uses the public CSV export URL to fetch data.
"""

import requests
from datetime import datetime
import csv
from io import StringIO

def get_sheet_data_from_csv_export(spreadsheet_id, sheet_id=0):
    """
    Fetch data from a public Google Sheet using CSV export.
    
    Args:
        spreadsheet_id: The spreadsheet ID from the URL
        sheet_id: The gid parameter (sheet tab ID), default is 0 (first sheet)
    
    Returns:
        List of dictionaries with row data
    """
    # Construct the CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
    
    try:
        print(f"Fetching Google Sheet data from: {csv_url}")
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(response.text))
        rows = list(csv_reader)
        
        print(f"Fetched {len(rows)} rows from Google Sheet")
        return rows
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Sheet: {e}")
        return []


def find_today_row(rows, date_column='Date'):
    """
    Find the row that matches today's date.
    
    Args:
        rows: List of dictionaries from the sheet
        date_column: The column name containing dates (default 'Date')
    
    Returns:
        Dictionary of the matching row, or None
    """
    from datetime import datetime as dt
    today = datetime.now()
    
    # Try both formats: with and without leading zero
    today_formats = [
        today.strftime("%m/%d/%Y"),  # 02/09/2026
        today.strftime("%-m/%-d/%Y") if hasattr(today, 'strftime') else f"{today.month}/{today.day}/{today.year}"  # 2/9/2026
    ]
    
    for row in rows:
        if date_column in row and row[date_column].strip() in today_formats:
            print(f"Found today's row: {row}")
            return row
    
    print(f"No row found for today's date: {today_formats}")
    return None


def extract_data_from_row(row, name_col='Name', address_col='Address', 
                          box_type_col='Box Type', rice_type_col='Rice Type'):
    """
    Extract order data from a single Google Sheet row.
    
    Args:
        row: Dictionary from CSV (single row)
        name_col: Column name for customer name
        address_col: Column name for address
        box_type_col: Column name for box type
        rice_type_col: Column name for rice type
    
    Returns:
        List of order dictionaries, one per column set
    """
    orders = []
    
    # If the row contains single entries in each column
    if all(col in row for col in [name_col, address_col, box_type_col, rice_type_col]):
        order = {
            'name': row.get(name_col, '').strip(),
            'address': row.get(address_col, '').strip(),
            'box_type': row.get(box_type_col, '').strip(),
            'rice_type': row.get(rice_type_col, '').strip()
        }
        if order['name']:  # Only add if name exists
            orders.append(order)
    
    return orders


def get_todays_lunch_orders(spreadsheet_id, sheet_id=0):
    """
    Get all lunch orders for today from Google Sheet.
    
    Handles merged date cells where:
    - First row has the date (e.g., "2/9/2026")
    - Subsequent rows have empty date cell (because date is merged)
    - All rows belong to the same date
    
    Args:
        spreadsheet_id: The spreadsheet ID from the URL
        sheet_id: The sheet tab ID (default 0 for first sheet)
    
    Returns:
        List of order dictionaries for today
    """
    from datetime import datetime as dt
    
    # Fetch all data
    rows = get_sheet_data_from_csv_export(spreadsheet_id, sheet_id)
    
    if not rows:
        print("No data fetched from Google Sheet")
        return []
    
    # Print column names for debugging
    if rows:
        all_cols = list(rows[0].keys())
        print(f"Available columns: {all_cols}")
        print(f"Total columns: {len(all_cols)}")
    
    # Find ALL rows for today
    today = dt.now()
    
    # Try both formats: with and without leading zero
    today_formats = [
        today.strftime("%m/%d/%Y"),  # 02/09/2026
        today.strftime("%-m/%-d/%Y") if hasattr(today, 'strftime') else f"{today.month}/{today.day}/{today.year}"  # 2/9/2026
    ]
    
    # Find rows with today's date OR empty date (for merged cells)
    today_rows = []
    found_today = False
    
    for idx, row in enumerate(rows):
        date_val = row.get('Date', '').strip()
        
        # Check if this row has today's date
        if date_val in today_formats:
            today_rows.append(row)
            found_today = True
        # If we found today, continue adding rows with empty dates (merged cells)
        elif found_today and date_val == '':
            today_rows.append(row)
        # If we found today and now we see a different date, stop
        elif found_today and date_val != '':
            break
    
    if not today_rows:
        print(f"No rows found for today's date: {today_formats}")
        return []
    
    print(f"Found {len(today_rows)} row(s) for today (including merged date cells)")
    
    # Extract data from all today's rows
    orders = []
    
    for row_idx, row in enumerate(today_rows, 1):
        # Extract from standard columns
        # Columns: Full Name, Address, Type of Food, Type of Rice
        name = row.get('Full Name', '').strip()
        address = row.get('Address', '').strip()
        box_type = row.get('Type of Food', '').strip()
        rice_type = row.get('Type of Rice', '').strip()
        
        if name:
            orders.append({
                'name': name,
                'address': address,
                'box_type': box_type,
                'rice_type': rice_type
            })
            print(f"  Order {len(orders)}: {name} - {box_type} - {rice_type}")
    
    print(f"Extracted {len(orders)} total orders from today's data")
    return orders


# Test function to help debug
if __name__ == "__main__":
    # Replace with your actual spreadsheet ID
    SPREADSHEET_ID = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"
    
    print("Testing Google Sheets integration...\n")
    orders = get_todays_lunch_orders(SPREADSHEET_ID)
    
    if orders:
        print(f"\nFound {len(orders)} orders for today:")
        for i, order in enumerate(orders, 1):
            print(f"  {i}. {order}")
    else:
        print("No orders found for today")
