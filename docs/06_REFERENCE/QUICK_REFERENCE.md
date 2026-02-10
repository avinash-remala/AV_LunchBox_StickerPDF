# 📋 Quick Reference

Fast lookup for common tasks and commands.

## CLI Commands

### Generate from Google Sheets

```bash
python -m av_lunchbox_stickerpdf.cli sheets SPREADSHEET_ID
```

**Example:**
```bash
python -m av_lunchbox_stickerpdf.cli sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

### Generate from Image

```bash
python -m av_lunchbox_stickerpdf.cli image path/to/image.png
```

## Installation Commands

```bash
# Install dependencies
pip install -r src/requirements.txt

# Install package
pip install -e .

# Verify installation
python -c "from av_lunchbox_stickerpdf import CLI; print('✓ OK')"
```

## File Locations

```
Project Root:  /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

Package:       av_lunchbox_stickerpdf/
Templates:     templates/AR_Template.docx
Exports:       exports/YYYY-MM-DD/
Docs:          docs/
Config:        av_lunchbox_stickerpdf/config/
```

## Google Sheets Setup

1. Create/open Google Sheet with columns:
   - Full Name
   - Address
   - Type of Food
   - Type of Rice

2. Make sheet public:
   - Click "Share"
   - Select "Anyone with the link"

3. Get Spreadsheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
   ```

## Configuration

Edit `av_lunchbox_stickerpdf/config/app_config.py`:

```python
# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
EXPORTS_DIR = PROJECT_ROOT / "exports"

# Settings
EXPORT_CLEAN_ON_SHEETS_RUN = True
GOOGLE_SHEETS_TIMEOUT = 10
LOG_LEVEL = "INFO"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| No module 'docx' | `pip install python-docx` |
| LibreOffice not found | `brew install libreoffice` |
| Spreadsheet not found | Check ID, make sheet public |
| No orders found | Verify column names, check data |
| Permission denied | `chmod 755 exports/` |

## Module Imports

```python
# Core
from av_lunchbox_stickerpdf.core import Order, PDFGenerator

# Data
from av_lunchbox_stickerpdf.data import (
    GoogleSheetsClient,
    OrderExtractor,
    ImageOCRExtractor
)

# Report
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

# CLI
from av_lunchbox_stickerpdf.cli import CLI

# Config
from av_lunchbox_stickerpdf.config import AppConfig

# Utils
from av_lunchbox_stickerpdf.utils import (
    clean_directory,
    create_dated_export_dir,
    get_timestamp_filename
)
```

## Quick Code Examples

### Full Workflow

```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()
pdf = cli.generate_from_sheets("spreadsheet-id")
```

### Custom Workflow

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor
from av_lunchbox_stickerpdf.core import PDFGenerator
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

# Get data
client = GoogleSheetsClient()
rows, _ = client.fetch_csv_data("id")
extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)

# Generate PDF
generator = PDFGenerator("template.docx")
generator.generate(orders, "output.pdf")

# Generate summary
summary = SummaryGenerator.generate(orders)
SummaryWriter.save_summary(summary, "exports")
```

### Extract from Image

```python
from av_lunchbox_stickerpdf.data import ImageOCRExtractor

extractor = ImageOCRExtractor()
orders = extractor.extract_from_image("image.png")
print(f"Found {len(orders)} orders")
```

## Documentation Locations

| Type | Location |
|------|----------|
| Quick Start | `docs/00_START_HERE/` |
| User Guides | `docs/01_USER_GUIDES/` |
| Developer Guides | `docs/02_DEVELOPER_GUIDES/` |
| API Reference | `docs/03_API_REFERENCE/` |
| Architecture | `docs/04_ARCHITECTURE/` |
| Troubleshooting | `docs/05_TROUBLESHOOTING/` |
| Reference | `docs/06_REFERENCE/` |

## System Requirements

- Python 3.8+
- pip (Python package manager)
- LibreOffice (for PDF conversion)
- Tesseract (for OCR)
- Internet connection (for Google Sheets)

## Performance Tips

💡 Use Google Sheets for large datasets  
💡 Use images for quick, one-off orders  
💡 Batch process multiple sheets  
💡 Keep exports folder clean (old files auto-deleted)  

## Keyboard Shortcuts

```bash
# Cancel running command
Ctrl + C

# View history
history | grep av_lunchbox

# Clear screen
clear

# Exit Python shell
exit() or Ctrl + D
```

## Useful Terminal Commands

```bash
# List generated PDFs
ls -lh exports/*/

# Find latest PDF
find exports -name "*.pdf" -newest

# Count orders in summary
grep "TOTAL BOXES" exports/*/*.txt

# See directory structure
tree docs/
```

## Environment Variables

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Run app
python -m av_lunchbox_stickerpdf.cli sheets ID
```

## Version & Help

```bash
# Check version
python -c "import av_lunchbox_stickerpdf; print(av_lunchbox_stickerpdf.__version__)"

# Show help
python -m av_lunchbox_stickerpdf.cli --help
```

---

**Bookmark this page for quick reference!** 🔖
