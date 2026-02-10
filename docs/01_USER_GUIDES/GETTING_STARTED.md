# 👤 Getting Started for Users

Complete guide for using the application.

## The Basics

### What You Can Do

✅ Generate PDF stickers from Google Sheets  
✅ Generate PDF stickers from images  
✅ Create summary reports  
✅ Organize output by date  

### What You Need

- The application installed (see Installation guide)
- Either a Google Sheets URL OR an image of orders

## Using Google Sheets

### Step 1: Prepare Your Sheet

Your Google Sheet should have columns:
- **Full Name** - Customer name
- **Address** - Delivery address
- **Type of Food** - Box type (e.g., "Veg Comfort Box")
- **Type of Rice** - Rice type (e.g., "Pulav Rice")

### Step 2: Make Sheet Public

1. Open your Google Sheet
2. Click "Share" → "Change to anyone with link"
3. Copy the Spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
   ```

### Step 3: Generate PDFs

```bash
python -m av_lunchbox_stickerpdf.cli sheets [YOUR_SPREADSHEET_ID]
```

Example:
```bash
python -m av_lunchbox_stickerpdf.cli sheets 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI
```

## Using Images

### Step 1: Prepare Your Image

Have an image with order information. The app will:
- Extract customer names
- Find addresses
- Identify box types
- Detect rice types

### Step 2: Generate PDFs

```bash
python -m av_lunchbox_stickerpdf.cli image path/to/your/image.png
```

## Finding Your Output

### Where Files Are Saved

```
exports/
└── 2026-02-10/
    ├── 2026-02-10_03:45 PM.pdf      ← Your PDF!
    └── 2026-02-10_03:45 PM.txt      ← Summary report
```

### What You Get

**PDF File:**
- Formatted sticker sheets
- Customer information
- Box and rice type details
- Ready to print!

**Summary File:**
- Total box count
- Breakdown by box type
- Breakdown by address
- Perfect for inventory!

## Common Tasks

### Task: Generate from Today's Sheet

```bash
python -m av_lunchbox_stickerpdf.cli sheets YOUR_SHEET_ID
```

### Task: Generate from a Photo

```bash
python -m av_lunchbox_stickerpdf.cli image photo.jpg
```

### Task: Find Last Generated PDF

```bash
ls -lh exports/*/
```

### Task: Clear Old Files

Old exports are automatically cleaned before Google Sheets runs.

## Tips & Tricks

💡 **Tip 1:** Keep your Google Sheet public for faster access  
💡 **Tip 2:** Use consistent naming in your sheet  
💡 **Tip 3:** Check summaries to verify order count  
💡 **Tip 4:** PDFs are ready to print directly  

## Troubleshooting

### "Spreadsheet not found"
- Verify the Spreadsheet ID is correct
- Make sure the sheet is public
- Check your internet connection

### "No orders found"
- Verify your sheet has the right column names
- Check that data is in the sheet
- Look for OCR errors if using images

### "PDF not created"
- Check that LibreOffice is installed
- Verify write permissions on the exports folder
- Check disk space

## Next Steps

- 📚 Read about Google Sheets setup: `06_REFERENCE/SHEETS_SETUP.md`
- 🔧 Troubleshoot issues: `05_TROUBLESHOOTING/`
- 👨‍💻 For developers: `02_DEVELOPER_GUIDES/`

---

**Ready to generate your first PDF?** Run the Quick Start! 🚀
