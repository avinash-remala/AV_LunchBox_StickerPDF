# PDF Generation from Lunch Box Google Sheets

A Python application to automatically extract lunch box order data from a Google Sheet and generate formatted PDFs from a Word template.

## Project Structure

```
.
├── src/                          # Main source code
│   ├── generate_pdf.py           # Main PDF generation script
│   ├── summary_generator.py      # Summary report generation ⭐ NEW
│   ├── google_sheets_handler.py  # Google Sheets data extraction
│   ├── sheets_extractor.py       # Flexible sheets handler
│   ├── pdf_generator_gui.py      # GUI version for Mac
│   ├── requirements.txt          # Python dependencies
│   └── setup.sh                  # Setup script
│
├── tests/                         # Test and debug scripts
│   ├── test_sheets.py            # Test Google Sheets integration
│   ├── test_extraction.py        # Test data extraction
│   ├── debug_*.py                # Debug utilities
│   └── analyze_sheet_structure.py# Sheet analysis tools
│
├── docs/                          # Documentation
│   ├── SUMMARY_GENERATOR.md      # Summary feature guide ⭐ NEW
│   ├── GETTING_STARTED.md        # Getting started guide
│   ├── SHEETS_API_REFERENCE.md   # Sheets API reference
│   ├── TROUBLESHOOTING.md        # Troubleshooting guide
│   └── *.md                      # Additional documentation
│
├── exports/                       # Generated files
│   └── YYYY-MM-DD/
│       ├── *.pdf                 # Generated PDF files
│       └── *.txt                 # Summary reports ⭐ NEW
│
├── templates/                     # Word templates
│   └── AR_Template.docx          # Lunch box order template
│
└── README.md                      # This file
```

## Quick Start

### Installation

1. **Install Python dependencies:**
   ```bash
   cd src
   pip install -r requirements.txt
   pip install requests
   ```

2. **Verify Google Sheet access:**
   - Ensure your Google Sheet is publicly accessible or you have sharing permissions
   - Get your Spreadsheet ID from the URL: `docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/...`

### Usage

#### Option 1: Command-Line Version (Mac/Linux/Windows)

**Generate PDF from Google Sheets:**
```bash
python3 src/generate_pdf.py --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

This will:
- ✓ Extract order data from Google Sheets
- ✓ Generate formatted PDF from template
- ✓ **Create summary report (NEW)** ⭐
- ✓ Save all files to `exports/YYYY-MM-DD/` with timestamp

**Generate PDF from Image (OCR):**
```bash
python3 src/generate_pdf.py --image path/to/image.png
```

#### Option 2: GUI Version (Mac)

**Run the GUI application:**
```bash
python3 src/pdf_generator_gui.py
```

The GUI provides an easy-to-use interface to:
- Select your Word template
- Choose image file (OCR extraction)
- Generate PDFs with a single click
- **Automatic summary generation** ⭐

**Output Location:**
The PDF will be saved in `exports/YYYY-MM-DD/` folder with the format: `YYYY-MM-DD_HH:MM AM/PM.pdf`

**Summary Report (NEW):** A text file with the same timestamp is automatically created alongside the PDF containing:
- Total box count
- Breakdown by box type (Veg/Non-Veg + Rice Type combinations)
- Distribution by delivery address

**Example output:**
```
exports/2026-02-10/
├── 2026-02-10_11:15 AM.pdf     # Generated sticker PDF
└── 2026-02-10_11:15 AM.txt     # Summary report ⭐ NEW
```

The date folder is automatically created if it doesn't exist.

For more details on the summary feature, see [SUMMARY_GENERATOR.md](docs/SUMMARY_GENERATOR.md).

## Features

### Google Sheets Integration
- **Automatic Data Extraction**: Reads lunch box orders from public Google Sheets
- **Handles Merged Cells**: Correctly processes merged date cells across multiple rows
- **Date Filtering**: Automatically extracts orders for today's date
- **Multiple Orders**: Supports extracting all orders (even duplicates for the same person)

### Data Extraction
Extracts the following information from Google Sheets:
- Order Number (S No)
- Customer Full Name
- Delivery Address
- Phone Number
- Type of Food (Veg/Non-Veg)
- Type of Rice (White Rice/Pulav Rice)
- Comments/Special Instructions

### PDF Generation
- **Dynamic Template Expansion**: Automatically adds rows to the template based on number of orders
- **Smart Formatting**: Applies markers based on food and rice type combinations
  - `--- VW ---` for Veg Comfort Box + White Rice
  - `--- VP ---` for Veg Comfort Box + Pulav Rice
  - `--- NVW ---` for Non-Veg Comfort Box + White Rice
  - `--- NVP ---` for Non-Veg Comfort Box + Pulav Rice
- **Cross-Platform PDF Conversion**: Uses LibreOffice, docx2pdf, or unoconv

### Summary Generation ⭐ NEW
- **Automatic Reports**: Creates summary text file alongside every PDF
- **Order Statistics**: Total box count and breakdown by type
- **Address Distribution**: Shows boxes per delivery address
- **Same Naming**: Summary uses same timestamp as PDF for easy matching
- **Same Location**: Saves to same `exports/YYYY-MM-DD/` folder

Example summary report:
```
TOTAL BOXES: 17

Boxes (count by type)
•	Veg Comfort Box + Pulav Rice: 11
•	Non-Veg Comfort Box + Pulav Rice: 6
•	Veg Comfort Box + White Rice: 0
•	Non-Veg Comfort Box + White Rice: 0

Addresses (total boxes per address)
•	2900 Plano Pkwy: 12 boxes
•	3400 W Plano Pkwy: 5 boxes
```

See [SUMMARY_GENERATOR.md](docs/SUMMARY_GENERATOR.md) for detailed documentation.

## Testing

Run test scripts to verify the setup:

```bash
# Test Google Sheets integration
python3 tests/test_sheets.py

# Test data extraction
python3 tests/test_extraction.py

# Analyze sheet structure
python3 tests/analyze_sheet_structure.py
```

## System Requirements

- **Python**: 3.8+
- **Dependencies**: See `src/requirements.txt`
- **PDF Conversion**: One of:
  - LibreOffice (recommended for Mac/Linux)
  - Microsoft Word (Windows)
  - docx2pdf package

### Mac Installation

```bash
# Install LibreOffice for PDF conversion
brew install libreoffice

# Install Python dependencies
pip3 install -r src/requirements.txt
pip3 install requests
```

### Linux Installation

```bash
# Install LibreOffice
sudo apt-get install libreoffice

# Install Python dependencies
pip3 install -r src/requirements.txt
pip3 install requests
```

### Windows Installation

```bash
# Install LibreOffice or have Microsoft Office installed
# Then install Python dependencies
pip install -r src/requirements.txt
pip install requests
pip install docx2pdf
```

## Troubleshooting

- **"sheets_handler module not found"**: Ensure you're running the script from the correct directory or adjust the import path
- **"requests module not found"**: Run `pip install requests`
- **PDF conversion fails**: Install LibreOffice or docx2pdf (see System Requirements)
- **Google Sheet not found**: Verify the Spreadsheet ID and that the sheet is publicly accessible
- **No orders found**: Check that the Google Sheet contains data for today's date in the Date column

For detailed troubleshooting, see `docs/TROUBLESHOOTING.md`

## Documentation

For detailed documentation, see the `docs/` folder:
- `README_COMPLETE.md` - Complete implementation details
- `GOOGLE_SHEETS_INTEGRATION.md` - Google Sheets setup guide
- `GOOGLE_SHEETS_GUIDE.md` - Data extraction guide
- `SHEETS_VS_OCR.md` - Comparison of Google Sheets vs OCR methods
- `INDEX.md` - Documentation index
- `TROUBLESHOOTING.md` - Common issues and solutions

## Development

### Running from Source

**Command-Line Version (Google Sheets):**
```bash
# Navigate to project root
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

# Run main script with Google Sheets
python3 src/update_template.py Templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**Command-Line Version (Image/OCR):**
```bash
python3 src/update_template.py Templates/AR_Template.docx \
  --image path/to/image.png
```

**GUI Version:**
```bash
# Run the GUI application
python3 src/update_template_gui.py
```

### Building GUI Executable (Windows)

To create a standalone Windows executable from the GUI:

```bash
cd src
pyinstaller update_template_gui.spec
```

The compiled executable will be available in the `dist/` folder and can be run without Python installed.

## Output

Generated PDFs are saved in organized folders:
- **Google Sheets exports:** `exports/YYYY-MM-DD/YYYY-MM-DD_HH:MM AM/PM.pdf`
- **Image exports:** `exports/YYYY-MM-DD_HH:MM AM/PM.pdf`

Date folders are automatically created when needed.

**Example:** `exports/2026-02-09/2026-02-09_10:12 PM.pdf`

## License

This project is for internal use by the lunch box delivery service.

## Support

For issues or questions, refer to:
1. `docs/TROUBLESHOOTING.md` for common problems
2. `docs/README_COMPLETE.md` for detailed documentation
3. Run test scripts in `tests/` folder to diagnose issues
