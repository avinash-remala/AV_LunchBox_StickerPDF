# AV Lunch Box Sticker PDF Generator

Generate lunch box order PDFs and summaries from Google Sheets.

**Version: 2.0** | **Status: Production Ready**

---

## Quick Start

**From Google Sheets (primary):**
```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
python3 src/generate_pdf.py templates/AR_Template.docx --google-sheet SPREADSHEET_ID
```

**From an image (OCR):**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx --image path/to/orders.png
```

**Example:**
```bash
python3 src/generate_pdf.py templates/AR_Template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

---

## What It Does

**Google Sheets mode (`--google-sheet`):**
1. Fetches today's orders from the Google Sheet (public CSV export)
2. Generates a sticker PDF using the Word template
3. Saves a summary `.txt` report
4. Cleans up old export folders (keeps only today's)

**Image mode (`--image`):**
1. Extracts order data from an image using OCR (tesseract)
2. Generates a sticker PDF and summary from the extracted data

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
TOTAL BOXES: 14

Boxes (count by type)
•   Veg Comfort Box + Pulav Rice: 5
•   Non-Veg Comfort Box + Pulav Rice: 4
•   Non-Veg Comfort Box + White Rice: 2
•   Veg Special Box + Pulav Rice: 2
•   Non-Veg Special Box + Pulav Rice: 1

Addresses (total boxes per address)
•   2900 Plano Pkwy: 8 boxes
•   3400 W Plano Pkwy: 6 boxes
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

## GitHub Actions — Automated Email Delivery

Two workflows run automatically (triggered by cron-job.org) Mon–Fri and send results via Zoho Mail.

### Workflows

| Workflow file | What gets sent |
|---------------|----------------|
| `lunch-summary.yml` | Summary text only |
| `lunch-pdf.yml` | Summary text + PDF attachment |

### Manual Trigger

Go to **Actions → Lunch Summary** or **Lunch Summary + PDF → Run workflow**.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `SPREADSHEET_ID` | Google Sheets spreadsheet ID |
| `EMAIL_USERNAME` | Zoho Mail address to send from |
| `EMAIL_PASSWORD` | Zoho Mail password (or app-specific password if 2FA is enabled) |
| `EMAIL_TO` | Recipient email addresses, comma-separated |

### How it works

1. Fetches today's orders from Google Sheets
2. Generates the sticker PDF and summary
3. Sends the summary via Zoho Mail (+ PDF as email attachment in `lunch-pdf.yml`)

---

## Project Structure

```
AV_LunchBox_StickerPDF/
├── .github/
│   └── workflows/
│       ├── lunch-summary.yml  # GitHub Actions — sends summary email only
│       └── lunch-pdf.yml      # GitHub Actions — sends summary + PDF email
│
├── src/
│   ├── generate_pdf.py        # Main script — all logic lives here
│   ├── send_lunch_email.py    # Sends summary/PDF via Zoho Mail
│   ├── requirements.txt       # Python dependencies
│   └── setup.sh               # Setup helper
│
├── templates/
│   └── AR_Template.docx      # Word template (3-column sticker layout)
│
├── assets/
│   └── logo.png              # Brand logo (not used in stickers)
│
├── exports/                  # Auto-created on first run
│   └── YYYY-MM-DD/
│       ├── *.pdf             # Generated sticker PDF
│       └── *.txt             # Summary report
│
├── av_lunchbox_stickerpdf/   # Python package (legacy, not used by run command)
│   ├── core/
│   ├── data/
│   ├── report/
│   ├── cli/
│   ├── config/
│   └── utils/
│
├── tests/                    # Test suite (pytest)
├── docs/                     # Project documentation
├── pyproject.toml
└── README.md
```

---

## Requirements

- Python 3.9+
- LibreOffice (for DOCX → PDF conversion)
- tesseract (only needed for `--image` mode)

**Install Python dependencies:**
```bash
pip install -r src/requirements.txt
```

**Install system dependencies (macOS):**
```bash
brew install libreoffice tesseract
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| PDF conversion fails | Install LibreOffice: `brew install libreoffice` |
| No orders extracted | Check the sheet has rows for today's date |
| Google Sheet not found | Verify the Spreadsheet ID and that the sheet is public |
| OCR gives bad results | Install tesseract: `brew install tesseract` |
| Import error on run | Run `pip install -r src/requirements.txt` |

---

## What's New in V2.0

- Removed logo watermark from sticker cells
- Added Comments field to stickers (italic, smaller font, only shown when non-empty)
- Summary no longer shows zero-count box combinations
- Merged all `src/` scripts into a single `generate_pdf.py` — no extra files
- Removed all dead/deprecated code and helper scripts
- LibreOffice path resolution works reliably on macOS
- GitHub Actions workflow with automated email delivery via Zoho Mail
- Split into two independent workflows: summary-only and summary + PDF
- All times use CST/CDT — GitHub runner UTC is corrected automatically

---

*Internal use only.*
