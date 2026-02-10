# 🔧 Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### "ModuleNotFoundError: No module named 'docx'"

**Cause:** python-docx not installed

**Solution:**
```bash
pip install python-docx
```

### "No module named 'pytesseract'"

**Cause:** OCR library not installed

**Solution:**
```bash
pip install pytesseract
```

Plus install Tesseract system package:
- **macOS:** `brew install tesseract`
- **Windows:** Download from [here](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux:** `sudo apt-get install tesseract-ocr`

### "No module named 'requests'"

**Cause:** requests library not installed

**Solution:**
```bash
pip install requests
```

## PDF Generation Issues

### "LibreOffice not found"

**Cause:** LibreOffice not installed or not in PATH

**Solution:**
- **macOS:** `brew install libreoffice`
- **Windows:** Download from [libreoffice.org](https://www.libreoffice.org/download/)
- **Linux:** `sudo apt-get install libreoffice`

### "PDF conversion failed"

**Cause:** LibreOffice conversion error

**Solutions:**
1. Check LibreOffice is installed: `which soffice` or `which libreoffice`
2. Try manual conversion:
   ```bash
   libreoffice --headless --convert-to pdf file.docx
   ```
3. Check disk space
4. Check write permissions on export folder

### "DOCX file created but no PDF"

**Cause:** PDF conversion tool not available

**Solution:** See "LibreOffice not found" above

## Google Sheets Issues

### "Spreadsheet not found" or "404 error"

**Cause:** Invalid Spreadsheet ID or sheet is private

**Solutions:**
1. Verify Spreadsheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/[CORRECT_ID]/edit
   ```
2. Make sure sheet is public:
   - Click "Share" → "Change to anyone with link"
3. Verify internet connection

### "No data found in sheet"

**Cause:** Sheet doesn't have expected columns

**Solutions:**
1. Verify column names:
   - `Full Name`
   - `Address`
   - `Type of Food`
   - `Type of Rice`

2. Check that data is in the sheet (not empty)

3. Verify date column matches today (if filtering by date)

### "Connection timeout"

**Cause:** Network issue or Google Sheets unavailable

**Solutions:**
1. Check internet connection
2. Try again after a few seconds
3. Verify Google Sheets is accessible in browser
4. Check firewall/proxy settings

## Image Extraction Issues

### "No orders found in image"

**Cause:** Image doesn't contain recognizable order data

**Solutions:**
1. Ensure image is clear and readable
2. Verify image contains:
   - Customer names
   - Addresses (2900 Plano Pkwy or 3400 W Plano Pkwy)
   - Box types
   - Rice types
3. Try with a clearer image

### "Wrong name extraction"

**Cause:** OCR misread text

**Solutions:**
1. Use clearer image
2. Verify names in output summary
3. Manual correction if needed

### "Addresses not recognized"

**Cause:** Address not in expected format

**Solutions:**
1. Check image contains full address
2. Verify address format matches:
   - "2900 Plano Pkwy"
   - "3400 W Plano Pkwy"

## File and Directory Issues

### "Permission denied" when saving

**Cause:** No write permission on exports folder

**Solutions:**
```bash
# Check permissions
ls -ld exports/

# Fix permissions
chmod 755 exports/
```

### "No space left on device"

**Cause:** Disk full

**Solutions:**
1. Check disk space: `df -h`
2. Clean up old exports: Delete old folders in `exports/`
3. Free up disk space

### "File not found" errors

**Cause:** File path incorrect or file deleted

**Solutions:**
1. Verify file path
2. Check file exists
3. Use absolute paths

## Output File Issues

### "Summary file not created"

**Cause:** Report generation failed

**Solutions:**
1. Check write permissions on exports folder
2. Verify orders were extracted
3. Check disk space

### "PDF created but summary missing"

**Cause:** Summary generation skipped or failed

**Solutions:**
1. Check export folder for .txt file
2. Manually generate summary
3. Check logs for errors

### "Files have wrong timestamp"

**Cause:** System clock incorrect

**Solutions:**
1. Check system date/time: `date`
2. Set correct time: `timedatectl set-time "2026-02-10 14:30:00"`

## Performance Issues

### "PDF generation is slow"

**Cause:** Large document or system load

**Solutions:**
1. Reduce number of orders
2. Close other applications
3. Check system resources: `top` or Task Manager

### "Image extraction is slow"

**Cause:** OCR is computationally intensive

**Solutions:**
1. Use clearer, smaller image
2. Close other applications
3. This is normal for OCR

## Debugging

### Enable Verbose Output

```bash
# Run with debug info
python -m av_lunchbox_stickerpdf.cli sheets SPREADSHEET_ID --verbose
```

### Check Logs

Look for error messages in terminal output

### Manual Testing

```python
# Test individual components
from av_lunchbox_stickerpdf.data import GoogleSheetsClient

client = GoogleSheetsClient()
rows, cols = client.fetch_csv_data("spreadsheet-id")
print(f"Got {len(rows)} rows")
```

## Getting More Help

1. **Check documentation:** `01_USER_GUIDES/`
2. **Review API docs:** `03_API_REFERENCE/`
3. **Check Architecture:** `04_ARCHITECTURE/`
4. **Read error messages carefully** - they usually indicate the problem

## Still Having Issues?

1. Verify installation: `pip list | grep av-lunchbox`
2. Check Python version: `python --version` (needs 3.8+)
3. Test imports: `python -c "from av_lunchbox_stickerpdf import CLI"`
4. Review generated logs for detailed error information

---

**Most common solution:** Reinstall dependencies

```bash
pip install -r src/requirements.txt
pip install -e .
```

**Last Updated:** February 10, 2026  
**Version:** 2.0.0
