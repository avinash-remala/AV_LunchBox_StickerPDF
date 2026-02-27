# AV Lunch Box Sticker PDF Generator

Generate lunch box order PDFs and summaries from Google Sheets.

**Version: 2.0** | **Status: Production Ready**

---

## Quick Start

```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
python3 src/generate_pdf.py templates/AR_Template.docx --google-sheet SPREADSHEET_ID
```

**Example:**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

---

## What It Does

1. Fetches today's orders from the Google Sheet (public CSV export)
2. Generates a sticker PDF using the Word template
3. Saves a summary `.txt` report
4. Cleans up old export folders (keeps only today's)

All output goes to `exports/YYYY-MM-DD/` with a timestamp filename.

---

## Sticker Layout (per cell)

Each sticker contains the following lines in order:

| Line | Content | Style |
|------|---------|-------|
| 1 | Full Name | Bold, centered |
| 2 | Address | Centered |
| 3 | Type of Food - Type of Rice | Centered, 11pt |
| 4 | Comments *(only if present)* | Italic, 9pt, centered |
| 5 | Marker *(only if applicable)* | Bold, 13pt, centered |

---

## Markers

Markers are auto-generated based on the box and rice type:

| Box Type | Rice Type | Marker |
|----------|-----------|--------|
| Veg Comfort Box | Pulav Rice | `--- VP ---` |
| Non-Veg Comfort Box | Pulav Rice | `--- NVP ---` |
| Veg Comfort Box | White Rice | `--- VW ---` |
| Non-Veg Comfort Box | White Rice | `--- NVW ---` |
| Veg Special Box | any | `--- VSP ---` |
| Non-Veg Special Box | any | `--- NVSP ---` |

---

## Summary Report

The `.txt` summary includes:
- Total box count
- Count per box/rice combination (zero-count items are omitted)
- Total boxes per delivery address

**Example:**
```
TOTAL BOXES: 11

Boxes (count by type)
•   Non-Veg Comfort Box + Pulav Rice: 4
•   Non-Veg Special Box + NA: 3
•   Veg Special Box + NA: 2
•   Veg Special Box - Egg Biryani + NA: 2

Addresses (total boxes per address)
•   2900 Plano Pkwy: 6 boxes
•   3400 W Plano Pkwy: 5 boxes
```

---

## Google Sheet Format

The sheet must be publicly accessible and have these columns:

| Column | Description |
|--------|-------------|
| `Date` | Order date (M/D/YYYY format) |
| `Full Name` | Customer name |
| `Address` | Delivery address |
| `Type of Food` | Box type (e.g. Veg Comfort Box) |
| `Type of Rice` | Rice type (e.g. Pulav Rice) |
| `Comments` | Optional notes shown on sticker |

Rows with a blank `Date` cell are grouped under the last non-blank date above them.

---

## Project Structure

```
AV_LunchBox_StickerPDF/
├── src/
│   └── generate_pdf.py       # Main script — all logic lives here
├── templates/
│   └── AR_Template.docx      # Word template (3-column sticker layout)
├── exports/
│   └── YYYY-MM-DD/
│       ├── *.pdf             # Generated sticker PDF
│       └── *.txt             # Summary report
└── README.md
```

---

## Requirements

- Python 3.9+
- LibreOffice (for PDF conversion)
- Dependencies auto-installed on first run: `pillow`, `pytesseract`, `python-docx`, `requests`

**Install LibreOffice (macOS):**
```bash
brew install libreoffice
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| PDF conversion fails | Install LibreOffice: `brew install libreoffice` |
| No orders extracted | Check the sheet has rows for today's date |
| Google Sheet not found | Verify the Spreadsheet ID and that the sheet is public |

---

## What's New in V2.0

- Removed logo watermark from sticker cells
- Added Comments field to stickers (italic, smaller font, only shown when non-empty)
- Summary no longer shows zero-count box combinations
- Merged all `src/` scripts into a single `generate_pdf.py` — no extra files
- Removed all dead/deprecated code and helper scripts
- LibreOffice path resolution works reliably on macOS

---

*Internal use only.*
