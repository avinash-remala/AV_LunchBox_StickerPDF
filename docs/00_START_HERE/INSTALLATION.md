# 📋 Installation Guide

Step-by-step installation instructions for all platforms.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- macOS, Windows, or Linux

## Step 1: Clone/Navigate to Project

```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
```

## Step 2: Install Dependencies

```bash
# Install Python packages
pip install -r src/requirements.txt

# Install the package itself
pip install -e .
```

## Step 3: Verify Installation

```bash
# Test imports
python3 -c "from av_lunchbox_stickerpdf import CLI; print('✓ Installation successful!')"
```

## System-Specific Setup

### macOS 🍎

For PDF conversion, install LibreOffice:

```bash
brew install libreoffice
brew install tesseract  # For OCR
```

### Windows 🪟

Download and install:
1. [LibreOffice](https://www.libreoffice.org/download/)
2. [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

### Linux 🐧

```bash
sudo apt-get install libreoffice tesseract-ocr
```

## Troubleshooting Installation

### Issue: `ModuleNotFoundError: No module named 'docx'`

**Solution:**
```bash
pip install python-docx
```

### Issue: LibreOffice not found

**Solution:**
- macOS: `brew install libreoffice`
- Windows: Download from libreoffice.org
- Linux: `sudo apt-get install libreoffice`

### Issue: pytesseract errors

**Solution:**
```bash
pip install pytesseract
```

Plus install Tesseract (see System-Specific Setup above)

## Verify Everything Works

```bash
# Run a test
python -m av_lunchbox_stickerpdf.cli --help
```

You should see the help menu!

---

**Next:** Go to Quick Start Guide to run your first report!
