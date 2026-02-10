# PDF Generation from Lunch Box Google Sheets

A Python application to automatically extract lunch box order data from a Google Sheet and generate formatted PDFs from a Word template.

> **Note**: This project has been professionally refactored with improved naming conventions and organization. See [`REFACTORING_SUMMARY.md`](REFACTORING_SUMMARY.md) for details on naming changes.

## Project Structure

```
.
├── src/                          # Main source code
│   ├── generate_pdf.py           # Main script to generate PDFs
│   ├── pdf_generator_gui.py      # GUI version for Windows/Mac
│   ├── google_sheets_handler.py  # Google Sheets data extraction
│   ├── sheets_extractor.py       # Alternative extraction handler
│   ├── requirements.txt          # Python dependencies
│   └── setup.sh                  # Setup script
│
├── tests/                         # Test and debug scripts
│   ├── test_sheets.py            # Test Google Sheets integration
│   ├── test_extraction.py        # Test data extraction
│   ├── debug_*.py                # Debug utilities
│   ├── analyze_sheet_structure.py# Sheet analysis tools
│   └── advanced_diagnostic.py    # Advanced diagnostics
│
├── docs/                          # Documentation
│   ├── GETTING_STARTED.md        # Getting started guide
│   ├── SHEETS_SETUP.md           # Google Sheets setup guide
│   ├── SHEETS_API_REFERENCE.md   # API reference
│   ├── DATA_EXTRACTION_METHODS.md# Data extraction methods
│   ├── TROUBLESHOOTING.md        # Troubleshooting guide
│   └── archive/                  # Legacy documentation
│
├── output/                        # Generated PDF files
│   └── YYYY-MM-DD/               # Date-organized outputs
│
├── templates/                     # Word templates
│   └── AR_Template.docx          # Lunch box order template
│
├── build/                         # Build outputs (PyInstaller)
│   └── update_template_gui/       # Compiled GUI executable
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
python3 src/generate_pdf.py templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**Generate PDF from Image (OCR):**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx \
  --image path/to/image.png
```

#### Option 2: GUI Version (Windows Recommended)

**Run the GUI application:**
```bash
python3 src/pdf_generator_gui.py
```

The GUI provides an easy-to-use interface to:
- Select your Word template
- Choose between Google Sheets or Image (OCR) input
- Enter your spreadsheet ID or image file path
- Generate PDFs with a single click

**Output Location:**
The PDF will be saved in `output/YYYY-MM-DD/` folder with the format: `YYYY-MM-DD_HH:MM AM/PM.pdf`

**Example output path:** `output/2026-02-09/2026-02-09_10:12 PM.pdf`

The date folder is automatically created if it doesn't exist.

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

- **"google_sheets_handler module not found"**: Ensure you're running the script from the correct directory or adjust the import path
- **"requests module not found"**: Run `pip install requests`
- **PDF conversion fails**: Install LibreOffice or docx2pdf (see System Requirements)
- **Google Sheet not found**: Verify the Spreadsheet ID and that the sheet is publicly accessible
- **No orders found**: Check that the Google Sheet contains data for today's date in the Date column

For detailed troubleshooting, see `docs/TROUBLESHOOTING.md`

## Documentation

For detailed documentation, see the `docs/` folder:
- `GETTING_STARTED.md` - Getting started guide
- `SHEETS_SETUP.md` - Google Sheets setup guide
- `SHEETS_API_REFERENCE.md` - API reference documentation
- `DATA_EXTRACTION_METHODS.md` - Comparison of data extraction methods
- `TROUBLESHOOTING.md` - Common issues and solutions
- `archive/` - Legacy documentation

## Development

### Running from Source

**Command-Line Version (Google Sheets):**
```bash
# Navigate to project root
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

# Run main script with Google Sheets
python3 src/generate_pdf.py templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**Command-Line Version (Image/OCR):**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx \
  --image path/to/image.png
```

**GUI Version:**
```bash
# Run the GUI application
python3 src/pdf_generator_gui.py
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
- **Google Sheets exports:** `output/YYYY-MM-DD/YYYY-MM-DD_HH:MM AM/PM.pdf`
- **Image exports:** `output/YYYY-MM-DD/YYYY-MM-DD_HH:MM AM/PM.pdf`

Date folders are automatically created when needed.

**Example:** `output/2026-02-09/2026-02-09_10:12 PM.pdf`

## License

This project is for internal use by the lunch box delivery service.

## Support

For issues or questions, refer to:
1. `docs/TROUBLESHOOTING.md` for common problems
2. `docs/README_COMPLETE.md` for detailed documentation
3. Run test scripts in `tests/` folder to diagnose issues
