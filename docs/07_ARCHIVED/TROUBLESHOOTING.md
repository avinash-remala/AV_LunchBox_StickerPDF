# Troubleshooting Guide

## Issue: Data Still Appears Misaligned in PDF

### Step 1: Run with Debug Output
When you run the script, it prints detailed debug information:

```bash
python3 generate_pdf.py your_image.png templates/AR_Template.docx output.pdf
```

Look for lines like:
```
→ Found address line: name='John Smith', addr='2900 Plano Pkwy'
→ Found box type: 2 Comfort Box
→ Found rice type: Pulav Rice
✓ Completed row: {'name': 'John Smith', 'address': '2900 Plano Pkwy', 'box_type': '2 Comfort Box', 'rice_type': 'Pulav Rice'}
```

### Step 2: Check What OCR Detected
Look at the "First 10 lines for debugging" section:

```
OCR extracted 45 lines total
First 10 lines for debugging:
  0: ORDER NO: 001
  1: Name: John Smith
  2: 2900 Plano Pkwy 9876543210 John Smith
  3: 2 Comfort Box
  4: Pulav Rice
```

**Is the address format correct?**
- ✓ "2900 Plano Pkwy" or "3400 W Plano Pkwy" → Will be recognized
- ✗ "2900 Plano Parkway" or other variations → Won't be recognized

**Is the format of the address line like this?**
- ✓ "2900 Plano Pkwy 9876543210 John Smith" → Correct
- ✓ "Address Name Phone" → Correct
- ✗ Address on separate line from name → May not work

### Step 3: Check Box Types
Look for lines with box quantities:

```
✓ Found box type: 2 Comfort Box
✗ Found box type: 2 Comfert Box  ← Typo in image
✗ Didn't find anything ← Box type format different
```

Supported box types:
- Comfort Box
- Kabuli Chana Box
- Moong Dal Box
- Rajma Box

If you see a different box type in the output (like "Pulav Box"), the pattern needs to be updated.

### Step 4: Check Rice Types
Look for:
```
✓ Found rice type: Pulav Rice
✓ Found rice type: White Rice
✗ Didn't find anything ← Format might be different
```

Supported rice types:
- Pulav Rice
- White Rice

If your images use different names (like "Basmati" or "Brown Rice"), the pattern needs updating.

---

## Common Issues & Fixes

### Issue: "No rows extracted" or "Extracted 0 rows"

**Cause**: Address pattern doesn't match
**Solution**: 
1. Check your image contains "2900 Plano Pkwy" or "3400 W Plano Pkwy"
2. Look at the "First 10 lines" output - is the address there?
3. If address is different, you need to update the pattern in the code

**How to fix in code:**
```python
# Find this line in generate_pdf.py (around line 78):
address_pattern = re.compile(r'(2900 Plano Pkwy|3400 W Plano Pkwy)')

# Change it to include your address pattern:
address_pattern = re.compile(r'(2900 Plano Pkwy|3400 W Plano Pkwy|YOUR_NEW_ADDRESS)')
```

---

### Issue: Names are extracted but boxes/rice are empty

**Cause**: Box or rice pattern doesn't match
**Solution**:
1. Check the "Completed row" output - are box/rice empty?
2. Look at what the OCR detected for box/rice lines
3. Update the pattern if needed

**How to fix box types:**
```python
# Find this line (around line 79):
box_pattern = re.compile(r'(\d+)\s*(Comfort Box|Kabuli Chana Box|Moong Dal Box|Rajma Box)')

# Add your box type:
box_pattern = re.compile(r'(\d+)\s*(Comfort Box|Kabuli Chana Box|Moong Dal Box|Rajma Box|YOUR_BOX_TYPE)')
```

**How to fix rice types:**
```python
# Find this line (around line 80):
rice_pattern = re.compile(r'(Pulav Rice|White Rice)')

# Add your rice type:
rice_pattern = re.compile(r'(Pulav Rice|White Rice|YOUR_RICE_TYPE)')
```

---

### Issue: Some fields are in wrong order (e.g., Rice before Box Type)

**Cause**: Order varies in the image
**Solution**: The current logic assumes:
1. Address line comes first
2. Box type comes next
3. Rice type comes last

If your image has them in a different order, the extraction might be incomplete. This would require more sophisticated line-grouping logic.

---

### Issue: Multiple names/addresses detected per order

**Cause**: OCR detected text on multiple lines
**Solution**:
1. Look at the "Completed row" output - are there duplicates?
2. The current logic groups by address - the FIRST address is used
3. Subsequent addresses start new rows

**Workaround**: If addresses appear twice per order:
```python
# After extracting address, check if next address is duplicate
if current_row['address'] == extracted_address:
    # Skip this duplicate address
    continue
```

---

### Issue: "Template file not found"

**Cause**: Path to template is incorrect
**Solution**:
1. Make sure `templates/AR_Template.docx` exists in your project folder
2. Check spelling: it should be `templates` (lowercase)
3. Verify the file is named `AR_Template.docx` (exact case)

**How to check:**
```bash
ls -la templates/
# Should show: AR_Template.docx
```

---

### Issue: PDF creation fails but DOCX is created

**Cause**: LibreOffice or equivalent PDF converter not installed
**Solution**: Install one of these:

```bash
# Mac - Install LibreOffice
brew install libreoffice

# Then re-run the script
python3 generate_pdf.py your_image.png templates/AR_Template.docx output.pdf
```

The DOCX file will still be created, which you can manually convert to PDF using:
- Mac Preview: Open DOCX → Export as PDF
- Microsoft Word: Open DOCX → Save As PDF

---

## Getting Help

To troubleshoot effectively, collect this info:

1. **Screenshot of the extracted data** in the PDF
2. **First 20 lines of debug output** from running the script
3. **Expected vs actual data** - What should be there vs what is
4. **Sample of the OCR output** - Check the "First 10 lines" section

With these details, it's easy to diagnose and fix the issue!

---

## Testing Your Changes

After modifying the patterns, test with the sample data:

```bash
python3 test_extraction.py
```

This validates the logic before using real images.

---

**Still stuck?** The debug output is very detailed. Look for patterns in what's being detected vs missed, and update the regex patterns accordingly.
