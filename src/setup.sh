#!/bin/bash
# Quick start script for Google Sheets integration

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Lunch Box PDF Generator - Google Sheets Integration      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Path to the Python venv
PYTHON_CMD="/Users/avinashremala/Desktop/PDF Creation From Image - Lunch Boxes/.venv/bin/python"
WORKSPACE_DIR="/Users/avinashremala/Desktop/PDF Creation From Image - Lunch Boxes"
TEMPLATE_PATH="$WORKSPACE_DIR/Templates/AR_Template.docx"
SPREADSHEET_ID="1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"

# Check if running with argument
if [ "$1" == "test" ]; then
    echo "Testing Google Sheets connection..."
    echo ""
    cd "$WORKSPACE_DIR"
    "$PYTHON_CMD" test_sheets.py
    
elif [ "$1" == "dates" ]; then
    echo "Checking available dates in Google Sheet..."
    echo ""
    cd "$WORKSPACE_DIR"
    "$PYTHON_CMD" debug_dates.py
    
elif [ "$1" == "image" ]; then
    if [ -z "$2" ]; then
        echo "Usage: ./quickstart.sh image <image_path>"
        echo ""
        echo "Example:"
        echo "  ./quickstart.sh image input.png"
        exit 1
    fi
    echo "Generating PDF from image OCR..."
    echo ""
    cd "$WORKSPACE_DIR"
    "$PYTHON_CMD" update_template.py "$TEMPLATE_PATH" --image "$2"
    
else
    echo "Generating PDF from today's Google Sheet data..."
    echo ""
    echo "📊 Spreadsheet: ATT Corporate Lunch box"
    echo "📅 Date: $(date '+%Y-%m-%d')"
    echo "📄 Template: $TEMPLATE_PATH"
    echo ""
    
    cd "$WORKSPACE_DIR"
    "$PYTHON_CMD" update_template.py "$TEMPLATE_PATH" --google-sheet "$SPREADSHEET_ID"
    
    echo ""
    echo "✓ Done! PDF generated in the workspace directory."
    echo ""
    echo "Options:"
    echo "  ./quickstart.sh test       - Test Google Sheets connection"
    echo "  ./quickstart.sh dates      - Check available dates"
    echo "  ./quickstart.sh image FILE - Generate from image instead"
fi
