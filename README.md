# 🍱 AV Lunch Box Sticker PDF Generator

Generate professional lunch box order PDFs and summaries from Google Sheets or images using OCR.

**Version:** 2.1.0 | **Status:** ✅ Production Ready

---

## 🚀 Quick Start

### Installation
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
pip install -e .
```

### Usage

**Using CLI:**
```bash
# Generate from Google Sheets
python -m av_lunchbox_stickerpdf.cli sheets SPREADSHEET_ID

# Generate from image
python -m av_lunchbox_stickerpdf.cli image image.png
```

**Using Python:**
```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()
cli.generate_from_sheets("spreadsheet-id")
```

---

## 📁 Project Structure

```
AV_LunchBox_StickerPDF/
│
├── av_lunchbox_stickerpdf/          ⭐ Main Package (PRODUCTION)
│   ├── core/                        Core business logic
│   ├── data/                        Data extraction
│   ├── report/                      Report generation
│   ├── cli/                         Command-line interface
│   ├── config/                      Configuration
│   ├── utils/                       Utilities
│   └── gui/                         GUI (placeholder)
│
├── src/                             Original scripts (reference)
│   ├── generate_pdf.py
│   ├── google_sheets_handler.py
│   ├── summary_generator.py
│   ├── requirements.txt
│   └── setup.sh
│
├── docs/                            📚 Documentation (organized)
│   ├── guides/                      Usage guides
│   │   ├── GETTING_STARTED_NEW.md  Start here!
│   │   ├── PROJECT_STRUCTURE.md    Architecture
│   │   ├── DOCUMENTATION_INDEX.md  Navigation
│   │   └── QUICK_COMMANDS.md       Common tasks
│   ├── archived/                    Reference docs
│   │   ├── RESTRUCTURING_SUMMARY.md
│   │   ├── RESTRUCTURING_CHECKLIST.md
│   │   └── (other docs)
│   ├── GETTING_STARTED.md          Original guide
│   ├── SHEETS_API_REFERENCE.md     API docs
│   └── TROUBLESHOOTING.md          Common issues
│
├── templates/                       Word templates
│   └── AR_Template.docx
│
├── exports/                         Generated files
│   └── YYYY-MM-DD/
│       ├── *.pdf
│       └── *.txt (summaries)
│
├── tests/                           Test suite (pytest)
│   ├── test_models.py
│   ├── test_markers.py
│   ├── test_summary.py
│   ├── test_file_utils.py
│   ├── test_order_extractor.py
│   └── test_config.py
│
├── pyproject.toml                   Modern Python packaging
├── setup.py                         Legacy package installation
├── README.md                        This file
└── .gitignore

```

---

## 📖 Documentation

### For New Users
Start here: [`docs/guides/GETTING_STARTED_NEW.md`](docs/guides/GETTING_STARTED_NEW.md)

### For Developers
- **Architecture:** [`docs/guides/PROJECT_STRUCTURE.md`](docs/guides/PROJECT_STRUCTURE.md)
- **API Reference:** [`docs/SHEETS_API_REFERENCE.md`](docs/SHEETS_API_REFERENCE.md)
- **Navigation:** [`docs/guides/DOCUMENTATION_INDEX.md`](docs/guides/DOCUMENTATION_INDEX.md)

### For Quick Reference
- **Commands:** [`docs/guides/QUICK_COMMANDS.md`](docs/guides/QUICK_COMMANDS.md)
- **Troubleshooting:** [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)

### Archive (Reference)
Detailed implementation docs in [`docs/archived/`](docs/archived/)

---

## ✨ Features

✅ **PDF Generation** - Create professional sticker PDFs from templates  
✅ **Google Sheets Integration** - Fetch order data automatically  
✅ **OCR Support** - Extract data from images  
✅ **Summary Reports** - Generate text summaries of orders  
✅ **Auto Cleanup** - Clean exports folder before new runs  
✅ **Cross-platform** - Works on Mac, Linux, Windows  

---

## 📦 What's New in v2.1

- ✅ **Proper test suite** — 73 pytest tests covering models, markers, summaries, config, utils
- ✅ **Marker logic module** — Extracted into `core/markers.py` with data-driven design
- ✅ **Special Box support** — `VEG_SPECIAL` and `NON_VEG_SPECIAL` in enums & summaries
- ✅ **Structured logging** — `get_logger()` replaces raw `print()` calls
- ✅ **Modern packaging** — `pyproject.toml` with `[project.optional-dependencies]`
- ✅ **PDFGenerator synced** — Marker logic, bold names, indentation, cell margins
- ✅ **`.gitignore`** — Proper exclusions for `__pycache__`, `dist/`, `.venv/`, etc.

---

## 🔧 Installation

### Requirements
- Python 3.9+
- LibreOffice or equivalent PDF converter

### Setup

1. **Install dependencies:**
   ```bash
   cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
   pip install -e .
   ```

2. **Install dev/test dependencies (optional):**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Verify Google Sheet access:**
   - Ensure your Google Sheet is publicly accessible
   - Get your Spreadsheet ID from the URL: `docs.google.com/spreadsheets/d/{ID}/...`

---

## 💻 Usage

### From Google Sheets
```bash
python -m av_lunchbox_stickerpdf.cli sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**This automatically:**
- ✅ Fetches order data from Google Sheets
- ✅ Generates formatted PDF from template
- ✅ Creates summary report
- ✅ Saves to `exports/YYYY-MM-DD/` with timestamp

### From Image (OCR)
```bash
python -m av_lunchbox_stickerpdf.cli image order.png
```

### In Python Code
```python
from av_lunchbox_stickerpdf.cli import CLI

cli = CLI()
pdf_path = cli.generate_from_sheets("SPREADSHEET_ID")
print(f"Generated: {pdf_path}")
```

---

## 🎯 Core Features

| Feature | Status | Details |
|---------|--------|---------|
| **PDF Generation** | ✅ | Generate professional sticker PDFs |
| **Google Sheets** | ✅ | Auto-fetch order data |
| **OCR Extraction** | ✅ | Extract data from images |
| **Summary Reports** | ✅ | Auto-generate statistics |
| **Cross-platform** | ✅ | Mac, Linux, Windows support |
| **Configuration** | ✅ | Centralized settings |
| **Type Safety** | ✅ | 100% type hints |
| **Test Suite** | ✅ | 73 pytest tests |

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=av_lunchbox_stickerpdf --cov-report=term-missing

# Run a specific test file
pytest tests/test_markers.py -v
```

---

## 📋 Output Example

```
exports/2026-02-10/
├── 2026-02-10_11:15 AM.pdf        # Generated sticker PDF
└── 2026-02-10_11:15 AM.txt        # Summary report
```

**Summary Report Contents:**
```
TOTAL BOXES: 17

Boxes (count by type)
•	Veg Comfort Box + Pulav Rice: 9
•	Non-Veg Comfort Box + Pulav Rice: 4
•	Veg Comfort Box + White Rice: 0
•	Non-Veg Comfort Box + White Rice: 0
•	Veg Special Box + Pulav Rice: 2
•	Veg Special Box + White Rice: 0
•	Non-Veg Special Box + Pulav Rice: 2
•	Non-Veg Special Box + White Rice: 0

Addresses (total boxes per address)
•	2900 Plano Pkwy: 12 boxes
•	3400 W Plano Pkwy: 5 boxes
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| PDF conversion fails | Install LibreOffice: `brew install libreoffice` |
| Import errors | Ensure installed: `pip install -e .` |
| Google Sheet not found | Verify Spreadsheet ID is correct and public |
| No orders extracted | Check sheet has data for today's date |

See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) for more help.

---

## 📚 Learn More

| Need Help With | Read This |
|-----------------|-----------|
| **Getting Started** | [`docs/guides/GETTING_STARTED_NEW.md`](docs/guides/GETTING_STARTED_NEW.md) |
| **Architecture** | [`docs/guides/PROJECT_STRUCTURE.md`](docs/guides/PROJECT_STRUCTURE.md) |
| **Navigation** | [`docs/guides/DOCUMENTATION_INDEX.md`](docs/guides/DOCUMENTATION_INDEX.md) |
| **Quick Commands** | [`docs/guides/QUICK_COMMANDS.md`](docs/guides/QUICK_COMMANDS.md) |
| **API Reference** | [`docs/SHEETS_API_REFERENCE.md`](docs/SHEETS_API_REFERENCE.md) |
| **Troubleshooting** | [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) |

---

## 🤝 Contributing

Found a bug? Want a feature? 
- Review the code structure in `av_lunchbox_stickerpdf/`
- Check existing documentation
- Submit improvements

---

## 📄 License

Internal use only.

---

**Questions?** Check the [documentation index](docs/guides/DOCUMENTATION_INDEX.md) or review module docstrings in the package.
