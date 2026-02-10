# Google Sheets Integration Guide

## Overview

The `update_template.py` script now supports reading lunch order data directly from a Google Sheet. This eliminates the need to use OCR on images and allows for direct data input into the system.

## Setup

### Prerequisites

1. **Python 3.7+** (already configured in the workspace)
2. **Required packages** (automatically installed):
   - `requests` - for fetching Google Sheet data
   - `python-docx` - for Word document handling
   - `pillow` & `pytesseract` - for OCR (if using image input)

### Google Sheet Structure

Your Google Sheet should have the following columns:
- **Date** - The date in MM/DD/YYYY format (e.g., `2/9/2026`)
- **Full Name** - Customer's name
- **Address** - Delivery address
- **Type of Food** - Box type (e.g., "Veg Comfort Box", "Non-Veg Comfort Box")
- **Type of Rice** - Rice type (e.g., "Pulav Rice", "White Rice")

**Important:** The Google Sheet must be **public** or you must be authenticated. The script uses the public CSV export feature.

## Usage

### Method 1: Using Google Sheets (Recommended)

```bash
python update_template.py Templates/AR_Template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

**What it does:**
1. Fetches all data from the Google Sheet
2. Finds all rows matching today's date
3. Extracts names, addresses, box types, and rice types
4. Updates the Word template
5. Converts to PDF with timestamp

### Method 2: Using Image OCR (Legacy)

```bash
python update_template.py Templates/AR_Template.docx --image input.png
```

**What it does:**
1. Performs OCR on the image
2. Extracts customer data from the image
3. Updates the Word template
4. Converts to PDF

## Output

The script generates a PDF file with the naming format:
```
YYYY-MM-DD_HH:MM AM/PM.pdf
```

Example:
```
2026-02-09_09:50 PM.pdf
```

## Spreadsheet ID

The spreadsheet ID is the long string in the Google Sheets URL:

```
https://docs.google.com/spreadsheets/d/1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI/edit
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      This is the spreadsheet ID
```

## Testing

### Test Google Sheets Connection

```bash
python test_sheets.py
```

This will:
- Fetch data from the Google Sheet
- Display all orders for today
- Show any errors in the connection

### Debug Available Dates

```bash
python debug_dates.py
```

This will:
- Show all unique dates in the sheet
- Indicate whether today's date is present
- Show the closest available date

## Troubleshooting

### "No orders found for today"

**Possible causes:**
1. **Date format mismatch**: The sheet uses `MM/DD/YYYY` but your actual date is different
   - Run `python debug_dates.py` to see available dates
   
2. **Date not in sheet**: There are no entries for today
   - Add entries for today's date in the sheet
   
3. **Sheet is private**: The Google Sheet requires authentication
   - Share the sheet publicly or use image input instead

### "Google Sheet is not accessible"

1. Check that the spreadsheet ID is correct
2. Ensure the sheet is publicly accessible (Share > Anyone with the link)
3. Verify internet connection

### PDF conversion fails

If LibreOffice is not installed:

**Mac:**
```bash
brew install libreoffice
```

**Linux:**
```bash
sudo apt-get install libreoffice
```

**Windows:**
- Download from https://www.libreoffice.org/download/

## Advanced Features

### Custom Box/Rice Markers

The script automatically generates markers based on box and rice combinations:

| Box Type | Rice Type | Marker | Font Size |
|----------|-----------|--------|-----------|
| Veg Comfort Box | Pulav Rice | --- VP --- | +2pt |
| Non-Veg Comfort Box | Pulav Rice | --- NVP --- | +2pt |
| Veg Comfort Box | White Rice | --- VW --- | +2pt |
| Non-Veg Comfort Box | White Rice | --- NVW --- | +2pt |

These markers are automatically added to the PDF and formatted as bold text.

### Multiple Orders Per Day

If your sheet has multiple entries for the same date, the script will:
1. Extract all entries for today
2. Add additional rows to the template as needed
3. Fill all rows with the corresponding data

## File Structure

```
.
├── update_template.py          # Main script
├── sheets_handler.py           # Google Sheets integration
├── test_sheets.py              # Test script
├── debug_dates.py              # Debug script
└── Templates/
    └── AR_Template.docx        # Word template
```

## API Reference

### `sheets_handler.py`

#### `get_todays_lunch_orders(spreadsheet_id, sheet_id=0)`

Fetches all lunch orders for today from a Google Sheet.

**Parameters:**
- `spreadsheet_id` (str): The Google Sheet ID
- `sheet_id` (int): The sheet tab ID (default: 0 for first sheet)

**Returns:**
- `list`: List of order dictionaries with keys: `name`, `address`, `box_type`, `rice_type`

**Example:**
```python
from sheets_handler import get_todays_lunch_orders

orders = get_todays_lunch_orders("1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")
for order in orders:
    print(f"{order['name']}: {order['box_type']} - {order['rice_type']}")
```

## Notes

- The script uses Google's public CSV export API, so no API keys or OAuth are needed
- Data is fetched fresh every time the script runs
- The script handles multiple orders per day automatically
- Today's date matching is case-insensitive and handles both `2/9/2026` and `02/09/2026` formats
