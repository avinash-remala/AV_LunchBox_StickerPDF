# 📖 API Reference

Complete API documentation for all public modules.

## Core Module: av_lunchbox_stickerpdf.core

### Order (Data Class)

```python
from av_lunchbox_stickerpdf.core import Order

order = Order(
    name: str,
    address: str,
    box_type: str,
    rice_type: str,
    order_id: Optional[int] = None,
    timestamp: Optional[datetime] = None,
    metadata: Optional[Dict] = None
)

# Methods
order.to_dict() → Dict  # Convert to dictionary
Order.from_dict(data: Dict) → Order  # Create from dictionary
```

### PDFGenerator (Class)

```python
from av_lunchbox_stickerpdf.core import PDFGenerator

generator = PDFGenerator(template_path: str)

# Methods
generator.generate(orders: List[Order], output_path: str) → bool
```

## Data Module: av_lunchbox_stickerpdf.data

### GoogleSheetsClient (Class)

```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient

client = GoogleSheetsClient(timeout: int = 10)

# Methods
client.fetch_csv_data(
    spreadsheet_id: str,
    sheet_id: int = 0
) → Tuple[List[Dict], List[str]]
```

### OrderExtractor (Class)

```python
from av_lunchbox_stickerpdf.data import OrderExtractor

extractor = OrderExtractor(column_mapping: Optional[Dict] = None)

# Methods
extractor.extract_orders_from_rows(rows: List[Dict]) → List[Order]
extractor.find_today_row(rows: List[Dict]) → Optional[Dict]
extractor.extract_single_row(row: Dict, row_index: int) → Order
```

### ImageOCRExtractor (Class)

```python
from av_lunchbox_stickerpdf.data import ImageOCRExtractor

extractor = ImageOCRExtractor()

# Methods
extractor.extract_from_image(image_path: str) → List[Order]
```

## Report Module: av_lunchbox_stickerpdf.report

### SummaryGenerator (Class)

```python
from av_lunchbox_stickerpdf.report import SummaryGenerator

# Methods (all static)
SummaryGenerator.generate(orders: List[Order]) → str
SummaryGenerator.generate_summary_object(
    orders: List[Order],
    date_for: Optional[str] = None
) → Summary
```

### SummaryWriter (Class)

```python
from av_lunchbox_stickerpdf.report import SummaryWriter

# Methods (all static)
SummaryWriter.save_summary(
    summary_text: str,
    output_dir: str = "exports",
    filename: Optional[str] = None
) → Optional[str]

SummaryWriter.save_summary_from_orders(
    orders: List[Order],
    output_dir: str = "exports",
    filename: Optional[str] = None
) → Optional[str]
```

## CLI Module: av_lunchbox_stickerpdf.cli

### CLI (Class)

```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()

# Methods
cli.generate_from_sheets(
    spreadsheet_id: str,
    sheet_id: int = 0,
    sheet_tab: str = "Name"
) → Optional[str]

cli.generate_from_image(image_path: str) → Optional[str]
```

### main() (Function)

```python
from av_lunchbox_stickerpdf.cli import main

# Entry point
exit_code = main()  # Returns 0 on success, 1 on failure
```

## Config Module: av_lunchbox_stickerpdf.config

### AppConfig (Class)

```python
from av_lunchbox_stickerpdf.config import AppConfig

config = AppConfig()

# Class Attributes
AppConfig.PROJECT_ROOT: Path
AppConfig.TEMPLATES_DIR: Path
AppConfig.EXPORTS_DIR: Path
AppConfig.DEFAULT_TEMPLATE: Path
AppConfig.GOOGLE_SHEETS_TIMEOUT: int

# Methods
AppConfig.ensure_directories() → None
AppConfig.get_template_path(template_name: Optional[str]) → Path
AppConfig.get_export_dir(date_string: Optional[str]) → Path
```

## Utils Module: av_lunchbox_stickerpdf.utils

### File Operations

```python
from av_lunchbox_stickerpdf.utils import (
    clean_directory,
    create_dated_export_dir,
    get_timestamp_filename,
    list_files_in_directory
)

# Functions
clean_directory(directory: str) → bool
create_dated_export_dir(base_dir: str, date_string: Optional[str]) → Path
get_timestamp_filename(extension: str = ".pdf", format_12h: bool = True) → str
list_files_in_directory(
    directory: str,
    extension: Optional[str] = None
) → List[str]
```

## Data Models

### Order
Represents a single lunch box order.

**Attributes:**
- name: str - Customer name
- address: str - Delivery address
- box_type: str - Type of box
- rice_type: str - Type of rice
- order_id: Optional[int] - Order identifier
- timestamp: Optional[datetime] - Creation time
- metadata: Optional[Dict] - Additional data

### Summary
Represents a summary report.

**Attributes:**
- total_boxes: int - Total order count
- box_combinations: Dict[str, int] - Count by type
- address_counts: Dict[str, int] - Count by address
- generated_at: datetime - Generation time
- date_for: Optional[str] - Report date

## Enums

### BoxType
Standard box types.

```python
BoxType.VEG_COMFORT = "Veg Comfort Box"
BoxType.NON_VEG_COMFORT = "Non-Veg Comfort Box"
BoxType.KABULI_CHANA = "Kabuli Chana Box"
BoxType.MOONG_DAL = "Moong Dal Box"
BoxType.RAJMA = "Rajma Box"
```

### RiceType
Standard rice types.

```python
RiceType.PULAV = "Pulav Rice"
RiceType.WHITE = "White Rice"
```

## Return Types & Exceptions

### Return Types

- `Optional[str]` - May return a string path or None if failed
- `List[Order]` - List of Order objects
- `Tuple[List[Dict], List[str]]` - Rows and column names
- `bool` - Success/failure

### Common Errors

**ModuleNotFoundError:** Missing dependency
```bash
pip install [package-name]
```

**FileNotFoundError:** Missing template or input file
```bash
# Check file paths
```

**RequestException:** Network error with Google Sheets
```bash
# Check internet connection
# Verify spreadsheet ID
```

## Usage Examples

See `01_USER_GUIDES/` and `02_DEVELOPER_GUIDES/` for complete examples.

---

**Last Updated:** February 10, 2026  
**Version:** 2.0.0
