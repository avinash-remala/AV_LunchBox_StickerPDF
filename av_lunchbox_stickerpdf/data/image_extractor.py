"""
Image-based order data extraction module.
Uses OCR to extract order information from images.
"""

import re
from pathlib import Path
from typing import List, Dict, Any
import sys

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Installing required image processing packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "pillow", "pytesseract", "--break-system-packages"])
    from PIL import Image
    import pytesseract

from ..core.models import Order


class ImageOCRExtractor:
    """Extracts order data from images using OCR."""
    
    def __init__(self):
        """Initialize the image OCR extractor."""
        self.phone_pattern = re.compile(r'\b\d{10}\b')
        self.address_pattern = re.compile(r'(2900 Plano Pkwy|3400 W Plano Pkwy)')
        self.box_pattern = re.compile(
            r'((?:Veg|Non-Veg)\s+Comfort Box|'
            r'(?:\d+\s+)?(?:Comfort Box|Kabuli Chana Box|Moong Dal Box|Rajma Box))'
        )
        self.rice_pattern = re.compile(r'(Pulav Rice|White Rice)')
    
    def extract_from_image(self, image_path: str) -> List[Order]:
        """
        Extract order data from an image.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            List of Order objects extracted from the image
        """
        print(f"Loading image: {image_path}")
        img = Image.open(image_path)
        
        # Perform OCR
        print("Performing OCR on image...")
        text = pytesseract.image_to_string(img)
        
        # Extract orders from OCR text
        orders = self._parse_ocr_text(text)
        print(f"Extracted {len(orders)} orders from image")
        
        return orders
    
    def _parse_ocr_text(self, text: str) -> List[Order]:
        """
        Parse OCR text to extract orders.
        
        Args:
            text: OCR extracted text from image
        
        Returns:
            List of Order objects
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        print(f"OCR extracted {len(lines)} lines total")
        if lines:
            print("First 10 lines for debugging:")
            for i, line in enumerate(lines[:10]):
                print(f"  {i}: {line}")
        
        orders = []
        current_order = {}
        
        for line in lines:
            # Check for name (has phone number nearby)
            if self.phone_pattern.search(line):
                # This is likely a name line
                if current_order and 'name' in current_order:
                    # Save previous order
                    orders.append(self._create_order_from_dict(current_order))
                    current_order = {}
                
                # Extract name (remove phone number)
                name = self.phone_pattern.sub('', line).strip()
                current_order['name'] = name
            
            # Check for address
            address_match = self.address_pattern.search(line)
            if address_match:
                current_order['address'] = address_match.group(1)
            
            # Check for box type
            box_match = self.box_pattern.search(line)
            if box_match:
                current_order['box_type'] = box_match.group(1)
            
            # Check for rice type
            rice_match = self.rice_pattern.search(line)
            if rice_match:
                current_order['rice_type'] = rice_match.group(1)
        
        # Add the last order
        if current_order and 'name' in current_order:
            orders.append(self._create_order_from_dict(current_order))
        
        return orders
    
    def _create_order_from_dict(self, data: Dict[str, str]) -> Order:
        """
        Create an Order object from a dictionary.
        
        Args:
            data: Dictionary with order data
        
        Returns:
            Order object
        """
        return Order(
            name=data.get('name', '').strip(),
            address=data.get('address', '').strip(),
            box_type=data.get('box_type', '').strip(),
            rice_type=data.get('rice_type', '').strip(),
        )
