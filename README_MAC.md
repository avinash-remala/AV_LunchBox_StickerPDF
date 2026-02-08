# AR Template Updater - Mac Version

Automatically extract data from spreadsheet images and update Word document templates, then convert to PDF on macOS.

## Quick Start

### Option 1: GUI Version (Easiest)
1. Double-click `update_template_gui.py`
2. Select your image file when prompted
3. Select your template file (AR_Template.docx)
4. Choose where to save the output PDF
5. Done!

### Option 2: Command Line
```bash
python3 update_template.py image.png AR_Template.docx output.pdf
```

### Option 3: Use the Shell Script
```bash
chmod +x run_updater.sh
./run_updater.sh
```

## Installation

### 1. Install Python 3
Python 3 usually comes pre-installed on Mac. Check your version:
```bash
python3 --version
```

If not installed:
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
# https://www.python.org/downloads/
```

### 2. Install LibreOffice (for PDF conversion)
```bash
# Using Homebrew (recommended)
brew install libreoffice

# Or download from: https://www.libreoffice.org/download/
```

### 3. Install Tesseract OCR
```bash
# Using Homebrew (recommended)
brew install tesseract

# Verify installation
tesseract --version
```

### 4. Install Python Packages
```bash
pip3 install pillow pytesseract python-docx
```

## Creating a Mac Application

### Quick Method (Recommended)
```bash
# Install PyInstaller
pip3 install pyinstaller

# Create GUI app
pyinstaller --onefile --windowed --name "AR Template Updater" update_template_gui.py

# Your app will be in: dist/AR Template Updater.app
```

### Detailed Instructions
See `HOW_TO_CREATE_MAC_APP.md` for:
- Creating .app bundles
- Creating DMG installers
- Code signing
- Automator workflows
- And more!

## Files Included

- **update_template.py** - Main script (command line)
- **update_template_gui.py** - GUI version with file pickers
- **run_updater.sh** - Shell script helper
- **HOW_TO_CREATE_MAC_APP.md** - Detailed app creation guide
- **README_MAC.md** - This file

## Features

- ✅ OCR text extraction from images
- ✅ Smart address detection based on row colors
- ✅ Preserves Word document formatting
- ✅ Center-aligned text with proper column offsets
- ✅ **Automatic PDF conversion**
- ✅ GUI file picker interface
- ✅ Command line interface
- ✅ Can be packaged as Mac app

## How It Works

1. **Image Analysis**: Uses Tesseract OCR to read text from the spreadsheet image
2. **Data Extraction**: Identifies names, addresses, phone numbers, box types, rice types
3. **Color Detection**: Analyzes background colors to determine addresses:
   - Yellow/Orange background = 2900 Plano Pkwy
   - Blue background = 3400 W Plano Pkwy
4. **Template Update**: Updates the Word template cells with extracted data
5. **Formatting**: Applies proper alignment and spacing
6. **PDF Conversion**: Automatically converts the updated document to PDF

## Usage Examples

### GUI Mode (Recommended for Mac)
```bash
python3 update_template_gui.py
# Then select files using the dialogs
# Output will be saved as PDF
```

### Command Line Mode
```bash
# Basic usage
python3 update_template.py input.png AR_Template.docx output.pdf

# With full paths
python3 update_template.py ~/Desktop/image.png ~/Documents/template.docx ~/Desktop/result.pdf
```

### From Finder
1. Make the GUI script executable:
   ```bash
   chmod +x update_template_gui.py
   ```
2. Right-click → Open With → Python Launcher
3. Or: Create a .app (see HOW_TO_CREATE_MAC_APP.md)

## Troubleshooting

### "Python not found" or wrong version
```bash
# Check version
python3 --version

# If needed, install via Homebrew
brew install python3
```

### "LibreOffice not found" - PDF conversion fails
```bash
# Install LibreOffice
brew install libreoffice

# Or download manually from:
# https://www.libreoffice.org/download/
```

Alternative: The script will save a .docx file if PDF conversion fails, which you can manually convert.

### "Tesseract not found"
```bash
# Install Tesseract
brew install tesseract

# Find installation path
which tesseract

# If still not found, the script will look in common locations
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x update_template.py
chmod +x update_template_gui.py
chmod +x run_updater.sh
```

### "Module not found" errors
```bash
# Install all required packages
pip3 install pillow pytesseract python-docx

# If pip3 not found
python3 -m pip install pillow pytesseract python-docx
```

### GUI doesn't show up
```bash
# Install tkinter (if needed)
brew install python-tk@3.11  # Adjust version as needed

# Or use the command line version instead
python3 update_template.py image.png template.docx output.pdf
```

### App created with PyInstaller won't open
```bash
# Remove quarantine attribute
xattr -cr "dist/AR Template Updater.app"

# Or right-click → Open (first time only)
```

### Poor OCR quality
- Use high-resolution images
- Ensure good contrast
- Make sure text is clearly visible
- Avoid blurry or distorted images

## Advanced Usage

### Batch Processing Multiple Images
Create a script:
```bash
#!/bin/bash
for image in *.png; do
    python3 update_template.py "$image" AR_Template.docx "output_${image%.png}.pdf"
done
```

### Integration with Automator
See `HOW_TO_CREATE_MAC_APP.md` for creating Automator workflows

### Custom Formatting
Edit `update_template.py` to adjust:
- Line 223-226: Column-specific indents
- Line 221: Cell margins
- Line 219: Alignment

## System Requirements

- macOS 10.12 or later
- Python 3.7 or higher
- LibreOffice (for PDF conversion)
- Tesseract OCR
- 100 MB free disk space
- PDF reader (Preview, Adobe Reader, etc.)

## License

This script is provided as-is for use with AR Template updates.

## Quick Start

### Option 1: GUI Version (Easiest)
1. Double-click `update_template_gui.py`
2. Select your image file when prompted
3. Select your template file (AR_Template.docx)
4. Choose where to save the output
5. Done!

### Option 2: Command Line
```bash
python3 update_template.py image.png AR_Template.docx output.docx
```

### Option 3: Use the Shell Script
```bash
chmod +x run_updater.sh
./run_updater.sh
```

## Installation

### 1. Install Python 3
Python 3 usually comes pre-installed on Mac. Check your version:
```bash
python3 --version
```

If not installed:
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
# https://www.python.org/downloads/
```

### 2. Install Tesseract OCR
```bash
# Using Homebrew (recommended)
brew install tesseract

# Verify installation
tesseract --version
```

### 3. Install Python Packages
```bash
pip3 install pillow pytesseract python-docx
```

## Creating a Mac Application

### Quick Method (Recommended)
```bash
# Install PyInstaller
pip3 install pyinstaller

# Create GUI app
pyinstaller --onefile --windowed --name "AR Template Updater" update_template_gui.py

# Your app will be in: dist/AR Template Updater.app
```

### Detailed Instructions
See `HOW_TO_CREATE_MAC_APP.md` for:
- Creating .app bundles
- Creating DMG installers
- Code signing
- Automator workflows
- And more!

## Files Included

- **update_template.py** - Main script (command line)
- **update_template_gui.py** - GUI version with file pickers
- **run_updater.sh** - Shell script helper
- **HOW_TO_CREATE_MAC_APP.md** - Detailed app creation guide
- **README_MAC.md** - This file

## Features

- ✅ OCR text extraction from images
- ✅ Smart address detection based on row colors
- ✅ Preserves Word document formatting
- ✅ Center-aligned text with proper column offsets
- ✅ GUI file picker interface
- ✅ Command line interface
- ✅ Can be packaged as Mac app

## How It Works

1. **Image Analysis**: Uses Tesseract OCR to read text from the spreadsheet image
2. **Data Extraction**: Identifies names, addresses, phone numbers, box types, rice types
3. **Color Detection**: Analyzes background colors to determine addresses:
   - Yellow/Orange background = 2900 Plano Pkwy
   - Blue background = 3400 W Plano Pkwy
4. **Template Update**: Updates the Word template cells with extracted data
5. **Formatting**: Applies proper alignment and spacing

## Usage Examples

### GUI Mode (Recommended for Mac)
```bash
python3 update_template_gui.py
# Then select files using the dialogs
```

### Command Line Mode
```bash
# Basic usage
python3 update_template.py input.png AR_Template.docx output.docx

# With full paths
python3 update_template.py ~/Desktop/image.png ~/Documents/template.docx ~/Desktop/result.docx
```

### From Finder
1. Make the GUI script executable:
   ```bash
   chmod +x update_template_gui.py
   ```
2. Right-click → Open With → Python Launcher
3. Or: Create a .app (see HOW_TO_CREATE_MAC_APP.md)

## Troubleshooting

### "Python not found" or wrong version
```bash
# Check version
python3 --version

# If needed, install via Homebrew
brew install python3
```

### "Tesseract not found"
```bash
# Install Tesseract
brew install tesseract

# Find installation path
which tesseract

# If still not found, the script will look in common locations
```

### "Permission denied"
```bash
# Make scripts executable
chmod +x update_template.py
chmod +x update_template_gui.py
chmod +x run_updater.sh
```

### "Module not found" errors
```bash
# Install all required packages
pip3 install pillow pytesseract python-docx

# If pip3 not found
python3 -m pip install pillow pytesseract python-docx
```

### GUI doesn't show up
```bash
# Install tkinter (if needed)
brew install python-tk@3.11  # Adjust version as needed

# Or use the command line version instead
python3 update_template.py image.png template.docx output.docx
```

### App created with PyInstaller won't open
```bash
# Remove quarantine attribute
xattr -cr "dist/AR Template Updater.app"

# Or right-click → Open (first time only)
```

### Poor OCR quality
- Use high-resolution images
- Ensure good contrast
- Make sure text is clearly visible
- Avoid blurry or distorted images

## Advanced Usage

### Batch Processing Multiple Images
Create a script:
```bash
#!/bin/bash
for image in *.png; do
    python3 update_template.py "$image" AR_Template.docx "output_${image%.png}.docx"
done
```

### Integration with Automator
See `HOW_TO_CREATE_MAC_APP.md` for creating Automator workflows

### Custom Formatting
Edit `update_template.py` to adjust:
- Line 223-226: Column-specific indents
- Line 221: Cell margins
- Line 219: Alignment

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `HOW_TO_CREATE_MAC_APP.md` for app creation issues
3. Ensure all dependencies are properly installed
4. Test with the command line version first

## System Requirements

- macOS 10.12 or later
- Python 3.7 or higher
- Tesseract OCR
- 50 MB free disk space
- Word-compatible application (for viewing output)

## License

This script is provided as-is for use with AR Template updates.
