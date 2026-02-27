# Project Structure & Architecture

Complete overview of the new modular package structure.

## Table of Contents
1. [Directory Structure](#directory-structure)
2. [Package Modules](#package-modules)
3. [Module Responsibilities](#module-responsibilities)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)

## Directory Structure

```
AV_LunchBox_StickerPDF/
│
├── av_lunchbox_stickerpdf/          # Main Python package
│   ├── __init__.py                  # Package entry point
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── models.py                # Data models (Order, Summary)
│   │   └── pdf_generator.py         # PDF generation
│   ├── data/                        # Data extraction
│   │   ├── __init__.py
│   │   ├── sheets_handler.py        # Google Sheets extraction
│   │   └── image_extractor.py       # Image/OCR extraction
│   ├── report/                      # Report generation
│   │   ├── __init__.py
│   │   └── summary_generator.py     # Summary reports
│   ├── cli/                         # Command-line interface
│   │   ├── __init__.py
│   │   └── main.py                  # CLI entry point
│   ├── gui/                         # GUI interface (future)
│   │   └── __init__.py
│   ├── config/                      # Configuration
│   │   ├── __init__.py
│   │   ├── app_config.py            # App settings
│   │   └── logging_config.py        # Logging setup
│   └── utils/                       # Utilities
│       ├── __init__.py
│       └── file_utils.py            # File operations
│
├── src/                             # Legacy source (will be deprecated)
│   ├── generate_pdf.py              # Main script
│   ├── google_sheets_handler.py     # Legacy sheets handler
│   ├── sheets_extractor.py          # Legacy extractor
│   ├── pdf_generator_gui.py         # GUI script
│   ├── summary_generator.py         # Legacy summary
│   ├── requirements.txt             # Python dependencies
│   └── setup.sh                     # Setup script
│
├── templates/                       # Word templates
│   └── AR_Template.docx             # Main template
│
├── exports/                         # Generated files
│   └── YYYY-MM-DD/
│       ├── *.pdf                    # Generated PDFs
│       └── *.txt                    # Summary reports
│
├── tests/                           # Test scripts
│   ├── test_extraction.py
│   ├── test_sheets.py
│   └── *.py
│
├── docs/                            # Documentation (27 files)
│   ├── 00_DOCUMENTATION_INDEX.md
│   ├── 01_QUICK_START.md
│   ├── 02_INSTALLATION.md
│   ├── 03_SETUP_VERIFICATION.md
│   ├── 04_USAGE_GUIDE.md
│   ├── 05_GOOGLE_SHEETS_GUIDE.md
│   ├── 06_IMAGE_INPUT_GUIDE.md
│   ├── 07_OUTPUT_FILES.md
│   ├── 08_PROJECT_STRUCTURE.md      # This file
│   ├── 09_ARCHITECTURE.md
│   ├── 10_API_REFERENCE.md
│   ├── 11_CONTRIBUTING.md
│   ├── 12_PDF_GENERATION.md
│   ├── 13_SUMMARY_GENERATION.md
│   ├── 14_DATA_EXTRACTION.md
│   ├── 15_CLEANUP_FEATURE.md
│   ├── 16_CONFIGURATION.md
│   ├── 17_GOOGLE_SHEETS_SETUP.md
│   ├── 18_ENVIRONMENT_SETUP.md
│   ├── 19_TROUBLESHOOTING.md
│   ├── 20_FAQ.md
│   ├── 21_ERROR_CODES.md
│   ├── 22_REFACTORING_ROADMAP.md
│   ├── 23_REFACTORING_ANALYSIS.md
│   ├── 24_MIGRATION_GUIDE.md
│   ├── 25_CHANGELOG.md
│   ├── 26_RELEASE_NOTES.md
│   ├── 27_MAINTENANCE.md
│   └── archive/                     # Archived docs
│
├── setup.py                         # Package installation
├── pyproject.toml                   # Project metadata
├── README.md                        # Project overview
└── QUICK_COMMANDS.md                # Quick command reference

```

## Package Modules

### 1. **core/** - Core Functionality

#### `models.py`
- **Order**: Data model for a single order
- **Summary**: Data model for summary reports
- **BoxType**: Enum for box types
- **RiceType**: Enum for rice types

#### `pdf_generator.py`
- **PDFGenerator**: Main PDF generation class
- Handles Word template loading and population
- Converts DOCX to PDF using LibreOffice

### 2. **data/** - Data Extraction

#### `sheets_handler.py`
- **GoogleSheetsClient**: Fetches data from public Google Sheets
- **OrderExtractor**: Extracts order data from sheet rows
- Supports flexible column mapping

#### `image_extractor.py`
- **ImageOCRExtractor**: Extracts orders from images using OCR
- Cleans and normalizes OCR text
- Handles name/address/box type extraction

### 3. **report/** - Reporting

#### `summary_generator.py`
- **SummaryGenerator**: Generates summary text from orders
- **SummaryWriter**: Saves summaries to files
- Counts boxes by type and address

### 4. **cli/** - Command Line Interface

#### `main.py`
- **CLI**: Command-line interface handler
- Supports `sheets` and `image` subcommands
- Orchestrates data extraction, PDF generation, and reporting

### 5. **config/** - Configuration

#### `app_config.py`
- **AppConfig**: Application configuration
- Defines directory paths
- Manages settings like export directory

#### `logging_config.py`
- **setup_logging()**: Configure logging
- Default logger instance

### 6. **utils/** - Utilities

#### `file_utils.py`
- `clean_directory()`: Remove directory contents
- `create_dated_export_dir()`: Create timestamped folders
- `get_timestamp_filename()`: Generate timestamp filenames
- `list_files_in_directory()`: List directory contents

## Module Responsibilities

### Data Flow Architecture

```
Input Sources
    ├── Google Sheets
    │   └── GoogleSheetsClient.fetch_csv_data()
    │       └── OrderExtractor.extract_orders_from_rows()
    │           └── List[Order]
    │
    └── Image File
        └── ImageOCRExtractor.extract_from_image()
            └── List[Order]

Processing
    └── List[Order]
        ├── PDFGenerator.generate(orders, output_path)
        │   └── PDF File
        │
        └── SummaryGenerator.generate(orders)
            └── SummaryWriter.save_summary()
                └── TXT File

Output
    ├── PDF in exports/YYYY-MM-DD/
    ├── TXT in exports/YYYY-MM-DD/
    └── Both with matching timestamps
```

## Design Patterns

### 1. **Separation of Concerns**
Each module has a single responsibility:
- Data extraction ← `data/` modules
- PDF generation ← `core/` modules
- Reporting ← `report/` modules
- CLI ← `cli/` modules

### 2. **Data Models**
Use `Order` and `Summary` dataclasses for type safety:
```python
from av_lunchbox_stickerpdf.core import Order

order = Order(
    name="John Doe",
    address="123 Main St",
    box_type="Veg Comfort Box",
    rice_type="Pulav Rice"
)
```

### 3. **Configuration Management**
Centralized configuration in `AppConfig`:
```python
from av_lunchbox_stickerpdf.config import AppConfig

template_path = AppConfig.DEFAULT_TEMPLATE
exports_dir = AppConfig.EXPORTS_DIR
```

### 4. **Error Handling**
Modules return `None` or `False` on failure with console messages:
```python
result = pdf_generator.generate(orders, output_path)
if not result:
    print("✗ PDF generation failed")
```

## Dependency Graph

```
cli/main.py
    ├→ config/app_config.py
    ├→ data/sheets_handler.py
    │   └→ core/models.py
    ├→ data/image_extractor.py
    │   └→ core/models.py
    ├→ core/pdf_generator.py
    │   └→ core/models.py
    ├→ report/summary_generator.py
    │   └→ core/models.py
    └→ utils/file_utils.py
```

## Module Import Examples

### From CLI:
```python
from av_lunchbox_stickerpdf.cli import CLI
cli = CLI()
pdf_path = cli.generate_from_sheets("spreadsheet_id")
```

### From Python Code:
```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor
from av_lunchbox_stickerpdf.core import PDFGenerator
from av_lunchbox_stickerpdf.report import SummaryGenerator

# Extract orders
client = GoogleSheetsClient()
rows, _ = client.fetch_csv_data(spreadsheet_id)
extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)

# Generate PDF
pdf_gen = PDFGenerator("templates/AR_Template.docx")
pdf_gen.generate(orders, "output.pdf")

# Generate summary
summary = SummaryGenerator.generate(orders)
```

## Migration from Legacy Code

### Old Way (src/)
```python
# src/generate_pdf.py
from generate_pdf import extract_table_data_from_image
data = extract_table_data_from_image("image.png")
```

### New Way (av_lunchbox_stickerpdf/)
```python
# Using CLI
from av_lunchbox_stickerpdf.cli import CLI
cli = CLI()
cli.generate_from_image("image.png")

# Or using modules directly
from av_lunchbox_stickerpdf.data import ImageOCRExtractor
extractor = ImageOCRExtractor()
orders = extractor.extract_from_image("image.png")
```

---

See also: [Architecture](09_ARCHITECTURE.md), [API Reference](10_API_REFERENCE.md)
