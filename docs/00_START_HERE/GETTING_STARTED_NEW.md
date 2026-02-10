# Quick Start Guide - New Modular Structure

## Installation

```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

# Install dependencies
pip install -r src/requirements.txt

# Install the package in development mode
pip install -e .
```

## Running the Application

### Option 1: Using CLI (Recommended)

```bash
# Generate from Google Sheets
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
python -m av_lunchbox_stickerpdf.cli sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI

# Generate from image
python -m av_lunchbox_stickerpdf.cli image path/to/image.png
```

### Option 2: Using Python Script

```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()

# From Google Sheets
pdf_path = cli.generate_from_sheets("1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")

# From image
pdf_path = cli.generate_from_image("order_image.png")
```

### Option 3: Backward Compatible Wrapper

```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF/src
python generate_pdf_wrapper.py --sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
python generate_pdf_wrapper.py --image path/to/image.png
```

## Working with Individual Components

### Extract Orders from Google Sheets

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor

# Fetch data
client = GoogleSheetsClient()
rows, columns = client.fetch_csv_data("1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")

# Extract orders
extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)

for order in orders:
    print(f"{order.name}: {order.box_type}")
```

### Extract Orders from Image

```python
from av_lunchbox_stickerpdf.data import ImageOCRExtractor

extractor = ImageOCRExtractor()
orders = extractor.extract_from_image("image.png")

print(f"Found {len(orders)} orders")
```

### Generate PDF from Orders

```python
from av_lunchbox_stickerpdf.core import PDFGenerator

generator = PDFGenerator("templates/AR_Template.docx")
generator.generate(orders, "output.pdf")
```

### Generate Summary Report

```python
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

# Generate summary text
summary_text = SummaryGenerator.generate(orders)
print(summary_text)

# Save to file
SummaryWriter.save_summary(summary_text, "exports", "summary.txt")
```

## Module Organization

### `core/` - Core Business Logic
- `models.py` - Data models (Order, Summary, etc.)
- `pdf_generator.py` - PDF generation from templates

### `data/` - Data Extraction
- `sheets_handler.py` - Google Sheets integration
- `image_extractor.py` - OCR-based image extraction

### `report/` - Report Generation
- `summary_generator.py` - Summary creation and file writing

### `cli/` - Command-Line Interface
- `main.py` - CLI entry points

### `config/` - Configuration
- `app_config.py` - Application paths and settings
- `logging_config.py` - Logging setup

### `utils/` - Utilities
- `file_utils.py` - File and directory operations

## File Locations

- **Templates:** `templates/AR_Template.docx`
- **Exports:** `exports/YYYY-MM-DD/`
  - PDFs: `exports/YYYY-MM-DD/YYYY-MM-DD_HH:MM AM/PM.pdf`
  - Summaries: `exports/YYYY-MM-DD/YYYY-MM-DD_HH:MM AM/PM.txt`
- **Old scripts:** `src/` (for reference only)
- **Documentation:** `docs/`

## Key Features

✓ **Modular Design** - Easy to import and use individual components
✓ **Type Hints** - Full type annotations for IDE support
✓ **Configuration Management** - Centralized settings
✓ **Logging** - Consistent logging across modules
✓ **File Utilities** - Helper functions for common operations
✓ **Backward Compatible** - Wrapper scripts for old code
✓ **Extensible** - Easy to add new features

## Configuration

Edit `av_lunchbox_stickerpdf/config/app_config.py` to customize:
- Output directories
- Template paths
- Google Sheets timeout
- Export cleanup behavior

## Troubleshooting

### Import Errors
Ensure the package is installed: `pip install -e .`

### Template Not Found
Check that `templates/AR_Template.docx` exists

### PDF Conversion Failed
Install LibreOffice: `brew install libreoffice` (macOS)

### Google Sheets Not Loading
- Verify spreadsheet ID is correct and public
- Check internet connection
- Try refreshing the sheet

## Next Steps

1. Read `docs/RESTRUCTURING_COMPLETE.md` for detailed documentation
2. Check `docs/GETTING_STARTED.md` for usage examples
3. Run tests: `python -m pytest tests/`
4. Contribute improvements!
