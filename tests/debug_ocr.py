#!/usr/bin/env python3
"""
Debug script to see all OCR output and identify box types
"""

import sys
from PIL import Image
import pytesseract

image_path = "/Users/avinashremala/Desktop/Screenshot 2026-02-09 at 10.25.51.png"

print("Loading image and performing OCR...")
img = Image.open(image_path)
text = pytesseract.image_to_string(img)

lines = [line.strip() for line in text.split('\n') if line.strip()]

print(f"\n{'='*70}")
print(f"ALL {len(lines)} LINES FROM OCR OUTPUT:")
print(f"{'='*70}\n")

for i, line in enumerate(lines):
    print(f"{i:2d}: {line}")

print(f"\n{'='*70}")
print("Looking for patterns:")
print(f"{'='*70}\n")

import re

# Look for any potential box type patterns
for i, line in enumerate(lines):
    if 'box' in line.lower() or 'comfort' in line.lower():
        print(f"Line {i}: {line}")
    # Look for quantity patterns (numbers followed by text)
    if re.match(r'^\d+\s*\w+', line):
        print(f"Line {i} (quantity pattern): {line}")
