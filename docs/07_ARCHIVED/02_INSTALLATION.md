# Installation Guide

Comprehensive installation instructions for all platforms.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Installation](#python-installation)
3. [Project Setup](#project-setup)
4. [System Dependencies](#system-dependencies)
5. [Verification](#verification)

## System Requirements

### Minimum Requirements
- **OS**: macOS 10.14+, Ubuntu 18.04+, or Windows 10+
- **Python**: 3.8 or higher
- **Memory**: 2GB RAM minimum
- **Disk Space**: 500MB for installation

### Recommended Requirements
- **Python**: 3.10 or higher
- **Memory**: 4GB RAM
- **Disk Space**: 1GB

## Python Installation

### Check Your Python Version
```bash
python3 --version
```

Should show `Python 3.8.0` or higher.

### macOS
```bash
brew install python@3.11
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### Windows
Download from [python.org](https://www.python.org/downloads/)  
Run installer and check "Add Python to PATH"

## Project Setup

### 1. Clone or Download the Project
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
```

### 2. Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Install Python Dependencies
```bash
cd src
pip install -r requirements.txt
```

## System Dependencies

### macOS
```bash
# Using Homebrew
brew install libreoffice tesseract

# Verify installation
which soffice  # Should show LibreOffice path
which tesseract  # Should show Tesseract path
```

### Ubuntu/Debian
```bash
# Update package lists
sudo apt-get update

# Install LibreOffice
sudo apt-get install libreoffice

# Install Tesseract
sudo apt-get install tesseract-ocr tesseract-ocr-eng

# Verify
which soffice
which tesseract
```

### Windows
1. **LibreOffice**:
   - Download from [libreoffice.org](https://www.libreoffice.org/download/)
   - Run installer with default settings
   - Add to PATH: `C:\Program Files\LibreOffice\program`

2. **Tesseract**:
   - Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Run installer with default settings
   - Add to PATH: `C:\Program Files\Tesseract-OCR`

## Verification

Run the verification script:
```bash
cd src
python ../tests/test_installation.py
```

Or manually test each component:

### Test Python Packages
```bash
python3 -c "import docx; print('✓ python-docx installed')"
python3 -c "import PIL; print('✓ Pillow installed')"
python3 -c "import pytesseract; print('✓ pytesseract installed')"
python3 -c "import requests; print('✓ requests installed')"
```

### Test System Tools
```bash
# macOS/Linux
which soffice && echo "✓ LibreOffice found"
which tesseract && echo "✓ Tesseract found"

# Windows
where soffice  # or check Program Files
where tesseract
```

## Troubleshooting Installation

### LibreOffice Not Found
**macOS**: 
```bash
brew install libreoffice
```

**Ubuntu**:
```bash
sudo apt-get install libreoffice
```

**Windows**:
- Check installation in `C:\Program Files\LibreOffice`
- Add to system PATH if needed

### Tesseract Not Found
**macOS**:
```bash
brew install tesseract
```

**Ubuntu**:
```bash
sudo apt-get install tesseract-ocr
```

**Windows**:
- Install from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- Add `C:\Program Files\Tesseract-OCR` to PATH

### Python Packages Not Installing
```bash
# Upgrade pip
pip install --upgrade pip

# Install with specific version
pip install -r requirements.txt --force-reinstall

# If still issues, install individually:
pip install python-docx requests pillow pytesseract
```

## Next Steps

1. ✅ Verify everything works: `python ../tests/test_installation.py`
2. 📖 Read [Quick Start Guide](01_QUICK_START.md)
3. 👤 Read [Usage Guide](04_USAGE_GUIDE.md)

---

**Installation Complete!** Ready to generate your first PDF.
