# Google Sheets Integration - Implementation Summary

## ✅ What's Been Implemented

Your lunch box PDF generator now has full Google Sheets integration! Here's what was added:

### 1. **New Module: `sheets_handler.py`**
   - Fetches data from public Google Sheets using CSV export
   - Automatically finds today's date (handles both `2/9/2026` and `02/09/2026` formats)
   - Extracts customer names, addresses, box types, and rice types
   - Supports multiple orders per day

### 2. **Enhanced `update_template.py`**
   - New command-line argument: `--google-sheet <spreadsheet_id>`
   - Maintains backward compatibility with image OCR (`--image <path>`)
   - Smart date/time formatting in output filenames
   - Automatic PDF generation with LibreOffice

### 3. **Testing & Debugging Scripts**
   - `test_sheets.py` - Verify Google Sheets connection
   - `debug_dates.py` - Check available dates in the sheet
   - `quickstart.sh` - Convenient bash wrapper

### 4. **Documentation**
   - `GOOGLE_SHEETS_GUIDE.md` - Complete usage guide
   - This summary document

## 🚀 Quick Start

### Basic Usage
```bash
python update_template.py Templates/AR_Template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

### Using the Quick Start Script
```bash
./quickstart.sh                    # Generate from Google Sheets
./quickstart.sh test               # Test connection
./quickstart.sh dates              # Check available dates
./quickstart.sh image input.png    # Generate from image (legacy)
```

## 📊 Google Sheet Structure

The sheet should have these columns:
| Column | Format | Example |
|--------|--------|---------|
| Date | MM/DD/YYYY | 2/9/2026 |
| Full Name | Text | Siva Nandipati |
| Address | Text | 2900 Plano Pkwy |
| Type of Food | Text | Veg Comfort Box |
| Type of Rice | Text | White Rice |

**Current Spreadsheet:** [ATT Corporate Lunch box](https://docs.google.com/spreadsheets/d/1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI/edit?pli=1&gid=0#gid=0)

## ✨ Key Features

### ✓ Automatic Date Matching
- Finds all entries for today's date
- Handles date format variations
- Shows closest date if today's data not found

### ✓ Smart Markers
Automatically generates markers based on box/rice combinations:
- **VP** - Veg + Pulav Rice
- **NVP** - Non-Veg + Pulav Rice  
- **VW** - Veg + White Rice
- **NVW** - Non-Veg + White Rice

### ✓ Multi-Order Support
- Handles multiple orders per day
- Automatically adds rows to template as needed
- Fills all data in proper table format

### ✓ Proper Text Formatting
- Customer names: **Bold, centered**
- Addresses: Centered with proper indentation
- Box+Rice types: Centered with special markers
- Markers: **Bold text, +2pt font size**

### ✓ PDF Generation
- Automatic timestamp naming: `2026-02-09_09:50 PM.pdf`
- LibreOffice conversion (macOS/Linux/Windows compatible)
- Fallback methods if LibreOffice unavailable

## 🔧 Technical Details

### Dependencies
- `requests` - HTTP requests for Google Sheets CSV export
- `python-docx` - Word document manipulation
- `pillow` & `pytesseract` - Image OCR (optional, for image input)
- `LibreOffice` - DOCX to PDF conversion

### How It Works

1. **Fetch Data**
   ```
   Google Sheets CSV Export → Parse CSV → Filter today's date
   ```

2. **Extract Orders**
   ```
   CSV rows → Extract name, address, box type, rice type
   ```

3. **Update Template**
   ```
   Template DOCX → Add rows as needed → Fill in data → Format text
   ```

4. **Generate PDF**
   ```
   Formatted DOCX → LibreOffice conversion → PDF output
   ```

## 📋 File Reference

| File | Purpose |
|------|---------|
| `update_template.py` | Main script - handles both Google Sheets and image input |
| `sheets_handler.py` | Google Sheets data fetching module |
| `test_sheets.py` | Test script to verify setup |
| `debug_dates.py` | Debug script to check available dates |
| `quickstart.sh` | Bash wrapper for easy execution |
| `GOOGLE_SHEETS_GUIDE.md` | Detailed user guide |

## 🐛 Troubleshooting

### "No orders found for today"
→ Run `./quickstart.sh dates` to see available dates in the sheet

### "Google Sheet is not accessible"
→ Ensure the sheet is publicly shared or use image input instead

### "PDF conversion fails"
→ Install LibreOffice: `brew install libreoffice` (macOS)

### Import errors
→ Run: `python -m pip install requests --break-system-packages`

## 📈 Example Output

```
Reading data from Google Sheet: 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
Fetching Google Sheet data from: https://docs.google.com/spreadsheets/d/...
Fetched 1590 rows from Google Sheet
Available columns: ['Date', 'S No', 'Address', 'Full Name', 'Phone Number', 'Type of Food', 'Type of Rice', 'Comments', '']
Found 1 entries for today
  Order 1: Siva Nandipati - Veg Comfort Box - White Rice
Extracted 1 orders from today's rows
Loading template: Templates/AR_Template.docx
Template has 10 rows initially
  Line 3: Added marker '--- VW ---' in separate paragraph (bold, +2pt) for Veg Comfort Box - White Rice
Updated 1 data cells from 1 rows

Saving temporary DOCX to: 2026-02-09_09:50 PM_temp.docx
Converting to PDF: 2026-02-09_09:50 PM.pdf
Converting with LibreOffice: /Applications/LibreOffice.app/Contents/MacOS/soffice
PDF created successfully with LibreOffice
Removed temporary file: 2026-02-09_09:50 PM_temp.docx
Successfully updated 1 cells and saved as PDF!
```

## 🎯 Next Steps

1. **Test the integration**: `./quickstart.sh test`
2. **Generate your first PDF**: `./quickstart.sh`
3. **Review the output**: Check the generated PDF
4. **Read the full guide**: `GOOGLE_SHEETS_GUIDE.md`

## 💡 Tips

- Keep the Google Sheet public for easy access
- Use consistent date formats in the sheet (MM/DD/YYYY)
- Add entries to the sheet as soon as orders come in
- Run the script once a day to generate fresh PDFs
- Use the `quickstart.sh` script for convenience

## 🔐 Privacy & Security

- The script uses public CSV export (no API keys needed)
- No data is stored locally permanently
- PDFs are generated in your workspace directory
- All processing is local

---

**Created:** February 9, 2026
**Python Version:** 3.14.3
**Status:** ✅ Tested and working
