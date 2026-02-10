#!/usr/bin/env python3
"""
Flexible Google Sheets handler that can map custom column layouts
"""

import requests
from datetime import datetime
import csv
from io import StringIO

def get_sheet_data_custom_columns(spreadsheet_id, sheet_id=0, column_mapping=None):
    """
    Fetch data from Google Sheet with custom column mapping.
    
    Args:
        spreadsheet_id: The spreadsheet ID
        sheet_id: The sheet tab ID (default 0)
        column_mapping: Dict mapping logical names to actual column names
                       Example: {'name': 'Full Name', 'address': 'Address', ...}
    
    Returns:
        List of order dictionaries
    """
    
    # Default mapping (standard vertical format)
    if column_mapping is None:
        column_mapping = {
            'name': 'Full Name',
            'address': 'Address',
            'box_type': 'Type of Food',
            'rice_type': 'Type of Rice'
        }
    
    # Fetch CSV data
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
    
    try:
        print(f"Fetching Google Sheet data from: {csv_url}")
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(response.text))
        rows = list(csv_reader)
        
        print(f"Fetched {len(rows)} rows from Google Sheet")
        return rows, csv_reader.fieldnames
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Sheet: {e}")
        return [], []


def extract_orders_from_sheet(rows, sheet_columns, date_value, column_mapping=None):
    """
    Extract orders from sheet rows.
    
    Supports multiple formats:
    1. Vertical: One order per row
    2. Horizontal: Multiple orders in one row (Name1, Address1, etc.)
    
    Args:
        rows: List of row dictionaries from CSV
        sheet_columns: List of all column names
        date_value: The date to filter by (e.g., '2/9/2026')
        column_mapping: Dict of column name mappings
    
    Returns:
        List of order dictionaries
    """
    
    if column_mapping is None:
        column_mapping = {
            'name': 'Full Name',
            'address': 'Address',
            'box_type': 'Type of Food',
            'rice_type': 'Type of Rice'
        }
    
    orders = []
    
    # Find rows with matching date
    today_rows = [row for row in rows if row.get('Date', '').strip() == date_value]
    
    if not today_rows:
        print(f"No rows found for date: {date_value}")
        return orders
    
    print(f"Found {len(today_rows)} row(s) for date: {date_value}")
    print(f"Sheet has {len(sheet_columns)} columns total")
    
    for row_idx, row in enumerate(today_rows, 1):
        # Try Format 1: Standard vertical (one order per row)
        name_col = column_mapping.get('name', 'Full Name')
        addr_col = column_mapping.get('address', 'Address')
        box_col = column_mapping.get('box_type', 'Type of Food')
        rice_col = column_mapping.get('rice_type', 'Type of Rice')
        
        name = row.get(name_col, '').strip()
        if name:
            orders.append({
                'name': name,
                'address': row.get(addr_col, '').strip(),
                'box_type': row.get(box_col, '').strip(),
                'rice_type': row.get(rice_col, '').strip()
            })
            print(f"  Vertical Order {len(orders)}: {name}")
        
        # Try Format 2: Horizontal (multiple orders in one row)
        # Try different patterns
        patterns = [
            # Pattern: Name1, Address1, Box1, Rice1, Name2, Address2, Box2, Rice2, ...
            {1: ('Name{}', 'Address{}', 'Box{}', 'Rice{}')},
            # Pattern: Full Name1, Address1, Type of Food1, Type of Rice1, ...
            {1: ('Full Name{}', 'Address{}', 'Type of Food{}', 'Type of Rice{}')},
            # Pattern: FullName1, Address1, BoxType1, RiceType1, ...
            {1: ('FullName{}', 'Address{}', 'BoxType{}', 'RiceType{}')},
        ]
        
        # Try each pattern
        for pattern_dict in patterns:
            entry_num = 1
            max_entries = 10
            
            while entry_num <= max_entries:
                base_pattern = pattern_dict.get(1)  # Only one pattern key in our dict
                name_pattern, addr_pattern, box_pattern, rice_pattern = base_pattern
                
                name_col_h = name_pattern.format(entry_num)
                addr_col_h = addr_pattern.format(entry_num)
                box_col_h = box_pattern.format(entry_num)
                rice_col_h = rice_pattern.format(entry_num)
                
                # Check if columns exist
                if name_col_h in row:
                    h_name = row.get(name_col_h, '').strip()
                    if h_name:
                        orders.append({
                            'name': h_name,
                            'address': row.get(addr_col_h, '').strip(),
                            'box_type': row.get(box_col_h, '').strip(),
                            'rice_type': row.get(rice_col_h, '').strip()
                        })
                        print(f"  Horizontal Order {len(orders)}: {h_name} (entry {entry_num})")
                        entry_num += 1
                    else:
                        break
                else:
                    break
    
    return orders


# Test usage
if __name__ == "__main__":
    spreadsheet_id = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"
    
    # Default mapping for standard sheet
    column_mapping = {
        'name': 'Full Name',
        'address': 'Address',
        'box_type': 'Type of Food',
        'rice_type': 'Type of Rice'
    }
    
    rows, columns = get_sheet_data_custom_columns(spreadsheet_id, column_mapping=column_mapping)
    
    # Get today's date
    today = datetime.now()
    today_date = f"{today.month}/{today.day}/{today.year}"
    
    print(f"\nLooking for date: {today_date}")
    print(f"Available columns: {columns}\n")
    
    orders = extract_orders_from_sheet(rows, columns, today_date, column_mapping)
    
    print(f"\n✓ Extracted {len(orders)} total orders")
    for i, order in enumerate(orders, 1):
        print(f"\nOrder {i}:")
        for key, value in order.items():
            print(f"  {key}: {value}")
