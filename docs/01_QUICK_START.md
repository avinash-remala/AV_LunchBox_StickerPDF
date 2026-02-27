# Quick Start Guide - 5 Minutes to First PDF

Get up and running in just a few minutes!

## Prerequisites

- Python 3.8+
- LibreOffice (for PDF conversion)
- pip (Python package manager)

## Installation (2 minutes)

### 1. Install Python Dependencies
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
pip install -r src/requirements.txt
```

### 2. Install System Dependencies

**macOS:**
```bash
brew install libreoffice tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libreoffice tesseract-ocr
```

**Windows:**
- Download and install [LibreOffice](https://www.libreoffice.org/download/)
- Download and install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

## First Run (3 minutes)

### Option 1: From Google Sheets (Recommended)

```bash
python src/generate_pdf.py templates/AR_Template.docx \
  --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

### Option 2: From an Image

```bash
python src/generate_pdf.py templates/AR_Template.docx \
  --image path/to/your/image.png
```

## What Gets Generated?

✅ **PDF File**: `exports/2026-02-10/2026-02-10_03-45 PM.pdf`  
✅ **Summary File**: `exports/2026-02-10/2026-02-10_03-45 PM.txt`

## Next Steps

- 📖 Read [Installation Guide](02_INSTALLATION.md) for detailed setup
- 👤 Read [Usage Guide](04_USAGE_GUIDE.md) for all features
- 🔧 See [Troubleshooting](19_TROUBLESHOOTING.md) if you have issues

---

**Done!** You're ready to generate PDFs. For more advanced usage, see the full documentation.
