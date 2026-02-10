# Professional Refactoring Implementation Plan

## Executive Summary

After analyzing the AV LunchBox StickerPDF project, we've identified opportunities for professional-grade refactoring to improve:
- Code organization and maintainability
- Separation of concerns
- Type safety and data models
- Configuration management
- Logging and debugging
- Extensibility and scalability

**Estimated Time: 14-18 hours** (can be done incrementally)

---

## Current Issues Analysis

### Critical Issues

#### 1. **Mixed Responsibilities** ⚠️ CRITICAL
```python
# generate_pdf.py (632 lines) contains:
- OCR extraction logic (150+ lines)
- Google Sheets integration (100+ lines)
- Word document manipulation (200+ lines)
- PDF conversion logic (100+ lines)
- Summary generation orchestration (20+ lines)
- CLI argument parsing (50+ lines)
```

**Impact:** Hard to test, modify, or reuse individual components

#### 2. **Duplicate Functionality**
- `google_sheets_handler.py` - Handles sheet data fetching
- `sheets_extractor.py` - Also handles sheet data extraction
- Both do similar things; need consolidation

**Impact:** Code duplication, maintenance burden, confusion

#### 3. **No Data Models**
```python
# Using raw dicts everywhere:
orders = [
    {'name': 'John', 'address': '...', 'box_type': 'Veg', 'rice_type': 'Pulav'},
    # Can't catch typos, no IDE support, no validation
]
```

**Impact:** Type errors not caught until runtime

#### 4. **Hardcoded Configuration**
```python
# Spreadsheet ID hardcoded in documentation
# No environment variables
# No config file support
```

**Impact:** Unsafe for production, hard to switch contexts

#### 5. **No Logging System**
```python
# Using print() everywhere
print("Processing...")
print("Done")
```

**Impact:** No log levels, can't disable output, no timestamps

---

## Refactoring Roadmap

### Phase 1: Create Package Structure (2 hours)

#### Step 1.1: Create Package Directory
```bash
mkdir -p src/av_lunchbox_stickerpdf/{core,document,report,cli,gui,config,utils}
```

#### Step 1.2: Create __init__.py Files
```python
# src/av_lunchbox_stickerpdf/__init__.py
__version__ = "1.0.0"
__author__ = "AV Team"

from .core.models import Order, Summary
from .document.pdf_generator import PDFGenerator
from .report.summary_generator import SummaryGenerator

__all__ = ["Order", "Summary", "PDFGenerator", "SummaryGenerator"]
```

#### Step 1.3: Create Version File
```python
# src/av_lunchbox_stickerpdf/__version__.py
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/__version__.py`
- [ ] `src/av_lunchbox_stickerpdf/core/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/document/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/report/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/cli/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/gui/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/config/__init__.py`
- [ ] `src/av_lunchbox_stickerpdf/utils/__init__.py`

---

### Phase 2: Create Core Data Models (1.5 hours)

#### Step 2.1: Create models.py
```python
# src/av_lunchbox_stickerpdf/core/models.py
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Order:
    """Represents a single lunch box order"""
    name: str
    address: str
    box_type: str
    rice_type: str
    
    def __post_init__(self):
        """Validate order data"""
        if not self.name or not self.address:
            raise ValueError("Name and address are required")

@dataclass
class Summary:
    """Represents order statistics summary"""
    total_boxes: int
    box_counts: Dict[str, int]
    address_counts: Dict[str, int]
    
    @property
    def formatted_summary(self) -> str:
        """Return formatted summary string"""
        lines = [f"TOTAL BOXES: {self.total_boxes}\n"]
        # ... formatting logic ...
        return "\n".join(lines)
```

#### Step 2.2: Create data validation
```python
# src/av_lunchbox_stickerpdf/utils/validators.py
from typing import List
from av_lunchbox_stickerpdf.core.models import Order

def validate_orders(orders: List[Order]) -> bool:
    """Validate order list"""
    if not orders:
        raise ValueError("Orders list cannot be empty")
    for order in orders:
        if not isinstance(order, Order):
            raise TypeError(f"Expected Order, got {type(order)}")
    return True

def validate_spreadsheet_id(spreadsheet_id: str) -> bool:
    """Validate Google Sheets ID"""
    if not spreadsheet_id or not isinstance(spreadsheet_id, str):
        raise ValueError("Invalid spreadsheet ID")
    return True
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/core/models.py` (40 lines)
- [ ] `src/av_lunchbox_stickerpdf/utils/validators.py` (50 lines)

---

### Phase 3: Extract Core Data Extraction (2.5 hours)

#### Step 3.1: Create Abstract Base
```python
# src/av_lunchbox_stickerpdf/core/data_extractor.py
from abc import ABC, abstractmethod
from typing import List
from .models import Order

class DataExtractor(ABC):
    """Abstract base class for data extraction"""
    
    @abstractmethod
    def extract(self) -> List[Order]:
        """Extract orders from source"""
        pass
```

#### Step 3.2: Create OCR Extractor
```python
# src/av_lunchbox_stickerpdf/core/ocr_extractor.py
from typing import List
from pathlib import Path
from .data_extractor import DataExtractor
from .models import Order

class OCRExtractor(DataExtractor):
    """Extract orders from image using OCR"""
    
    def __init__(self, image_path: str):
        self.image_path = Path(image_path)
        self.logger = get_logger(__name__)
    
    def extract(self) -> List[Order]:
        """Extract orders from image"""
        # Move OCR logic from generate_pdf.py here
        pass
```

#### Step 3.3: Create Sheets Extractor
```python
# src/av_lunchbox_stickerpdf/core/sheets_extractor.py
from typing import List
from .data_extractor import DataExtractor
from .models import Order

class SheetsExtractor(DataExtractor):
    """Extract orders from Google Sheets"""
    
    def __init__(self, spreadsheet_id: str, sheet_id: int = 0):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id
        self.logger = get_logger(__name__)
    
    def extract(self) -> List[Order]:
        """Extract orders from Google Sheets"""
        # Consolidate logic from google_sheets_handler.py
        pass
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/core/data_extractor.py` (20 lines)
- [ ] `src/av_lunchbox_stickerpdf/core/ocr_extractor.py` (150 lines - moved from generate_pdf.py)
- [ ] `src/av_lunchbox_stickerpdf/core/sheets_extractor.py` (120 lines - consolidated)

#### Files to Consolidate
- [ ] Delete `src/google_sheets_handler.py` (move to sheets_extractor)
- [ ] Keep `src/sheets_extractor.py` for backward compatibility initially

---

### Phase 4: Extract Document Generation (2.5 hours)

#### Step 4.1: Create DOCX Processor
```python
# src/av_lunchbox_stickerpdf/document/docx_processor.py
from pathlib import Path
from typing import List
from docx import Document

class DocxProcessor:
    """Handle DOCX file manipulation"""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.logger = get_logger(__name__)
    
    def update_with_orders(self, orders: List[Order]) -> Path:
        """Update template with order data"""
        # Move DOCX manipulation logic here
        pass
```

#### Step 4.2: Create PDF Converter
```python
# src/av_lunchbox_stickerpdf/document/pdf_converter.py
from pathlib import Path

class PDFConverter:
    """Handle DOCX to PDF conversion"""
    
    def convert(self, docx_path: str, pdf_path: str) -> bool:
        """Convert DOCX to PDF"""
        # Move conversion logic here
        pass
```

#### Step 4.3: Create Main Generator
```python
# src/av_lunchbox_stickerpdf/document/pdf_generator.py
from typing import List
from .docx_processor import DocxProcessor
from .pdf_converter import PDFConverter

class PDFGenerator:
    """Orchestrate PDF generation"""
    
    def __init__(self, template_path: str = "templates/AR_Template.docx"):
        self.template_path = template_path
        self.docx_processor = DocxProcessor(template_path)
        self.pdf_converter = PDFConverter()
    
    def generate(self, orders: List[Order], output_dir: str = "exports") -> str:
        """Generate PDF from orders"""
        # Orchestrate the process
        pass
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/document/docx_processor.py` (200 lines - moved from generate_pdf.py)
- [ ] `src/av_lunchbox_stickerpdf/document/pdf_converter.py` (100 lines - moved from generate_pdf.py)
- [ ] `src/av_lunchbox_stickerpdf/document/pdf_generator.py` (100 lines - orchestration)

---

### Phase 5: Move Report Generation (1 hour)

#### Step 5.1: Move Summary Generator
```bash
mv src/summary_generator.py src/av_lunchbox_stickerpdf/report/summary_generator.py
```

#### Step 5.2: Update imports in summary_generator.py
```python
# Update imports to use new package structure
from av_lunchbox_stickerpdf.core.models import Order, Summary
```

#### Files to Update
- [ ] Move `src/summary_generator.py` → `src/av_lunchbox_stickerpdf/report/summary_generator.py`
- [ ] Update imports in the moved file

---

### Phase 6: Create Configuration Management (1 hour)

#### Step 6.1: Create Settings
```python
# src/av_lunchbox_stickerpdf/config/settings.py
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration"""
    spreadsheet_id: str = os.getenv("LUNCH_BOX_SPREADSHEET_ID", "")
    sheet_id: int = int(os.getenv("LUNCH_BOX_SHEET_ID", "0"))
    template_path: Path = Path("templates/AR_Template.docx")
    export_dir: Path = Path("exports")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def from_env(cls):
        """Load from environment variables"""
        return cls()
    
    def validate(self):
        """Validate configuration"""
        if not self.spreadsheet_id:
            raise ValueError("LUNCH_BOX_SPREADSHEET_ID not set")
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")
```

#### Step 6.2: Create Constants
```python
# src/av_lunchbox_stickerpdf/config/constants.py
# Application constants
APP_NAME = "AV Lunch Box Sticker PDF"
APP_VERSION = "1.0.0"

# Box type combinations
BOX_TYPES = [
    "Veg Comfort Box + Pulav Rice",
    "Non-Veg Comfort Box + Pulav Rice",
    "Veg Comfort Box + White Rice",
    "Non-Veg Comfort Box + White Rice",
]

# Date/time format
OUTPUT_FORMAT = "%Y-%m-%d_%I:%M %p"

# Timeouts
SHEETS_TIMEOUT = 10
PDF_CONVERSION_TIMEOUT = 60
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/config/settings.py` (50 lines)
- [ ] `src/av_lunchbox_stickerpdf/config/constants.py` (40 lines)

---

### Phase 7: Create Utilities (1.5 hours)

#### Step 7.1: Create Logger
```python
# src/av_lunchbox_stickerpdf/utils/logger.py
import logging
from av_lunchbox_stickerpdf.config import AppConfig

def get_logger(name: str, config: AppConfig = None) -> logging.Logger:
    """Get configured logger"""
    if config is None:
        config = AppConfig.from_env()
    
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(config.log_level)
    
    return logger
```

#### Step 7.2: Create File Handler
```python
# src/av_lunchbox_stickerpdf/utils/file_handler.py
from pathlib import Path
from typing import Optional

class FileHandler:
    """Handle file operations"""
    
    @staticmethod
    def ensure_dir(path: Path) -> None:
        """Create directory if it doesn't exist"""
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def save_file(content: str, path: Path) -> bool:
        """Save content to file"""
        try:
            FileHandler.ensure_dir(path.parent)
            path.write_text(content)
            return True
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            return False
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/utils/logger.py` (40 lines)
- [ ] `src/av_lunchbox_stickerpdf/utils/file_handler.py` (50 lines)
- [ ] `src/av_lunchbox_stickerpdf/utils/__init__.py` (imports)

---

### Phase 8: Create CLI Entry Point (1.5 hours)

#### Step 8.1: Create Main CLI
```python
# src/av_lunchbox_stickerpdf/cli/main.py
import argparse
import sys
from av_lunchbox_stickerpdf.core import SheetsExtractor, OCRExtractor
from av_lunchbox_stickerpdf.document import PDFGenerator
from av_lunchbox_stickerpdf.report import SummaryGenerator

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AV Lunch Box Sticker PDF Generator"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Sheets subcommand
    sheets_parser = subparsers.add_parser('sheets', help='Generate from Google Sheets')
    sheets_parser.add_argument('--spreadsheet-id', required=True, help='Google Sheets ID')
    sheets_parser.add_argument('--sheet-id', type=int, default=0, help='Sheet ID')
    sheets_parser.set_defaults(func=cmd_sheets)
    
    # Image subcommand
    image_parser = subparsers.add_parser('image', help='Generate from image')
    image_parser.add_argument('--image', required=True, help='Image file path')
    image_parser.set_defaults(func=cmd_image)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

def cmd_sheets(args):
    """Handle sheets command"""
    print(f"Generating from Google Sheets: {args.spreadsheet_id}")
    extractor = SheetsExtractor(args.spreadsheet_id, args.sheet_id)
    orders = extractor.extract()
    
    if not orders:
        print("No orders found")
        return
    
    print(f"Found {len(orders)} orders")
    
    generator = PDFGenerator()
    pdf_path = generator.generate(orders)
    print(f"✓ PDF: {pdf_path}")
    
    summary_gen = SummaryGenerator()
    summary_path = summary_gen.generate(orders)
    print(f"✓ Summary: {summary_path}")

def cmd_image(args):
    """Handle image command"""
    print(f"Generating from image: {args.image}")
    extractor = OCRExtractor(args.image)
    orders = extractor.extract()
    
    if not orders:
        print("No orders found")
        return
    
    generator = PDFGenerator()
    pdf_path = generator.generate(orders)
    summary_path = SummaryGenerator().generate(orders)
    
    print(f"✓ PDF: {pdf_path}")
    print(f"✓ Summary: {summary_path}")

if __name__ == '__main__':
    main()
```

#### Files to Create
- [ ] `src/av_lunchbox_stickerpdf/cli/main.py` (100 lines)
- [ ] `src/av_lunchbox_stickerpdf/cli/__init__.py`

---

### Phase 9: Update Entry Points (1 hour)

#### Step 9.1: Create setup.py
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="av-lunchbox-stickerpdf",
    version="1.0.0",
    author="AV Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'lunch-box=av_lunchbox_stickerpdf.cli.main:main',
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        "python-docx>=0.8.11",
        "requests>=2.25.0",
        "Pillow>=9.0.0",
        "pytesseract>=0.3.10",
    ],
)
```

#### Step 9.2: Create __main__.py for module execution
```python
# src/av_lunchbox_stickerpdf/__main__.py
if __name__ == '__main__':
    from .cli.main import main
    main()
```

#### Files to Create
- [ ] `setup.py` (35 lines)
- [ ] `src/av_lunchbox_stickerpdf/__main__.py` (5 lines)

---

### Phase 10: Update Documentation (1 hour)

#### Files to Update
- [ ] Update `README.md` with new structure
- [ ] Create `API_REFERENCE.md`
- [ ] Update `QUICK_COMMANDS.md` with new commands
- [ ] Create migration guide

---

## Implementation Checklist

### Phase 1: Package Structure
- [ ] Create directory structure
- [ ] Create all `__init__.py` files
- [ ] Create `__version__.py`

### Phase 2: Data Models
- [ ] Create `models.py`
- [ ] Create `validators.py`
- [ ] Add type hints throughout

### Phase 3: Core Extraction
- [ ] Create abstract `DataExtractor`
- [ ] Create `OCRExtractor`
- [ ] Create `SheetsExtractor`
- [ ] Test extraction independently

### Phase 4: Document Generation
- [ ] Create `DocxProcessor`
- [ ] Create `PDFConverter`
- [ ] Create `PDFGenerator`
- [ ] Test generation independently

### Phase 5: Report Generation
- [ ] Move `SummaryGenerator`
- [ ] Update imports
- [ ] Test independently

### Phase 6: Configuration
- [ ] Create `settings.py`
- [ ] Create `constants.py`
- [ ] Add environment variable support

### Phase 7: Utilities
- [ ] Create `logger.py`
- [ ] Create `file_handler.py`
- [ ] Create `validators.py` (if not done)

### Phase 8: CLI
- [ ] Create CLI entry point
- [ ] Test CLI commands
- [ ] Add help text

### Phase 9: Entry Points
- [ ] Create `setup.py`
- [ ] Create `__main__.py`
- [ ] Test module execution

### Phase 10: Documentation
- [ ] Update README
- [ ] Create API reference
- [ ] Update quick commands
- [ ] Create migration guide

---

## Backward Compatibility

### Keep Legacy Entry Points
Initially, keep old scripts working:
```python
# src/generate_pdf.py (wrapper)
from av_lunchbox_stickerpdf.cli.main import main
import sys

if __name__ == '__main__':
    sys.argv[0] = 'generate_pdf.py'
    # Convert old-style args to new style
    main()
```

### Gradual Deprecation
```python
import warnings

def old_function():
    warnings.warn(
        "old_function() is deprecated, use new_function() instead",
        DeprecationWarning,
        stacklevel=2
    )
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_models.py
def test_order_creation():
    order = Order(name="John", address="123 Main", box_type="Veg", rice_type="Pulav")
    assert order.name == "John"

# tests/test_extractors.py
def test_sheets_extractor():
    extractor = SheetsExtractor("test_id")
    orders = extractor.extract()
    assert len(orders) > 0
```

### Integration Tests
```python
# tests/test_integration.py
def test_full_workflow():
    extractor = SheetsExtractor("test_id")
    orders = extractor.extract()
    
    generator = PDFGenerator()
    pdf_path = generator.generate(orders)
    
    assert Path(pdf_path).exists()
```

---

## Timeline Estimate

| Phase | Task | Hours |
|-------|------|-------|
| 1 | Package Structure | 2.0 |
| 2 | Data Models | 1.5 |
| 3 | Core Extraction | 2.5 |
| 4 | Document Generation | 2.5 |
| 5 | Report Generation | 1.0 |
| 6 | Configuration | 1.0 |
| 7 | Utilities | 1.5 |
| 8 | CLI | 1.5 |
| 9 | Entry Points | 1.0 |
| 10 | Documentation | 1.0 |
| **Total** | | **15.5 hours** |

---

## Next Steps

1. **Review this plan** - Any changes or preferences?
2. **Start Phase 1** - Create package structure
3. **Iterate** - One phase at a time
4. **Test** - Test each phase before moving to next
5. **Document** - Update docs as we go

**Ready to proceed?** Let me know if you'd like to:
- [ ] Start Phase 1 immediately
- [ ] Modify any parts of the plan
- [ ] Take a different approach
- [ ] Ask clarifying questions

