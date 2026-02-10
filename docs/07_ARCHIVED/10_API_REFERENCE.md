# API Reference

Complete API documentation for all modules and classes.

## Table of Contents
1. [Core API](#core-api)
2. [Data Extraction API](#data-extraction-api)
3. [Report Generation API](#report-generation-api)
4. [CLI API](#cli-api)
5. [Configuration API](#configuration-api)
6. [Utilities API](#utilities-api)

---

## Core API

### `av_lunchbox_stickerpdf.core.models`

#### **Order** (Dataclass)
Represents a single lunch box order.

```python
@dataclass
class Order:
    name: str                               # Customer name
    address: str                            # Delivery address
    box_type: str                           # Type of box (e.g., "Veg Comfort Box")
    rice_type: str                          # Type of rice (e.g., "Pulav Rice")
    order_id: Optional[int] = None          # Unique order ID
    timestamp: Optional[datetime] = None    # Order timestamp
    metadata: Optional[Dict[str, Any]] = None  # Additional data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert order to dictionary"""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Order':
        """Create order from dictionary"""
```

#### **BoxType** (Enum)
```python
class BoxType(str, Enum):
    VEG_COMFORT = "Veg Comfort Box"
    NON_VEG_COMFORT = "Non-Veg Comfort Box"
    KABULI_CHANA = "Kabuli Chana Box"
    MOONG_DAL = "Moong Dal Box"
    RAJMA = "Rajma Box"
    UNKNOWN = "Unknown"
```

#### **RiceType** (Enum)
```python
class RiceType(str, Enum):
    PULAV = "Pulav Rice"
    WHITE = "White Rice"
    UNKNOWN = "Unknown"
```

#### **Summary** (Dataclass)
Represents a summary report.

```python
@dataclass
class Summary:
    total_boxes: int                        # Total number of boxes
    box_combinations: Dict[str, int]        # Count by box+rice combo
    address_counts: Dict[str, int]          # Count by address
    generated_at: datetime                  # When summary was created
    date_for: Optional[str] = None          # Date the summary is for
```

### `av_lunchbox_stickerpdf.core.pdf_generator`

#### **PDFGenerator**
Main class for generating PDFs.

```python
class PDFGenerator:
    def __init__(self, template_path: str):
        """Initialize with path to Word template"""
    
    def generate(self, orders: List[Order], output_path: str) -> bool:
        """
        Generate PDF from orders.
        
        Args:
            orders: List of Order objects
            output_path: Path for output PDF
        
        Returns:
            True if successful, False otherwise
        """
```

**Example:**
```python
from av_lunchbox_stickerpdf.core import PDFGenerator, Order

pdf_gen = PDFGenerator("templates/AR_Template.docx")
orders = [
    Order("John Doe", "123 Main St", "Veg Comfort Box", "Pulav Rice"),
    Order("Jane Smith", "456 Oak Ave", "Non-Veg Comfort Box", "White Rice"),
]
success = pdf_gen.generate(orders, "output.pdf")
```

---

## Data Extraction API

### `av_lunchbox_stickerpdf.data.sheets_handler`

#### **GoogleSheetsClient**
Client for accessing public Google Sheets.

```python
class GoogleSheetsClient:
    def __init__(self, timeout: int = 10):
        """Initialize with optional timeout"""
    
    def fetch_csv_data(self, spreadsheet_id: str, sheet_id: int = 0) \
        -> Tuple[List[Dict[str, str]], List[str]]:
        """
        Fetch data from Google Sheet as CSV.
        
        Args:
            spreadsheet_id: Spreadsheet ID from URL
            sheet_id: Sheet tab ID (gid parameter)
        
        Returns:
            Tuple of (rows, column_names)
        """
```

#### **OrderExtractor**
Extracts orders from sheet data.

```python
class OrderExtractor:
    def __init__(self, column_mapping: Optional[Dict[str, str]] = None):
        """
        Initialize with optional column mapping.
        
        Default mapping:
        - 'name': 'Full Name'
        - 'address': 'Address'
        - 'box_type': 'Type of Food'
        - 'rice_type': 'Type of Rice'
        """
    
    def extract_orders_from_rows(self, rows: List[Dict[str, str]]) \
        -> List[Order]:
        """
        Extract multiple orders from sheet rows.
        
        Args:
            rows: List of row dictionaries from CSV
        
        Returns:
            List of Order objects
        """
```

**Example:**
```python
from av_lunchbox_stickerpdf.data import GoogleSheetsClient, OrderExtractor

client = GoogleSheetsClient()
rows, columns = client.fetch_csv_data("1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")

extractor = OrderExtractor()
orders = extractor.extract_orders_from_rows(rows)
```

### `av_lunchbox_stickerpdf.data.image_extractor`

#### **ImageOCRExtractor**
Extracts orders from images using OCR.

```python
class ImageOCRExtractor:
    def extract_from_image(self, image_path: str) -> List[Order]:
        """
        Extract order data from an image.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            List of Order objects extracted from image
        """
```

**Example:**
```python
from av_lunchbox_stickerpdf.data import ImageOCRExtractor

extractor = ImageOCRExtractor()
orders = extractor.extract_from_image("orders.png")
```

---

## Report Generation API

### `av_lunchbox_stickerpdf.report.summary_generator`

#### **SummaryGenerator**
Generates summary reports from orders.

```python
class SummaryGenerator:
    @classmethod
    def generate(cls, orders: List[Order]) -> str:
        """
        Generate summary text from orders.
        
        Args:
            orders: List of Order objects
        
        Returns:
            Formatted summary text
        """
    
    @classmethod
    def generate_summary_object(cls, orders: List[Order], 
                               date_for: Optional[str] = None) -> Summary:
        """
        Generate Summary object from orders.
        
        Args:
            orders: List of Order objects
            date_for: Optional date string
        
        Returns:
            Summary object
        """
```

#### **SummaryWriter**
Writes summaries to files.

```python
class SummaryWriter:
    @staticmethod
    def save_summary(summary_text: str, output_dir: str = "exports", 
                    filename: Optional[str] = None) -> Optional[str]:
        """
        Save summary text to file.
        
        Args:
            summary_text: Summary text to save
            output_dir: Directory for output
            filename: Optional custom filename
        
        Returns:
            Path to saved file, or None if failed
        """
    
    @staticmethod
    def save_summary_from_orders(orders: List[Order], 
                                 output_dir: str = "exports",
                                 filename: Optional[str] = None) \
        -> Optional[str]:
        """
        Generate and save summary from orders.
        
        Args:
            orders: List of Order objects
            output_dir: Directory for output
            filename: Optional custom filename
        
        Returns:
            Path to saved file, or None if failed
        """
```

**Example:**
```python
from av_lunchbox_stickerpdf.report import SummaryGenerator, SummaryWriter

# Generate summary text
summary_text = SummaryGenerator.generate(orders)

# Save to file
path = SummaryWriter.save_summary(summary_text, "exports")
```

---

## CLI API

### `av_lunchbox_stickerpdf.cli.main`

#### **CLI**
Command-line interface handler.

```python
class CLI:
    def __init__(self):
        """Initialize CLI"""
    
    def generate_from_sheets(self, spreadsheet_id: str, 
                            sheet_id: int = 0) -> Optional[str]:
        """
        Generate PDF and summary from Google Sheets.
        
        Args:
            spreadsheet_id: Google Sheets ID
            sheet_id: Sheet tab ID
        
        Returns:
            Path to generated PDF, or None if failed
        """
    
    def generate_from_image(self, image_path: str) -> Optional[str]:
        """
        Generate PDF and summary from image.
        
        Args:
            image_path: Path to image file
        
        Returns:
            Path to generated PDF, or None if failed
        """
```

**Example:**
```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()

# From Google Sheets
pdf_path = cli.generate_from_sheets("1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")

# From image
pdf_path = cli.generate_from_image("orders.png")
```

#### **main()**
Entry point for CLI.

```bash
python -m av_lunchbox_stickerpdf.cli sheets <spreadsheet_id>
python -m av_lunchbox_stickerpdf.cli image <image_path>
```

---

## Configuration API

### `av_lunchbox_stickerpdf.config.app_config`

#### **AppConfig**
Application configuration.

```python
class AppConfig:
    PROJECT_ROOT: Path              # Project root directory
    SRC_DIR: Path                   # Source directory
    TEMPLATES_DIR: Path             # Templates directory
    EXPORTS_DIR: Path               # Exports directory
    DEFAULT_TEMPLATE: Path          # Default template file
    GOOGLE_SHEETS_TIMEOUT: int      # API timeout (10s)
    EXPORT_CLEAN_ON_SHEETS_RUN: bool  # Auto-cleanup flag
    LOG_LEVEL: str                  # Logging level
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
    
    @classmethod
    def get_template_path(cls, template_name: Optional[str] = None) -> Path:
        """Get path to template file"""
    
    @classmethod
    def get_export_dir(cls, date_string: Optional[str] = None) -> Path:
        """Get export directory for date"""
```

**Example:**
```python
from av_lunchbox_stickerpdf.config import AppConfig

template = AppConfig.get_template_path()
exports_dir = AppConfig.get_export_dir("2026-02-10")
```

---

## Utilities API

### `av_lunchbox_stickerpdf.utils.file_utils`

```python
def clean_directory(directory: str) -> bool:
    """Remove all files and subdirectories"""

def create_dated_export_dir(base_dir: str, 
                           date_string: Optional[str] = None) -> Path:
    """Create dated export directory"""

def get_timestamp_filename(extension: str = ".pdf", 
                          format_12h: bool = True) -> str:
    """Generate timestamp-based filename"""

def list_files_in_directory(directory: str, 
                           extension: Optional[str] = None) -> List[str]:
    """List files in directory"""
```

**Example:**
```python
from av_lunchbox_stickerpdf.utils import (
    create_dated_export_dir,
    get_timestamp_filename,
    clean_directory
)

# Create export directory
export_dir = create_dated_export_dir("exports")

# Get timestamp filename
filename = get_timestamp_filename(".pdf")  # "2026-02-10_03-45 PM.pdf"

# Clean directory
clean_directory("exports")
```

---

## Error Handling

Most functions return `None` or `False` on failure with console output:

```python
# Check return value
pdf_path = cli.generate_from_sheets(spreadsheet_id)
if pdf_path is None:
    print("Error: PDF generation failed")

# Check boolean return
success = pdf_generator.generate(orders, output_path)
if not success:
    print("Error: Generation failed")
```

---

## Type Hints

All modules use full type hints for better IDE support:

```python
from typing import List, Optional, Dict, Tuple
from av_lunchbox_stickerpdf.core import Order

def process_orders(orders: List[Order]) -> Dict[str, int]:
    """Count orders by address"""
    ...
```

---

See also: [Project Structure](08_PROJECT_STRUCTURE.md), [Architecture](09_ARCHITECTURE.md)
