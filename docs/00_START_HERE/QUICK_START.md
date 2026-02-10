# 🚀 Quick Start Guide

Welcome! This guide will get you started in 5 minutes.

## What is This?

AV Lunch Box Sticker PDF Generator is a tool that:
- 📊 Reads lunch box orders from Google Sheets
- 🖼️ Generates formatted PDF stickers
- 📈 Creates summary reports
- ⚡ Automates order processing

## Installation (2 minutes)

```bash
cd /Users/avinashremala/Desktop/AV_LunchBox_StickerPDF
pip install -e .
```

## Your First Run (3 minutes)

### Option 1: From Google Sheets

```bash
python -m av_lunchbox_stickerpdf.cli sheets YOUR_SPREADSHEET_ID
```

### Option 2: From an Image

```bash
python -m av_lunchbox_stickerpdf.cli image path/to/image.png
```

## Where to Find Results

- **PDFs:** `exports/YYYY-MM-DD/`
- **Summaries:** `exports/YYYY-MM-DD/`

## Next Steps

- 📖 Read `01_USER_GUIDES/GETTING_STARTED.md` for detailed steps
- 🔧 Check `05_TROUBLESHOOTING/` if you have issues
- 📚 Browse other guides for more features

## Need Help?

- **Quick Answer:** Check `05_TROUBLESHOOTING/`
- **How-to:** Read `01_USER_GUIDES/`
- **Deep Dive:** Check `02_DEVELOPER_GUIDES/`

---

**Estimated time to first PDF:** 5 minutes ⚡
