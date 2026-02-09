# Data Alignment Fix - User Guide

## What Was Fixed

Your PDF was showing **misaligned data** because the extraction logic was collecting each field type (names, addresses, box types, rice types) independently and then combining them by index. If OCR extracted fields in different quantities or orders, the final data would be scrambled.

### Example of the Problem
```
Before Fix (WRONG):
Row 1: Name1, Address2, BoxType1, Rice3  ← Names, addresses, boxes, and rice don't match!
Row 2: Name2, Address3, BoxType2, Rice1
Row 3: Name3, Address1, BoxType3, Rice2

After Fix (CORRECT):
Row 1: Name1, Address1, BoxType1, Rice1  ← All fields from the same order
Row 2: Name2, Address2, BoxType2, Rice2
Row 3: Name3, Address3, BoxType3, Rice3
```

## How It's Fixed

The script now processes data **row-by-row** instead of field-by-field:

1. **Address line is the row anchor** - Each address marks the start of a new order
2. **Fields are grouped together** - Name, box type, and rice type are collected as a unit
3. **Automatic row completion** - When a new address is encountered, the previous row is saved
4. **Proper field pairing** - All fields stay with their correct order

## Using the Updated Script

The usage remains the same:

```bash
# GUI Mode (Recommended)
python3 update_template_gui.py

# Command Line Mode
python3 update_template.py <image.png> <template.docx> <output.pdf>
```

### Example
```bash
python3 update_template.py order_image.png Templates/AR_Template.docx output.pdf
```

## What to Expect

When you run the script now with your image, you'll see:

```
OCR extracted 45 lines total
First 10 lines for debugging:
  0: ORDER NO: 001
  1: Name: John Smith
  2: 2900 Plano Pkwy 9876543210 John Smith
  ...

→ Found address line: name='John Smith', addr='2900 Plano Pkwy'
→ Found box type: 2 Comfort Box
→ Found rice type: Pulav Rice
✓ Completed row: {'name': 'John Smith', 'address': '2900 Plano Pkwy', 'box_type': '2 Comfort Box', 'rice_type': 'Pulav Rice'}
→ Found address line: name='Jane Doe', addr='3400 W Plano Pkwy'
...

Extracted 42 complete rows from image:
  Row 1: {'name': 'John Smith', 'address': '2900 Plano Pkwy', 'box_type': '2 Comfort Box', 'rice_type': 'Pulav Rice'}
  Row 2: {'name': 'Jane Doe', 'address': '3400 W Plano Pkwy', 'box_type': '3 Comfort Box', 'rice_type': 'White Rice'}
  ...
```

Each row will show the name, address, box type, and rice type properly aligned.

## Testing

To verify the fix works with sample data:

```bash
python3 test_extraction.py
```

This will test the extraction logic with sample OCR data and confirm it produces correctly aligned rows.

## Files Modified

- `update_template.py` - Core extraction logic completely rewritten
  - Old: Independent field collection → Combined by index
  - New: Row-by-row processing with address as anchor

- `test_extraction.py` - New test file to validate the logic

- `DATA_ALIGNMENT_FIX.md` - Technical details of the fix

## Benefits

✓ **Correct Data Pairing** - Names always match with their addresses  
✓ **Reliable Extraction** - Works even if OCR finds fields in different order  
✓ **Better Debugging** - Clear console output showing each row being processed  
✓ **Maintains Compatibility** - GUI and command-line interfaces unchanged  

## If Issues Persist

1. Check the console output for "Completed row" messages to see what was extracted
2. Look at the first 10 lines of OCR output to verify image format is recognized
3. Make sure addresses in your image match: "2900 Plano Pkwy" or "3400 W Plano Pkwy"
4. Verify box types match one of: Comfort Box, Kabuli Chana Box, Moong Dal Box, Rajma Box
5. Verify rice types are: Pulav Rice or White Rice

## Next Steps

1. Run the script with your actual image
2. Review the debug output to ensure rows are being extracted correctly
3. Check the PDF output to verify all data is properly aligned
4. If any fields are still missing, share the debug output for further investigation

---

**Questions?** The extraction logic is now much more robust. If you encounter any issues, the detailed console output will help diagnose the problem.
