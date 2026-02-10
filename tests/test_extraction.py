#!/usr/bin/env python3
"""
Test script to verify the row-based extraction logic
"""

import re

def test_extraction_logic():
    """Test the new row-based extraction with sample OCR output"""
    
    # Sample OCR output that previously would have caused misalignment
    sample_ocr_output = """
    ORDER NO: 001
    Name: John Smith
    2900 Plano Pkwy 9876543210 John Smith
    2 Comfort Box
    Pulav Rice
    
    ORDER NO: 002
    Name: Jane Doe
    3400 W Plano Pkwy 5551234567 Jane Doe
    3 Comfort Box
    White Rice
    
    ORDER NO: 003
    Name: Bob Johnson
    2900 Plano Pkwy 5559876543 Bob Johnson
    1 Comfort Box
    Pulav Rice
    """
    
    # Patterns
    phone_pattern = re.compile(r'\b\d{10}\b')
    address_pattern = re.compile(r'(2900 Plano Pkwy|3400 W Plano Pkwy)')
    box_pattern = re.compile(r'(\d+)\s*(Comfort Box|Kabuli Chana Box|Moong Dal Box|Rajma Box)')
    rice_pattern = re.compile(r'(Pulav Rice|White Rice)')
    
    lines = [line.strip() for line in sample_ocr_output.split('\n') if line.strip()]
    
    print(f"Processing {len(lines)} lines:")
    for i, line in enumerate(lines):
        print(f"  {i:2d}: {line}")
    print()
    
    data_rows = []
    current_row = {
        'name': '',
        'address': '',
        'box_type': '',
        'rice_type': ''
    }
    
    for line in lines:
        # Skip header and junk
        if any(skip in line for skip in ['OAN', 'RWDN', 'ORDER NO', 'DELIVERY', 'PHONE', 'Name:']):
            continue
        
        # Check if line contains address (potential start of new row)
        address_match = address_pattern.search(line)
        if address_match:
            # Save previous row if it has data
            if current_row['name'] or current_row['address']:
                data_rows.append(current_row.copy())
                print(f"✓ Completed row: {current_row}")
            
            # Start new row
            current_row = {
                'name': '',
                'address': address_match.group(1),
                'box_type': '',
                'rice_type': ''
            }
            
            # Extract name and phone from this line
            line_remainder = line.replace(address_match.group(1), '').strip()
            
            # Remove special characters
            for char in ['=v', '=', '~', '»', '|', '¥']:
                line_remainder = line_remainder.replace(char, '')
            line_remainder = line_remainder.strip()
            
            # Extract phone number
            phone_match = phone_pattern.search(line_remainder)
            if phone_match:
                phone = phone_match.group()
                line_remainder = line_remainder.replace(phone, '').strip()
            
            # What's left should be the name
            if line_remainder:
                current_row['name'] = line_remainder
            
            print(f"→ Found address line: name='{current_row['name']}', addr='{current_row['address']}'")
            continue
        
        # Check if it's a box type
        box_match = box_pattern.search(line)
        if box_match:
            quantity = box_match.group(1)
            box_name = box_match.group(2)
            current_row['box_type'] = f"{quantity} {box_name}"
            print(f"→ Found box type: {current_row['box_type']}")
            continue
        
        # Check if it's rice type
        rice_match = rice_pattern.search(line)
        if rice_match:
            current_row['rice_type'] = rice_match.group(1)
            print(f"→ Found rice type: {current_row['rice_type']}")
            continue
    
    # Save the last row if it has data
    if current_row['name'] or current_row['address']:
        data_rows.append(current_row.copy())
        print(f"✓ Final row: {current_row}")
    
    print(f"\n{'='*60}")
    print(f"EXTRACTED {len(data_rows)} ROWS:")
    print(f"{'='*60}")
    for i, row in enumerate(data_rows, 1):
        print(f"\nRow {i}:")
        print(f"  Name:     {row['name']}")
        print(f"  Address:  {row['address']}")
        print(f"  Box Type: {row['box_type']}")
        print(f"  Rice:     {row['rice_type']}")
    
    # Verify correctness
    assert len(data_rows) == 3, f"Expected 3 rows, got {len(data_rows)}"
    assert data_rows[0]['name'] == 'John Smith', f"Row 0 name mismatch: {data_rows[0]['name']}"
    assert data_rows[0]['address'] == '2900 Plano Pkwy', f"Row 0 address mismatch"
    assert data_rows[0]['box_type'] == '2 Comfort Box', f"Row 0 box_type mismatch"
    assert data_rows[0]['rice_type'] == 'Pulav Rice', f"Row 0 rice_type mismatch"
    
    assert data_rows[1]['name'] == 'Jane Doe', f"Row 1 name mismatch"
    assert data_rows[1]['address'] == '3400 W Plano Pkwy', f"Row 1 address mismatch"
    assert data_rows[1]['box_type'] == '3 Comfort Box', f"Row 1 box_type mismatch"
    assert data_rows[1]['rice_type'] == 'White Rice', f"Row 1 rice_type mismatch"
    
    assert data_rows[2]['name'] == 'Bob Johnson', f"Row 2 name mismatch"
    
    print(f"\n{'='*60}")
    print("✓ ALL TESTS PASSED!")
    print(f"{'='*60}")

if __name__ == "__main__":
    test_extraction_logic()
