"""
Google Sheets data extraction module.
Provides utilities for fetching and parsing data from Google Sheets.
"""

import requests
import csv
from io import StringIO
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from ..core.models import Order
from ..config.logging_config import get_logger

log = get_logger("data.sheets_handler")


class GoogleSheetsClient:
    """Client for accessing public Google Sheets."""
    
    def __init__(self, timeout: int = 10):
        """Initialize the Google Sheets client."""
        self.timeout = timeout
    
    def fetch_csv_data(self, spreadsheet_id: str, sheet_id: int = 0) -> Tuple[List[Dict[str, str]], List[str]]:
        """
        Fetch data from a public Google Sheet using CSV export.
        
        Args:
            spreadsheet_id: The spreadsheet ID from the URL
            sheet_id: The gid parameter (sheet tab ID), default is 0 (first sheet)
        
        Returns:
            Tuple of (rows list, column names list)
        """
        csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
        
        try:
            log.info(f"Fetching Google Sheet data (gid={sheet_id})")
            response = requests.get(csv_url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse CSV
            csv_reader = csv.DictReader(StringIO(response.text))
            rows = list(csv_reader)
            
            log.info(f"Fetched {len(rows)} rows from Google Sheet")
            return rows, csv_reader.fieldnames
        
        except requests.exceptions.RequestException as e:
            log.error(f"Error fetching Google Sheet: {e}")
            return [], []


class OrderExtractor:
    """Extracts order data from sheet rows."""
    
    def __init__(self, column_mapping: Optional[Dict[str, str]] = None):
        """
        Initialize the order extractor.
        
        Args:
            column_mapping: Mapping of logical names to actual column names.
                           Example: {'name': 'Full Name', 'address': 'Address', ...}
        """
        self.column_mapping = column_mapping or {
            'name': 'Full Name',
            'address': 'Address',
            'box_type': 'Type of Food',
            'rice_type': 'Type of Rice'
        }
    
    def find_today_row(self, rows: List[Dict[str, str]], date_column: str = 'Date') -> Optional[Dict[str, str]]:
        """
        Find the row that matches today's date.
        
        Args:
            rows: List of dictionaries from the sheet
            date_column: The column name containing dates
        
        Returns:
            Dictionary of the matching row, or None
        """
        today = datetime.now()
        
        # Try both formats: with and without leading zero
        today_formats = [
            today.strftime("%m/%d/%Y"),  # 02/09/2026
            f"{today.month}/{today.day}/{today.year}"  # 2/9/2026
        ]
        
        for row in rows:
            if date_column in row and row[date_column].strip() in today_formats:
                log.debug(f"Found today's row: {row}")
                return row
        
        log.warning(f"No row found for today's date: {today_formats}")
        return None
    
    def extract_single_row(self, row: Dict[str, str], row_index: int = 0) -> Order:
        """
        Extract a single order from a row.
        
        Args:
            row: Dictionary from CSV (single row)
            row_index: Index of the row (for order_id)
        
        Returns:
            Order object
        """
        return Order(
            name=row.get(self.column_mapping['name'], '').strip(),
            address=row.get(self.column_mapping['address'], '').strip(),
            box_type=row.get(self.column_mapping['box_type'], '').strip(),
            rice_type=row.get(self.column_mapping['rice_type'], '').strip(),
            order_id=row_index,
        )
    
    def extract_orders_from_rows(self, rows: List[Dict[str, str]]) -> List[Order]:
        """
        Extract multiple orders from sheet rows.

        Args:
            rows: List of row dictionaries from CSV

        Returns:
            List of Order objects
        """
        orders = []
        for idx, row in enumerate(rows):
            order = self.extract_single_row(row, row_index=idx)
            if order.name and order.address:  # Only include non-empty orders
                orders.append(order)

        return orders
