# Quick Reference - Data Alignment Fix

## What's Different?

| Aspect | Before | After |
|--------|--------|-------|
| **Extraction Method** | Independent field collection | Sequential row-by-row processing |
| **Data Grouping** | By field type (names, addresses, etc.) | By order (all fields together) |
| **Row Anchor** | Index position (unreliable) | Address line (reliable) |
| **Misalignment Risk** | High (if field counts differ) | Low (address anchors each row) |
| **Debug Info** | Minimal | Detailed row-by-row output |

## Running the Script

**Same as before - no changes to usage:**

```bash
# Command line
python3 update_template.py image.png Templates/AR_Template.docx output.pdf

# GUI
python3 update_template_gui.py
```

## What to Check After Running

1. **Look at console output** for "Completed row" messages
2. **Verify each row has all 4 fields** (name, address, box_type, rice_type)
3. **Check PDF** - Data should be properly aligned

## If Data Still Looks Wrong

See `TROUBLESHOOTING.md` for:
- How to read debug output
- How to identify OCR issues
- How to update patterns
- How to fix common problems

## Key Improvements

✓ Names stay with their addresses  
✓ Box types matched correctly  
✓ Rice types paired properly  
✓ No more duplicate/empty fields  
✓ Handles reordered OCR output  

## What Changed in the Code

**Only one function was rewritten:**
- `extract_table_data_from_image()` in `update_template.py`

**Everything else stayed the same:**
- GUI interface
- PDF conversion
- Document formatting
- Template handling

## For Customization

If you need to support different:
- **Addresses**: Update address_pattern (line 78)
- **Box types**: Update box_pattern (line 79)
- **Rice types**: Update rice_pattern (line 80)

See `TROUBLESHOOTING.md` → "Common Issues & Fixes" for examples.

## Test It First

Before using with real images, validate with sample data:

```bash
python3 test_extraction.py
```

Expected output:
```
✓ ALL TESTS PASSED!
```

---

**Questions?** Check the documentation files in this folder:
- `FIX_EXPLANATION.md` - What was fixed and why
- `DATA_ALIGNMENT_FIX.md` - Technical deep dive
- `TROUBLESHOOTING.md` - How to debug issues
- `CHANGES_SUMMARY.md` - Complete change list
