# Summary Generator Documentation

## Overview

The Summary Generator is a new feature that automatically creates a summary report of all lunch box orders after the PDF is generated. The summary provides:

- **Total box count** across all orders
- **Box type breakdown** (by food type + rice type combination)
- **Address distribution** (how many boxes per delivery address)

## Features

✓ **Automatic Generation** - Runs automatically when generating PDFs from Google Sheets  
✓ **Same Naming Convention** - Summary files use the same timestamp as the PDF  
✓ **Same Location** - Saved in the same `exports/YYYY-MM-DD/` folder as the PDF  
✓ **Clear Formatting** - Easy-to-read text format with bullet points  

## Summary Format

The summary file contains the following structure:

```
TOTAL BOXES: 17

Boxes (count by type)
•	Veg Comfort Box + Pulav Rice: 11
•	Non-Veg Comfort Box + Pulav Rice: 6
•	Veg Comfort Box + White Rice: 0
•	Non-Veg Comfort Box + White Rice: 0

Addresses (total boxes per address)
•	2900 Plano Pkwy: 12 boxes
•	3400 W Plano Pkwy: 5 boxes
```

## File Structure

The summary generator module is located at:
- `src/summary_generator.py`

## Usage

### Automatic (Recommended)

When you run the Google Sheets PDF generation:

```bash
python3 src/generate_pdf.py --google-sheet <SPREADSHEET_ID>
```

The summary is **automatically generated and saved** alongside the PDF with the same timestamp.

### Manual Usage

You can also generate a summary manually from Python code:

```python
from summary_generator import save_summary

# Your orders list
orders = [
    {'name': 'John Doe', 'address': '2900 Plano Pkwy', 'box_type': 'Veg Comfort Box', 'rice_type': 'Pulav Rice'},
    {'name': 'Jane Smith', 'address': '3400 W Plano Pkwy', 'box_type': 'Non-Veg Comfort Box', 'rice_type': 'Pulav Rice'},
]

# Generate and save
summary_path = save_summary(orders, output_dir="exports/2026-02-10")
```

## File Naming Convention

Summary files follow the same naming convention as PDFs:

**Format:** `YYYY-MM-DD_HH:MM AM/PM.txt`

**Example:**
- PDF: `exports/2026-02-10/2026-02-10_11:15 AM.pdf`
- Summary: `exports/2026-02-10/2026-02-10_11:15 AM.txt`

## Directory Structure

Summaries are saved in date-based folders:

```
exports/
├── 2026-02-10/
│   ├── 2026-02-10_11:11 AM.pdf
│   ├── 2026-02-10_11:11 AM.txt     ← Summary file
│   ├── 2026-02-10_11:15 AM.pdf
│   └── 2026-02-10_11:15 AM.txt     ← Summary file
└── 2026-02-11/
    ├── 2026-02-11_10:00 AM.pdf
    └── 2026-02-11_10:00 AM.txt
```

## Data Collected

The summary collects information from order data:

| Field | Description | Source |
|-------|-------------|--------|
| Total Count | Total number of boxes | Count of all orders |
| Box Types | Veg/Non-Veg combinations | `box_type` field |
| Rice Types | Pulav/White Rice | `rice_type` field |
| Addresses | Delivery addresses | `address` field |

## Implementation Details

### Core Functions

1. **`generate_summary(orders)`**
   - Takes a list of order dictionaries
   - Returns formatted summary string
   - Counts by type and address combinations

2. **`save_summary(orders, output_dir, filename)`**
   - Generates summary and saves to file
   - Creates directories if needed
   - Returns path to saved file

3. **`generate_and_save_summary(orders, output_dir)`**
   - Convenience function
   - Auto-generates timestamp filename
   - Saves with standard naming convention

### Integration Points

The summary generator integrates with:
- `generate_pdf.py` - Automatic summary generation after PDF creation
- `google_sheets_handler.py` - Uses order data from Google Sheets
- `sheets_extractor.py` - Compatible with flexible column mapping

## Example Output

When processing 17 lunch box orders:

```
TOTAL BOXES: 17

Boxes (count by type)
•	Veg Comfort Box + Pulav Rice: 11
•	Non-Veg Comfort Box + Pulav Rice: 6
•	Veg Comfort Box + White Rice: 0
•	Non-Veg Comfort Box + White Rice: 0

Addresses (total boxes per address)
•	2900 Plano Pkwy: 12 boxes
•	3400 W Plano Pkwy: 5 boxes
```

## Error Handling

The summary generation is designed to be non-blocking:

- If summary generation fails, the PDF is still created successfully
- Warnings are printed if the summary module is not found
- The main PDF generation process continues even if summary fails

## Troubleshooting

### Summary file not created?

1. Check if the export directory exists: `ls -la exports/YYYY-MM-DD/`
2. Verify file permissions: `chmod 755 exports/`
3. Check the terminal output for error messages

### Special characters in summary?

The summary uses Unicode bullet points (•) for better formatting. If these appear as `?`, your terminal may not support UTF-8. Try:

```bash
export LANG=en_US.UTF-8
python3 src/generate_pdf.py --google-sheet <ID>
```

## Future Enhancements

Possible improvements:
- CSV export option
- Email summary notification
- HTML formatted reports
- Customer-specific summaries
- Payment tracking in summary
- Nutritional information per order

