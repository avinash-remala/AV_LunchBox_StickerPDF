# 🏗️ Architecture Guide

System architecture and design documentation.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│              User Interface Layer                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  CLI (command-line)                                │   │
│  │  GUI (future)                                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Orchestration Layer                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  CLI Main Logic (main.py)                          │   │
│  │  - Coordinate extraction → PDF → Report            │   │
│  │  - Handle user input                               │   │
│  │  - Manage cleanup                                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Business Logic Layer                           │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  PDF Generation  │  │  Report          │                │
│  │  (core/)         │  │  Generation      │                │
│  │                  │  │  (report/)       │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Data Source Layer                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Google Sheets   │  │  Image (OCR)     │                │
│  │  Extractor       │  │  Extractor       │                │
│  │  (data/)         │  │  (data/)         │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Infrastructure Layer                           │
│  ┌──────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │ Configuration│  │  Logging    │  │  File Utils     │    │
│  │ (config/)    │  │  (config/)  │  │  (utils/)       │    │
│  └──────────────┘  └─────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Module Responsibilities

### Core Module (core/)

**Purpose:** Core business logic and data models

**Components:**
- `models.py` - Data classes (Order, Summary, enums)
- `pdf_generator.py` - PDF generation from templates

**Responsibilities:**
- Define data structures
- Handle template manipulation
- Manage PDF conversion

### Data Module (data/)

**Purpose:** Extract data from various sources

**Components:**
- `sheets_handler.py` - Google Sheets client and extractor
- `image_extractor.py` - OCR-based image extraction

**Responsibilities:**
- Fetch external data
- Parse and normalize data
- Return Order objects

### Report Module (report/)

**Purpose:** Generate summary reports

**Components:**
- `summary_generator.py` - Summary creation and file writing

**Responsibilities:**
- Aggregate order statistics
- Format summaries
- Save to files

### CLI Module (cli/)

**Purpose:** Command-line interface

**Components:**
- `main.py` - CLI entry point and orchestration

**Responsibilities:**
- Parse arguments
- Orchestrate workflow
- Handle user interaction

### Config Module (config/)

**Purpose:** Application configuration

**Components:**
- `app_config.py` - Settings and paths
- `logging_config.py` - Logging setup

**Responsibilities:**
- Manage paths
- Store settings
- Configure logging

### Utils Module (utils/)

**Purpose:** Utility functions

**Components:**
- `file_utils.py` - File operations

**Responsibilities:**
- File manipulation
- Directory management
- Timestamp generation

## Data Flow

### From Google Sheets

```
1. User provides Spreadsheet ID
   ↓
2. GoogleSheetsClient fetches CSV
   ↓
3. OrderExtractor parses rows
   ↓
4. Returns List[Order]
   ↓
5. PDFGenerator creates PDF
   ↓
6. SummaryGenerator creates report
   ↓
7. Files saved to exports/
```

### From Image

```
1. User provides image path
   ↓
2. ImageOCRExtractor performs OCR
   ↓
3. Parses extracted text
   ↓
4. Returns List[Order]
   ↓
5. Same as above (steps 5-7)
```

## Design Patterns

### Separation of Concerns
- Each module handles one responsibility
- Clear module boundaries
- Minimal coupling

### Dependency Injection
- Components accept dependencies
- Easy to test with mocks
- Flexible configuration

### Data Models
- Type-safe Order and Summary classes
- Validation in __post_init__
- Easy conversion to/from dict

### Configuration Management
- Centralized AppConfig class
- Environment-aware settings
- Consistent paths

## Class Relationships

```
Order (core.models)
  ↓ used by
GoogleSheetsClient (data)
OrderExtractor (data)
ImageOCRExtractor (data)
  ↓ all return
List[Order]
  ↓ used by
PDFGenerator (core)
SummaryGenerator (report)
  ↓ all process
Order objects
  ↓ produce
PDF + Summary files
```

## Error Handling

**Network Errors:**
- GoogleSheetsClient catches RequestException
- Returns empty list on failure
- User sees clear error message

**File Errors:**
- PDFGenerator handles missing files
- SummaryWriter handles write errors
- Graceful fallbacks provided

**OCR Errors:**
- ImageOCRExtractor handles extraction failures
- Returns best-effort results
- Logs issues for debugging

## Scalability Considerations

### Adding New Data Sources
1. Create new extractor in data/
2. Implement standard interface
3. Return List[Order]
4. Rest of system works unchanged

### Adding New Report Types
1. Create new generator in report/
2. Accept List[Order] as input
3. Generate and save output
4. Reuse existing infrastructure

### Adding Configuration Options
1. Add to AppConfig class
2. Use throughout system
3. Allows environment customization

## Performance

### Optimization Points
- Batch processing of orders
- Streaming CSV parsing
- Lazy template loading
- Caching of configurations

### Bottlenecks
- Google Sheets API latency
- OCR processing time
- PDF generation time
- File I/O operations

## Security Considerations

- Public Google Sheets only (no auth needed)
- File paths validated
- No external code execution
- Input validation on orders

## Future Extensibility

### Planned Features
- GUI interface
- REST API
- Multiple templates
- Database integration
- Plugin system

### Design Ready For
- Easy to add new modules
- Clear extension points
- Modular architecture
- Type hints for safety

---

**Last Updated:** February 10, 2026  
**Version:** 2.0.0
