# PDF Generation from Lunch Box Google Sheets

A Python application to automatically extract lunch box order data from a Google Sheet and generate formatted PDFs from a Word template.

## Project Structure

```
.
├── src/                          # Main source code
│   ├── update_template.py        # Main script to generate PDFs
│   ├── update_template_gui.py    # GUI version for Windows
│   ├── sheets_handler.py         # Google Sheets data extraction
│   ├── flexible_sheets_handler.py# Alternative extraction handler
│   ├── requirements.txt          # Python dependencies
│   └── quickstart.sh             # Quick start script
│
├── tests/                         # Test and debug scripts
│   ├── test_sheets.py            # Test Google Sheets integration
│   ├── test_extraction.py        # Test data extraction
│   ├── debug_*.py                # Debug utilities
│   ├── analyze_sheet_structure.py# Sheet analysis tools
│   └── advanced_diagnostic.py    # Advanced diagnostics
│
├── docs/                          # Documentation
│   ├── README_COMPLETE.md        # Complete documentation
│   ├── GOOGLE_SHEETS_INTEGRATION.md
│   ├── GOOGLE_SHEETS_GUIDE.md
│   ├── INDEX.md
│   ├── SHEETS_VS_OCR.md
│   ├── TROUBLESHOOTING.md
│   ├── SETUP_COMPLETE.txt
│   └── *.md                      # Additional documentation
│
├── exports/                       # Generated PDF files
│   └── *.pdf                     # Output PDFs
│
├── outputs/                       # Build outputs
│   └── update_template_gui.spec  # PyInstaller spec file
│
├── Templates/                     # Word templates
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

#### Generate PDF from Google Sheets

```bash
python3 src/update_template.py Templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

The PDF will be saved in `exports/YYYY-MM-DD/` folder with the format: `YYYY-MM-DD_HH:MM AM/PM.pdf`

**Example output path:** `exports/2026-02-09/2026-02-09_10:12 PM.pdf`

The date folder is automatically created if it doesn't exist.

#### Generate PDF from Image (OCR)

```bash
python3 src/update_template.py src/../Templates/AR_Template.docx \
  --image path/to/image.png
```

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

```bash
# Navigate to project root
cd /Users/avinashremala/Desktop/"PDF Creation From Image - Lunch Boxes"

# Run main script
python3 src/update_template.py Templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

### Building GUI Executable (Windows)

```bash
cd src
pyinstaller update_template_gui.spec
```

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
