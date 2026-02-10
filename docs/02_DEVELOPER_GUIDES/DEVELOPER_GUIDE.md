# 👨‍💻 Developer Guide

Complete guide for developers using and extending the package.

## Package Overview

The `av_lunchbox_stickerpdf` package is organized into 7 modules:

```
av_lunchbox_stickerpdf/
├── core/       - Data models and PDF generation
├── data/       - Data extraction (sheets, images)
├── report/     - Summary generation
├── cli/        - Command-line interface
├── config/     - Configuration management
├── utils/      - Utility functions
└── gui/        - GUI (future)
```

## Using as a Library

### Installation

```bash
pip install -e /path/to/av_lunchbox_stickerpdf
```

### Basic Usage

```python
from av_lunchbox_stickerpdf.cli import CLI

# Full workflow
cli = CLI()
pdf_path = cli.generate_from_sheets("spreadsheet-id")
```

### Component Usage

```python
# Use individual components
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor
from av_lunchbox_stickerpdf.core import PDFGenerator
from av_lunchbox_stickerpdf.report import SummaryGenerator

# Extract orders from Google Sheets
client = GoogleSheetsClient()
rows, _ = client.fetch_csv_data("spreadsheet-id")

extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)

# Generate PDF
generator = PDFGenerator("templates/AR_Template.docx")
generator.generate(orders, "output.pdf")

# Generate summary
summary = SummaryGenerator.generate(orders)
```

## Module Documentation

### core.models
Data classes for type-safe order handling:

```python
from av_lunchbox_stickerpdf.core import Order, Summary

order = Order(
    name="John Doe",
    address="123 Main St",
    box_type="Veg Comfort Box",
    rice_type="Pulav Rice"
)
```

### data.sheets_handler
Google Sheets extraction:

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor

client = GoogleSheetsClient()
rows, columns = client.fetch_csv_data(spreadsheet_id)

extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)
```

### data.image_extractor
Image-based extraction via OCR:

```python
from av_lunchbox_stickerpdf.data import ImageOCRExtractor

extractor = ImageOCRExtractor()
orders = extractor.extract_from_image("image.png")
```

### core.pdf_generator
PDF generation:

```python
from av_lunchbox_stickerpdf.core import PDFGenerator

generator = PDFGenerator("template.docx")
success = generator.generate(orders, "output.pdf")
```

### report.summary_generator
Summary report creation:

```python
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

summary_text = SummaryGenerator.generate(orders)
SummaryWriter.save_summary(summary_text, "exports")
```

### config.app_config
Configuration management:

```python
from av_lunchbox_stickerpdf.config import AppConfig

config = AppConfig()
print(config.EXPORTS_DIR)
print(config.DEFAULT_TEMPLATE)
```

### utils.file_utils
File operations:

```python
from av_lunchbox_stickerpdf.utils import (
    clean_directory,
    create_dated_export_dir,
    get_timestamp_filename
)

export_dir = create_dated_export_dir("exports")
filename = get_timestamp_filename(".pdf")
```

## Development Setup

```bash
# Clone repo
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

## Code Quality

Type hints are used throughout:

```python
from typing import List, Optional
from av_lunchbox_stickerpdf.core import Order

def process_orders(orders: List[Order]) -> Optional[str]:
    """Process orders and return summary path."""
    # Your code here
    pass
```

## Testing

All modules are designed for testing:

```python
import pytest
from av_lunchbox_stickerpdf.core import Order

def test_order_creation():
    order = Order("John", "123 Main", "Veg Box", "Pulav")
    assert order.name == "John"
```

## Contributing

1. Follow the module structure
2. Add type hints to all functions
3. Write docstrings
4. Test your code
5. Keep modules focused

## Architecture

See `04_ARCHITECTURE/PROJECT_STRUCTURE.md` for:
- Module relationships
- Data flow diagrams
- Design patterns
- Best practices

## API Reference

Detailed API docs in `03_API_REFERENCE/`

## Need Help?

- **Module details:** Check module docstrings
- **Type hints:** Hover in IDE for help
- **Examples:** See `GETTING_STARTED.md`
- **Troubleshooting:** `05_TROUBLESHOOTING/`

---

**Ready to develop?** Start with understanding the modules! 🚀
