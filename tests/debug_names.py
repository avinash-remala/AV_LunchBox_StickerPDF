#!/usr/bin/env python3
"""
Debug script to see exactly what's happening with name extraction
"""

import re
from PIL import Image
import pytesseract

image_path = "/Users/avinashremala/Desktop/Screenshot 2026-02-09 at 10.38.15.png"

print("Loading image and performing OCR...")
img = Image.open(image_path)
text = pytesseract.image_to_string(img)

lines = [line.strip() for line in text.split('\n') if line.strip()]

phone_pattern = re.compile(r'\b\d{10}\b')
address_pattern = re.compile(r'(2900 Plano Pkwy|3400 W Plano Pkwy)')

print("\n" + "="*80)
print("DEBUGGING NAME EXTRACTION FOR FIRST 10 ADDRESSES")
print("="*80 + "\n")

for idx, line in enumerate(lines):
    address_match = address_pattern.search(line)
    if address_match:
        address = address_match.group(1)
        
        # Get what's left after removing address
        remainder = line.replace(address, '').strip()
        
        # Remove phone
        phone_match = phone_pattern.search(remainder)
        if phone_match:
            remainder = remainder.replace(phone_match.group(), '').strip()
        
        print(f"Line {idx}: {line}")
        print(f"  Address: {address}")
        print(f"  After removing address: '{remainder}'")
        print(f"  Bytes: {remainder.encode('utf-8')}")
        
        # Try to extract name
        name_match = re.search(r'[A-Za-z]+(?:\s+[A-Za-z]+)*', remainder)
        if name_match:
            name = name_match.group(0)
            print(f"  Extracted name: '{name}'")
        else:
            print(f"  No name match found!")
        print()
