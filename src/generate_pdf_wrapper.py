#!/usr/bin/env python3
"""
Backward compatibility wrapper for generate_pdf.py
Routes to the new modular CLI system.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from av_lunchbox_stickerpdf.cli import CLI


def main():
    """Main entry point for backward compatibility."""
    
    parser = argparse.ArgumentParser(
        description="Generate lunch box order PDFs"
    )
    
    parser.add_argument("--image", help="Path to image file")
    parser.add_argument("--sheets", help="Google Sheets spreadsheet ID")
    parser.add_argument("--sheet-id", type=int, default=0, help="Sheet tab ID")
    
    args = parser.parse_args()
    
    cli = CLI()
    
    if args.image:
        result = cli.generate_from_image(args.image)
        return 0 if result else 1
    
    elif args.sheets:
        result = cli.generate_from_sheets(args.sheets, args.sheet_id)
        return 0 if result else 1
    
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
