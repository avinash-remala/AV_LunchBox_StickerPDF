# Quick Command Reference

## 🚀 Quick Start Commands

### Option 1: Google Sheets Version (Command-Line)

**Generate PDFs from Google Sheets:**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**What happens:**
1. Connects to the Google Sheet
2. Extracts today's lunch box orders
3. Generates a PDF in `exports/YYYY-MM-DD/` folder
4. Uses timestamp for filename (e.g., `2026-02-09_10:12 PM.pdf`)

---

### Option 2: Image OCR Version (Command-Line)

**Generate PDFs from image (OCR):**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx \
  --image /path/to/image.png
```

**Examples:**
```bash
# Current directory
python3 src/generate_pdf.py templates/AR_Template.docx --image screenshot.png

# Specific path
python3 src/generate_pdf.py templates/AR_Template.docx --image ~/Pictures/orders.png

# Desktop
python3 src/generate_pdf.py templates/AR_Template.docx --image ~/Desktop/lunch_orders.png
```

---

### Option 3: GUI Version (Graphical Interface)

**Launch the GUI application:**
```bash
python3 src/pdf_generator_gui.py
```

**What the GUI does:**
1. Opens a file browser to select your template
2. Lets you choose between Google Sheets or Image input
3. For Google Sheets: Enter spreadsheet ID
4. For Image: Browse and select image file
5. Generates PDF with a single click
6. Shows success/error message

---

## 📍 Output Locations

### Google Sheets Output
```
exports/2026-02-09/2026-02-09_10:12 PM.pdf
exports/2026-02-09/2026-02-09_02:45 PM.pdf
exports/2026-02-09/2026-02-09_03:30 PM.pdf
```

### Image Output
```
exports/2026-02-09/
  2026-02-09_10:12 PM.pdf
```

---

## 🔧 Setup Commands (Run Once)

### Install Dependencies
```bash
cd src
pip install -r requirements.txt
pip install requests
```

### Install PDF Converter (Required)

**Mac:**
```bash
brew install libreoffice
```

**Linux:**
```bash
sudo apt-get install libreoffice
```

**Windows:**
```bash
# Download and install from: https://www.libreoffice.org/download/
# OR install Microsoft Office
```

---

## 🧪 Test Commands

### Test Google Sheets Connection
```bash
python3 tests/test_sheets.py
```

### Check Available Dates in Sheet
```bash
python3 tests/debug_dates.py
```

### Test Data Extraction
```bash
python3 tests/test_extraction.py
```

### Analyze Sheet Structure
```bash
python3 tests/analyze_sheet_structure.py
```

---

## 📋 Complete Examples

### Example 1: Generate PDF from Google Sheets (Full Path)
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
python3 src/generate_pdf.py templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**Expected Output:**
```
→ Fetching data from Google Sheet...
→ Found 5 orders for today (2026-02-09)
→ Processing order 1: John Smith
→ Processing order 2: Jane Doe
→ Creating PDF...
✓ PDF saved to: exports/2026-02-09/2026-02-09_10:30 PM.pdf
```

---

### Example 2: Generate PDF from Image File
```bash
python3 src/generate_pdf.py templates/AR_Template.docx \
  --image ~/Desktop/lunch_screenshot.png
```

**Expected Output:**
```
→ Reading image...
→ Performing OCR...
→ Extracted 4 orders
→ Processing order 1: Alex Kumar
→ Processing order 2: Sarah Johnson
→ Creating PDF...
✓ PDF saved to: exports/2026-02-09/2026-02-09_10:30 PM.pdf
```

---

### Example 3: Launch GUI (Interactive)
```bash
python3 src/pdf_generator_gui.py
```

**What You See:**
1. File browser opens for template selection
2. Dialog asks: "Google Sheets or Image?"
3. If Google Sheets → Enter spreadsheet ID
4. If Image → Browse and select image file
5. Success message shows output location

---

## 💡 Useful Tips

### Copy Commands Easily

**Google Sheets (Ready to Paste):**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**Image OCR (Template):**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx --image <YOUR_IMAGE_PATH>
```

### Create Desktop Shortcut (Mac)

**Create an alias:**
```bash
alias generate-lunch-pdf="python3 src/generate_pdf.py templates/AR_Template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"
```

**Then use:**
```bash
generate-lunch-pdf
```

---

## 🎯 Most Common Use Case

If you use Google Sheets daily:

```bash
# Step 1: Open terminal and navigate to project
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

# Step 2: Run the command
python3 src/generate_pdf.py templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI

# Step 3: Check output folder
open exports/
```

---

## 📌 Spreadsheet ID Reference

Your Google Sheet ID: `1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI`

**To find your Google Sheet ID:**
1. Open Google Sheets
2. Look at URL: `https://docs.google.com/spreadsheets/d/{ID}/edit`
3. Copy the ID part

---

## ❓ Troubleshooting Quick Fix

**Command not found?**
```bash
# Add to PATH or use full path
/usr/local/bin/python3 src/generate_pdf.py ...
```

**No orders found?**
```bash
# Check available dates
python3 tests/debug_dates.py
```

**PDF not created?**
```bash
# Make sure LibreOffice is installed
brew install libreoffice  # Mac
```

**Image file not found?**
```bash
# Use full path
python3 src/generate_pdf.py templates/AR_Template.docx --image ~/Desktop/image.png
```

---

## 🔗 Related Documentation

- See [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md) for detailed setup
- See [`docs/SHEETS_SETUP.md`](docs/SHEETS_SETUP.md) for Google Sheets configuration
- See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) for common issues
- See [`docs/REFACTORING_SUMMARY.md`](docs/REFACTORING_SUMMARY.md) for file naming changes

---

**Last Updated**: February 10, 2026  
**Version**: 2.0 (Post-Refactoring)
