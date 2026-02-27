# Project Structure Overview

## Directory Tree

```
AV_LunchBox_StickerPDF/
│
├── av_lunchbox_stickerpdf/          ⭐ NEW MODULAR PACKAGE
│   ├── __init__.py                  Package initialization & exports
│   │
│   ├── core/                        Core business logic
│   │   ├── __init__.py
│   │   ├── models.py                Data models (Order, Summary, enums)
│   │   └── pdf_generator.py         PDF generation from Word templates
│   │
│   ├── data/                        Data extraction & sources
│   │   ├── __init__.py
│   │   ├── sheets_handler.py        Google Sheets client + extractor
│   │   └── image_extractor.py       OCR-based image extraction
│   │
│   ├── report/                      Report generation
│   │   ├── __init__.py
│   │   └── summary_generator.py     Summary creation & file writing
│   │
│   ├── cli/                         Command-line interface
│   │   ├── __init__.py
│   │   └── main.py                  CLI entry point & orchestration
│   │
│   ├── config/                      Configuration management
│   │   ├── __init__.py
│   │   ├── app_config.py            Application paths & settings
│   │   └── logging_config.py        Logging configuration
│   │
│   ├── utils/                       Utility functions
│   │   ├── __init__.py
│   │   └── file_utils.py            File & directory utilities
│   │
│   └── gui/                         GUI interface (future)
│       └── __init__.py              (Placeholder for GUI)
│
├── src/                             Original scripts (reference only)
│   ├── generate_pdf.py              Original PDF generator
│   ├── generate_pdf_wrapper.py       ⭐ NEW backward compatible wrapper
│   ├── google_sheets_handler.py      Original sheets handler
│   ├── sheets_extractor.py           Original extractor
│   ├── summary_generator.py          Original summary generator
│   ├── pdf_generator_gui.py          GUI implementation
│   ├── requirements.txt              Python dependencies
│   └── setup.sh                      Setup script
│
├── templates/                       Word templates
│   └── AR_Template.docx             Lunch box order template
│
├── tests/                           Test suite
│   ├── test_extraction.py
│   ├── test_sheets.py
│   ├── debug_*.py
│   └── analyze_sheet_structure.py
│
├── exports/                         Generated files
│   └── YYYY-MM-DD/
│       ├── *.pdf                    Generated PDFs
│       └── *.txt                    Summary reports
│
├── docs/                            Documentation
│   ├── GETTING_STARTED.md
│   ├── SHEETS_API_REFERENCE.md
│   ├── TROUBLESHOOTING.md
│   ├── SHEETS_SETUP.md
│   ├── RESTRUCTURING_COMPLETE.md    ⭐ NEW detailed docs
│   ├── archive/                     Archived docs
│   └── *.md                         Other docs
│
├── RESTRUCTURING_SUMMARY.md         ⭐ NEW migration summary
├── QUICK_START_NEW.md               ⭐ NEW quick start guide
├── QUICK_COMMANDS.md                Quick reference
├── README.md                        Main README
├── setup.py                         ⭐ NEW package setup
└── .gitignore                       Git ignore rules
```

## Module Details

### Core Module (`av_lunchbox_stickerpdf/core/`)

**Purpose:** Core business logic and data models

#### `models.py`
- `Order` - Data class for individual orders
- `Summary` - Data class for summary reports
- `BoxType` - Enum for box types
- `RiceType` - Enum for rice types

#### `pdf_generator.py`
- `PDFGenerator` - Generates PDFs from Word templates
- Handles cross-platform PDF conversion
- Manages document layout and formatting

### Data Module (`av_lunchbox_stickerpdf/data/`)

**Purpose:** Data extraction from various sources

#### `sheets_handler.py`
- `GoogleSheetsClient` - Fetches data via CSV export
- `OrderExtractor` - Converts rows to Order objects
- Handles column mapping and filtering

#### `image_extractor.py`
- `ImageOCRExtractor` - Extracts orders from images
- Performs OCR using pytesseract
- Parses order details from text

### Report Module (`av_lunchbox_stickerpdf/report/`)

**Purpose:** Report generation and output

#### `summary_generator.py`
- `SummaryGenerator` - Creates summary statistics
- `SummaryWriter` - Saves summaries to files
- Formats box counts and address breakdowns

### CLI Module (`av_lunchbox_stickerpdf/cli/`)

**Purpose:** Command-line interface

#### `main.py`
- `CLI` - Main CLI class
- `main()` - Entry point function
- Handles argument parsing and orchestration

### Config Module (`av_lunchbox_stickerpdf/config/`)

**Purpose:** Configuration and settings management

#### `app_config.py`
- `AppConfig` - Centralized configuration
- Path definitions
- Application settings

#### `logging_config.py`
- `setup_logging()` - Configure logging
- `logger` - Default logger instance

### Utils Module (`av_lunchbox_stickerpdf/utils/`)

**Purpose:** Utility and helper functions

#### `file_utils.py`
- `clean_directory()` - Remove directory contents
- `create_dated_export_dir()` - Create dated exports
- `get_timestamp_filename()` - Generate timestamped filenames
- `list_files_in_directory()` - List files with filtering

## Usage Patterns

### Pattern 1: Full Workflow (Recommended)

```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()
pdf_path = cli.generate_from_sheets("spreadsheet-id")
```

### Pattern 2: Custom Workflow

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor
from av_lunchbox_stickerpdf.core import PDFGenerator
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

# Extract
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

### Pattern 3: Component Usage

```python
# Use individual components
from av_lunchbox_stickerpdf.core import Order
from av_lunchbox_stickerpdf.report import SummaryGenerator

order = Order("John", "123 Main", "Veg Box", "Pulav")
summary = SummaryGenerator.generate([order])
```

## File Organization Principles

1. **Single Responsibility** - Each module does one thing well
2. **Clear Dependencies** - Modules clearly import what they need
3. **Type Safety** - Full type hints throughout
4. **Documentation** - Docstrings and comments for clarity
5. **Testability** - Modules designed for unit testing
6. **Reusability** - Components can be used independently

## Benefits of This Structure

| Benefit | Example |
|---------|---------|
| **Modularity** | Import only what you need |
| **Maintainability** | Small, focused files |
| **Testability** | Easy to test components |
| **Scalability** | Easy to add features |
| **Type Safety** | Full IDE support |
| **Documentation** | Clear module purposes |
| **Flexibility** | Mix and match components |
| **Professionalism** | Industry-standard layout |

## Installation & Running

### Development Installation
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
pip install -e .
```

### Using CLI
```bash
python -m av_lunchbox_stickerpdf.cli sheets SPREADSHEET_ID
python -m av_lunchbox_stickerpdf.cli image image.png
```

### Using Python API
```python
from av_lunchbox_stickerpdf.cli import CLI
cli = CLI()
cli.generate_from_sheets("id")
```

## Next Steps

1. **Read** `docs/RESTRUCTURING_COMPLETE.md` for detailed documentation
2. **Try** examples in `QUICK_START_NEW.md`
3. **Explore** module docstrings in the package
4. **Contribute** improvements and features
5. **Extend** with new modules as needed

## Key Improvements Over Original

| Aspect | Before | After |
|--------|--------|-------|
| **Code Organization** | Monolithic | Modular |
| **Reusability** | Low | High |
| **Testing** | Difficult | Easy |
| **Type Hints** | Minimal | Full |
| **Dependencies** | Implicit | Explicit |
| **Configuration** | Hardcoded | Centralized |
| **Extensibility** | Limited | Excellent |
| **Documentation** | Scattered | Organized |

## Support

- **Quick Start:** `QUICK_START_NEW.md`
- **Detailed Docs:** `docs/RESTRUCTURING_COMPLETE.md`
- **Migration:** `RESTRUCTURING_SUMMARY.md`
- **Original Scripts:** `src/` (reference only)

---

**Version:** 2.0.0  
**Status:** ✅ Complete and Ready to Use  
**Last Updated:** February 2026
