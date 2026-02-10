"""
Command-line interface for the application.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from ..config import AppConfig
from ..data import GoogleSheetsClient, OrderExtractor, ImageOCRExtractor
from ..core import PDFGenerator
from ..report import SummaryGenerator, SummaryWriter
from ..utils import clean_directory, create_dated_export_dir, get_timestamp_filename


class CLI:
    """Command-line interface handler."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.config = AppConfig()
        self.config.ensure_directories()
    
    def generate_from_sheets(self, spreadsheet_id: str, sheet_id: int = 0, 
                           sheet_tab: str = "Name") -> Optional[str]:
        """
        Generate PDF and summary from Google Sheets.
        
        Args:
            spreadsheet_id: Google Sheets spreadsheet ID
            sheet_id: Sheet tab ID (gid parameter)
            sheet_tab: Column name for sheet tab filtering
        
        Returns:
            Path to generated PDF, or None if failed
        """
        
        print(f"Generating from Google Sheets: {spreadsheet_id}")
        
        # Clean exports directory if configured
        if self.config.EXPORT_CLEAN_ON_SHEETS_RUN:
            print("\nCleaning exports directory...")
            clean_directory(str(self.config.EXPORTS_DIR))
        
        # Fetch data
        client = GoogleSheetsClient()
        rows, columns = client.fetch_csv_data(spreadsheet_id, sheet_id)
        
        if not rows:
            print("✗ Failed to fetch data from Google Sheets")
            return None
        
        # Extract orders
        extractor = OrderExtractor()
        orders = extractor.extract_orders_from_rows(rows)
        
        if not orders:
            print("✗ No valid orders found in Google Sheets")
            return None
        
        print(f"✓ Extracted {len(orders)} orders from Google Sheets")
        
        # Create export directory
        export_dir = create_dated_export_dir(str(self.config.EXPORTS_DIR))
        
        # Generate PDF
        pdf_filename = get_timestamp_filename(".pdf")
        pdf_path = export_dir / pdf_filename
        
        pdf_generator = PDFGenerator(str(self.config.DEFAULT_TEMPLATE))
        success = pdf_generator.generate(orders, str(pdf_path))
        
        if not success:
            print("✗ Failed to generate PDF")
            return None
        
        # Generate summary
        summary_filename = pdf_filename.replace(".pdf", ".txt")
        summary_text = SummaryGenerator.generate(orders)
        summary_path = SummaryWriter.save_summary(summary_text, str(export_dir), summary_filename)
        
        print(f"\n✓ PDF generated: {pdf_path}")
        print(f"✓ Summary generated: {summary_path}")
        
        return str(pdf_path)
    
    def generate_from_image(self, image_path: str) -> Optional[str]:
        """
        Generate PDF and summary from an image.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Path to generated PDF, or None if failed
        """
        
        print(f"Generating from image: {image_path}")
        
        # Extract orders from image
        extractor = ImageOCRExtractor()
        orders = extractor.extract_from_image(image_path)
        
        if not orders:
            print("✗ No orders found in image")
            return None
        
        print(f"✓ Extracted {len(orders)} orders from image")
        
        # Create export directory
        export_dir = create_dated_export_dir(str(self.config.EXPORTS_DIR))
        
        # Generate PDF
        pdf_filename = get_timestamp_filename(".pdf")
        pdf_path = export_dir / pdf_filename
        
        pdf_generator = PDFGenerator(str(self.config.DEFAULT_TEMPLATE))
        success = pdf_generator.generate(orders, str(pdf_path))
        
        if not success:
            print("✗ Failed to generate PDF")
            return None
        
        # Generate summary
        summary_filename = pdf_filename.replace(".pdf", ".txt")
        summary_text = SummaryGenerator.generate(orders)
        summary_path = SummaryWriter.save_summary(summary_text, str(export_dir), summary_filename)
        
        print(f"\n✓ PDF generated: {pdf_path}")
        print(f"✓ Summary generated: {summary_path}")
        
        return str(pdf_path)


def main():
    """Main CLI entry point."""
    
    parser = argparse.ArgumentParser(
        description="Generate lunch box order PDFs from Google Sheets or images"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Google Sheets subcommand
    sheets_parser = subparsers.add_parser("sheets", help="Generate from Google Sheets")
    sheets_parser.add_argument("spreadsheet_id", help="Google Sheets spreadsheet ID")
    sheets_parser.add_argument("--sheet-id", type=int, default=0, help="Sheet tab ID (default: 0)")
    
    # Image subcommand
    image_parser = subparsers.add_parser("image", help="Generate from image")
    image_parser.add_argument("image_path", help="Path to the image file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = CLI()
    
    if args.command == "sheets":
        result = cli.generate_from_sheets(args.spreadsheet_id, args.sheet_id)
        return 0 if result else 1
    
    elif args.command == "image":
        result = cli.generate_from_image(args.image_path)
        return 0 if result else 1
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
