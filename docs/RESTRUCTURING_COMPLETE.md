# Restructuring Complete ✓

This document describes the new modular package structure for the AV Lunch Box Sticker PDF Generator.

## New Package Structure

```
av_lunchbox_stickerpdf/                 # Main package root
├── __init__.py                         # Package initialization
│
├── core/                               # Core business logic
│   ├── __init__.py
│   ├── models.py                       # Data models (Order, Summary, enums)
│   └── pdf_generator.py                # PDF generation from orders
│
├── data/                               # Data extraction
│   ├── __init__.py
│   ├── sheets_handler.py               # Google Sheets client and extraction
│   └── image_extractor.py              # Image OCR extraction
│
├── report/                             # Report generation
│   ├── __init__.py
│   └── summary_generator.py            # Summary generation and writing
│
├── cli/                                # Command-line interface
│   ├── __init__.py
│   └── main.py                         # CLI entry points and logic
│
├── gui/                                # GUI interface (future)
│   ├── __init__.py
│   └── (GUI implementation goes here)
│
├── config/                             # Configuration management
│   ├── __init__.py
│   ├── app_config.py                   # Application settings
│   └── logging_config.py               # Logging configuration
│
└── utils/                              # Utility functions
    ├── __init__.py
    └── file_utils.py                   # File and directory utilities
```

## Module Descriptions

### `core/models.py`
Data models with type hints and validation.

**Key Classes:**
- `Order`: Represents a single lunch box order
- `Summary`: Represents a summary report
- `BoxType`: Enum for box types (Veg, Non-Veg, etc.)
- `RiceType`: Enum for rice types (Pulav, White)

```python
from av_lunchbox_stickerpdf.core import Order

order = Order(
    name="John Doe",
    address="2900 Plano Pkwy",
    box_type="Veg Comfort Box",
    rice_type="Pulav Rice"
)
```

### `core/pdf_generator.py`
Generates PDFs from Word templates.

```python
from av_lunchbox_stickerpdf.core import PDFGenerator

generator = PDFGenerator("templates/AR_Template.docx")
generator.generate(orders, "output.pdf")
```

### `data/sheets_handler.py`
Fetches and parses Google Sheets data.

**Key Classes:**
- `GoogleSheetsClient`: Fetches data via CSV export
- `OrderExtractor`: Extracts orders from sheet rows

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor

client = GoogleSheetsClient()
rows, columns = client.fetch_csv_data(spreadsheet_id)

extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)
```

### `data/image_extractor.py`
Extracts orders from images using OCR.

```python
from av_lunchbox_stickerpdf.data import ImageOCRExtractor

extractor = ImageOCRExtractor()
orders = extractor.extract_from_image("image.png")
```

### `report/summary_generator.py`
Generates and saves summary reports.

**Key Classes:**
- `SummaryGenerator`: Generates summary text
- `SummaryWriter`: Writes summaries to files

```python
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

summary_text = SummaryGenerator.generate(orders)
SummaryWriter.save_summary(summary_text, "exports", "summary.txt")
```

### `cli/main.py`
Command-line interface.

**Key Class:**
- `CLI`: Main CLI handler

```bash
# Generate from Google Sheets
python -m av_lunchbox_stickerpdf.cli sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI

# Generate from image
python -m av_lunchbox_stickerpdf.cli image image.png
```

### `config/app_config.py`
Application configuration and paths.

```python
from av_lunchbox_stickerpdf.config import AppConfig

config = AppConfig()
print(config.EXPORTS_DIR)
print(config.DEFAULT_TEMPLATE)
```

### `utils/file_utils.py`
File and directory utilities.

```python
from av_lunchbox_stickerpdf.utils import (
    clean_directory,
    create_dated_export_dir,
    get_timestamp_filename
)
```

## Migration Guide

### For Existing Code Using Old Scripts

The old scripts (`generate_pdf.py`, `google_sheets_handler.py`, etc.) in the `src/` directory have been kept for reference.

For new code, use the modular structure:

**Old way:**
```python
from google_sheets_handler import get_todays_lunch_orders
data = get_todays_lunch_orders(spreadsheet_id)
```

**New way:**
```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor

client = GoogleSheetsClient()
rows, columns = client.fetch_csv_data(spreadsheet_id)

extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)
```

## Usage Examples

### Example 1: Generate from Google Sheets (Recommended)

```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()
pdf_path = cli.generate_from_sheets("1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")
```

### Example 2: Generate from Image

```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()
pdf_path = cli.generate_from_image("order_image.png")
```

### Example 3: Custom Workflow

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor
from av_lunchbox_stickerpdf.core import PDFGenerator
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter
from av_lunchbox_stickerpdf.utils import create_dated_export_dir, get_timestamp_filename

# 1. Fetch data
client = GoogleSheetsClient()
rows, _ = client.fetch_csv_data(spreadsheet_id)

# 2. Extract orders
extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)

# 3. Generate PDF
export_dir = create_dated_export_dir("exports")
pdf_path = export_dir / get_timestamp_filename(".pdf")
generator = PDFGenerator("templates/AR_Template.docx")
generator.generate(orders, str(pdf_path))

# 4. Generate summary
summary_text = SummaryGenerator.generate(orders)
SummaryWriter.save_summary(summary_text, str(export_dir), "summary.txt")
```

## Running the CLI

### Using Python Module
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

# From Google Sheets
python -m av_lunchbox_stickerpdf.cli sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI

# From image
python -m av_lunchbox_stickerpdf.cli image path/to/image.png
```

### Using Direct Script
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF/src

# Backward compatible wrapper
python generate_pdf_wrapper.py --sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
python generate_pdf_wrapper.py --image path/to/image.png
```

## Benefits of New Structure

1. **Modularity**: Each module has a single responsibility
2. **Reusability**: Components can be imported and used independently
3. **Testability**: Isolated modules are easier to test
4. **Maintainability**: Clear organization makes code maintenance easier
5. **Scalability**: Easy to add new features without affecting existing code
6. **Type Safety**: Full type hints throughout the codebase
7. **Configuration**: Centralized configuration management
8. **Logging**: Consistent logging across all modules

## Testing

Tests should be organized under `tests/` and import from the new package:

```python
import pytest
from av_lunchbox_stickerpdf.core import Order
from av_lunchbox_stickerpdf.data import GoogleSheetsClient

def test_order_creation():
    order = Order("John", "123 Main St", "Veg Comfort Box", "Pulav Rice")
    assert order.name == "John"
    assert order.to_dict()["address"] == "123 Main St"
```

## Next Steps

1. Update existing tests to use the new package structure
2. Add unit tests for each module
3. Add integration tests for workflows
4. Create documentation for each module
5. Set up CI/CD pipeline for automated testing
