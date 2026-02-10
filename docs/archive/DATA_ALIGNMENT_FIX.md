# Data Alignment Fix - Technical Summary

## Problem Identified

The previous extraction logic had a **critical flaw in data alignment**:

### Old Approach (Broken)
```python
# Collected each field type independently
names = [extract all names]
addresses = [extract all addresses]
box_types = [extract all box types]
rice_types = [extract all rice types]

# Then zipped by index (WRONG!)
for i in range(len(names)):
    row = {
        'name': names[i],
        'address': addresses[i],
        'box_type': box_types[i],
        'rice_type': rice_types[i]
    }
```

**Why this fails:**
- OCR sometimes extracts fields in different quantities or orders
- If OCR finds 10 names but 9 addresses, the final rows are misaligned
- Fields get paired with wrong rows: Row 1 might get Name1 with Address2 and BoxType3

### Example of Misalignment
If OCR output was processed as:
- Names: [John, Jane, Bob]
- Addresses: [2900 Plano, 3400 W Plano, 2900 Plano]
- Boxes: [2 Comfort Box, 3 Comfort Box, 1 Comfort Box]
- Rice: [Pulav Rice, White Rice, Pulav Rice]

The OLD code would still produce correct results IF counts matched, but:
- If counts didn't match, padding with empty strings created garbage rows
- If OCR detected things in different order, misalignment was unavoidable

## Solution Implemented

### New Approach (Fixed)
```python
# Process data row-by-row as it appears in the image
data_rows = []
current_row = {'name': '', 'address': '', 'box_type': '', 'rice_type': ''}

for line in lines:
    if address_pattern.matches(line):
        # ADDRESS FOUND = START OF NEW ROW
        # Save previous row
        if current_row['name'] or current_row['address']:
            data_rows.append(current_row.copy())
        
        # Start fresh row with this address
        current_row = extract_address_and_name(line)
    
    elif box_pattern.matches(line):
        # Add to current row
        current_row['box_type'] = extract_box_type(line)
    
    elif rice_pattern.matches(line):
        # Add to current row
        current_row['rice_type'] = extract_rice_type(line)
```

**Why this works:**
- Uses **address line as row delimiter** - each address marks the start of a new order
- Groups all fields for one order together
- Handles missing or reordered fields gracefully
- Rows stay grouped by their address anchor

## Key Improvements

1. **Address as Row Anchor**: Address line is the definitive start of each row
2. **Sequential Processing**: Fields are added to the current row as encountered
3. **Automatic Row Completion**: When a new address is found, the previous row is saved
4. **Better Error Handling**: Empty fields are preserved in context, not misaligned

## Testing

Created `test_extraction.py` to verify the logic with sample data:
- ✓ Correctly extracts 3 rows with all fields properly aligned
- ✓ Handles multiple address formats (2900 vs 3400 W Plano Pkwy)
- ✓ Correctly pairs names with addresses on same line
- ✓ Extracts box quantities and types correctly
- ✓ Distinguishes between rice types (Pulav vs White)

## Files Modified

- `update_template.py` - Replaced `extract_table_data_from_image()` function with row-based logic
- Added comprehensive debug output showing row processing

## Result

The PDF output should now have:
- ✓ Names correctly paired with their addresses
- ✓ Box types matched with correct orders
- ✓ Rice types aligned with proper rows
- ✓ No duplicate or misaligned data
