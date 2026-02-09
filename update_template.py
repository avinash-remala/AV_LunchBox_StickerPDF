#!/usr/bin/env python3
"""
Update Word template with data extracted from image.
Replaces existing cell contents in the template table.

Usage:
    python update_template.py <input_image> <template_docx> <output_docx>

Example:
    python update_template.py input.png template.docx output.docx
"""

import sys
import re
from pathlib import Path

# OCR and image processing
try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "pillow", "pytesseract", "--break-system-packages"])
    from PIL import Image
    import pytesseract

# Word document handling
try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor, Inches
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.dml import MSO_THEME_COLOR
except ImportError:
    print("Installing python-docx...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "python-docx", "--break-system-packages"])
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor, Inches
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.dml import MSO_THEME_COLOR


def extract_table_data_from_image(image_path):
    """
    Extract table data from image using OCR and image analysis.
    Returns list of dictionaries with keys: name, address, box_type, rice_type
    """
    print(f"Loading image: {image_path}")
    img = Image.open(image_path)
    
    # Perform OCR to get full text
    print("Performing OCR on image...")
    text = pytesseract.image_to_string(img)
    
    # Also get detailed OCR data to detect row positions
    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    # Split into lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Extract separate lists for each column
    names = []
    phones = []
    box_types = []
    rice_types = []
    
    # Patterns
    phone_pattern = re.compile(r'\d{10}')
    
    for line in lines:
        # Skip header and junk
        if 'OAN' in line or 'RWDN' in line:
            continue
        
        # Skip lines with too many repeated characters or all caps gibberish
        if len(line) > 0:
            # Count repeated characters
            repeated_chars = sum(1 for i in range(len(line)-1) if line[i] == line[i+1])
            if repeated_chars > len(line) / 3:  # More than 1/3 repeated chars = likely garbage
                continue
        
        # Check if it's a phone number
        if phone_pattern.match(line):
            phones.append(line)
        
        # Check if it's a box type
        elif 'Comfort Box' in line:
            box_types.append(line)
        
        # Check if it's rice type
        elif 'Pulav Rice' in line or 'White Rice' in line or line == 'Rice':
            rice_types.append('Pulav Rice')
        
        # Otherwise, it might be a name (if it contains letters and is not too short)
        elif len(line) > 2 and any(c.isalpha() for c in line):
            # Skip if it's address-related or rice-related
            if 'Plano' in line or 'Pkwy' in line or line in ['wy', 'v', '~', 'W', '2900', '3400', 'Rice']:
                continue
            # Filter out numbers and short strings
            if not line.isdigit() and len(line) > 2:
                names.append(line)
    
    print(f"Found: {len(names)} names, {len(phones)} phones, {len(box_types)} box types, {len(rice_types)} rice types")
    
    # Detect addresses by analyzing row background colors
    # Yellow/Orange (RGB ~240,180,100) = 2900 Plano Pkwy
    # Blue (RGB ~180,220,240) = 3400 W Plano Pkwy
    addresses = []
    
    # Get image dimensions
    width, height = img.size
    
    # First, find the approximate y-positions of name texts
    name_positions = []
    for i, text in enumerate(ocr_data['text']):
        if text.strip() in names:
            y = ocr_data['top'][i]
            name_positions.append(y)
    
    # Remove duplicates and sort
    name_positions = sorted(list(set(name_positions)))
    
    # Now sample the background color for each position
    for y_pos in name_positions[:len(names)]:  # Match the number of names
        # Sample a few pixels from the left side of the row
        sample_x = 100  # Sample from the address column area
        
        # Make sure we're within bounds
        if 0 <= sample_x < width and 0 <= y_pos < height:
            # Sample a few pixels and average
            colors = []
            for offset in range(-5, 6, 2):
                try:
                    pixel = img.getpixel((sample_x, y_pos + offset))
                    if isinstance(pixel, tuple) and len(pixel) >= 3:
                        colors.append(pixel[:3])
                except:
                    pass
            
            if colors:
                # Average the colors
                avg_r = sum(c[0] for c in colors) / len(colors)
                avg_g = sum(c[1] for c in colors) / len(colors)
                avg_b = sum(c[2] for c in colors) / len(colors)
                
                # Determine address based on color
                # Blue backgrounds have higher blue values, lower red
                # Yellow/Orange backgrounds have higher red values
                if avg_b > avg_r and avg_b > 150:  # Bluish
                    addresses.append('3400 W Plano Pkwy')
                else:  # Yellowish/Orange
                    addresses.append('2900 Plano Pkwy')
            else:
                # Default if sampling failed
                addresses.append('2900 Plano Pkwy')
        else:
            addresses.append('2900 Plano Pkwy')
    
    # Ensure we have the right number of addresses
    while len(addresses) < len(names):
        addresses.append('2900 Plano Pkwy')
    addresses = addresses[:len(names)]
    
    print(f"Detected {len(addresses)} addresses based on row colors")
    
    # Combine into rows
    num_rows = max(len(names), len(phones), len(box_types), len(rice_types))
    
    data_rows = []
    for i in range(num_rows):
        row_data = {
            'name': names[i] if i < len(names) else '',
            'address': addresses[i] if i < len(addresses) else '',
            'box_type': box_types[i] if i < len(box_types) else '',
            'rice_type': rice_types[i] if i < len(rice_types) else ''
        }
        data_rows.append(row_data)
    
    print(f"Extracted {len(data_rows)} rows from image")
    return data_rows


def set_cell_margins(cell, left=None, right=None, top=None, bottom=None):
    """
    Set cell margins (padding) in twentieths of a point (twips).
    1 point = 20 twips
    """
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    
    margins = {
        'left': left,
        'right': right,
        'top': top,
        'bottom': bottom
    }
    
    for margin_name, value in margins.items():
        if value is not None:
            node = OxmlElement(f'w:{margin_name}')
            node.set(qn('w:w'), str(value))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
    
    tcPr.append(tcMar)


def convert_docx_to_pdf(docx_path, pdf_path):
    """
    Convert DOCX to PDF using available tools on Mac/Linux/Windows
    """
    import subprocess
    import platform
    import shutil
    
    system = platform.system()
    
    # Method 1: Try LibreOffice (works on Mac, Linux, Windows)
    libreoffice_paths = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',  # Mac
        'soffice',  # Linux/Windows (if in PATH)
        '/usr/bin/soffice',  # Linux
        'C:\\Program Files\\LibreOffice\\program\\soffice.exe',  # Windows
    ]
    
    for soffice_path in libreoffice_paths:
        if shutil.which(soffice_path) or Path(soffice_path).exists():
            try:
                print(f"Converting with LibreOffice: {soffice_path}")
                output_dir = str(Path(pdf_path).parent)
                
                # Run LibreOffice conversion
                result = subprocess.run([
                    soffice_path,
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', output_dir,
                    docx_path
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    # LibreOffice creates output.pdf in the output directory
                    # We need to rename it to our desired name
                    generated_pdf = str(Path(output_dir) / Path(docx_path).with_suffix('.pdf').name)
                    if Path(generated_pdf).exists() and generated_pdf != pdf_path:
                        import shutil
                        shutil.move(generated_pdf, pdf_path)
                    
                    if Path(pdf_path).exists():
                        print("PDF created successfully with LibreOffice")
                        return
                    
            except Exception as e:
                print(f"LibreOffice conversion failed: {e}")
                continue
    
    # Method 2: Try docx2pdf (Python package - works well on Windows)
    try:
        import docx2pdf
        print("Converting with docx2pdf...")
        docx2pdf.convert(docx_path, pdf_path)
        if Path(pdf_path).exists():
            print("PDF created successfully with docx2pdf")
            return
    except ImportError:
        print("docx2pdf not available (run: pip install docx2pdf)")
    except Exception as e:
        print(f"docx2pdf conversion failed: {e}")
    
    # Method 3: Try unoconv (Linux/Mac alternative)
    if shutil.which('unoconv'):
        try:
            print("Converting with unoconv...")
            subprocess.run([
                'unoconv',
                '-f', 'pdf',
                '-o', pdf_path,
                docx_path
            ], check=True)
            if Path(pdf_path).exists():
                print("PDF created successfully with unoconv")
                return
        except Exception as e:
            print(f"unoconv conversion failed: {e}")
    
    # If all methods fail, provide instructions
    print("\n" + "=" * 60)
    print("ERROR: Could not convert to PDF automatically")
    print("=" * 60)
    print("\nThe DOCX file was created successfully, but PDF conversion failed.")
    print("Please install one of the following:\n")
    
    if system == "Darwin":  # Mac
        print("Option 1 (Recommended): LibreOffice")
        print("  brew install libreoffice")
        print("\nOption 2: Use Preview")
        print("  Open the DOCX in Preview and export as PDF")
        print("\nOption 3: Use Pages")
        print("  Open the DOCX in Pages and export as PDF")
    elif system == "Linux":
        print("Option 1 (Recommended): LibreOffice")
        print("  sudo apt-get install libreoffice")
        print("\nOption 2: unoconv")
        print("  sudo apt-get install unoconv")
    elif system == "Windows":
        print("Option 1: docx2pdf")
        print("  pip install docx2pdf")
        print("\nOption 2: LibreOffice")
        print("  Download from: https://www.libreoffice.org/download/")
    
    print("\nThen run the script again.")
    print("=" * 60)
    
    # Keep the DOCX file for manual conversion
    final_docx = pdf_path.replace('.pdf', '.docx')
    if Path(docx_path).exists():
        import shutil
        shutil.copy(docx_path, final_docx)
        print(f"\nDOCX file saved as: {final_docx}")
        print("You can manually convert this to PDF.")


def update_template_with_data(template_path, output_path, data_rows):
    """
    Update the Word template by replacing cell contents with extracted data.
    Handles pagination by adding new rows/pages as needed.
    Then convert to PDF.
    """
    from docx import Document
    from docx.oxml import parse_xml
    from copy import deepcopy
    
    print(f"Loading template: {template_path}")
    doc = Document(template_path)
    table = doc.tables[0]
    data_columns = [0, 2, 4]
    offset_2px = Pt(2)
    data_index = 0
    
    # Get the number of available rows in the template
    initial_row_count = len(table.rows)
    print(f"Template has {initial_row_count} rows initially")
    
    # Calculate how many additional rows we need
    rows_needed = len(data_rows)
    if rows_needed > initial_row_count:
        additional_rows_needed = rows_needed - initial_row_count
        print(f"Need to add {additional_rows_needed} new rows for {len(data_rows)} data items")
        
        # Get a reference row to copy (usually the first data row)
        if initial_row_count > 0:
            reference_row = table.rows[0]
            tbl = table._element
            
            # Add new rows by copying the reference row
            for _ in range(additional_rows_needed):
                # Deep copy the reference row
                new_row = deepcopy(reference_row._element)
                tbl.append(new_row)
                print(f"Added new row (total now: {len(table.rows)})")
    
    # Now fill all rows with data
    for row_idx, row in enumerate(table.rows):
        for col_idx in data_columns:
            if data_index < len(data_rows):
                data = data_rows[data_index]
                
                # Change + to - in the display text
                cell_text = f"{data['name']}\n{data['address']}\n{data['box_type']} - {data['rice_type']}"
                
                cell = row.cells[col_idx]
                cell.text = ""  # Clear existing text
                
                # Add the three lines of text
                for idx, line in enumerate(cell_text.split('\n')):
                    if idx > 0:
                        cell.add_paragraph()
                    para = cell.paragraphs[idx]
                    para.text = line
                    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    current_indent = para.paragraph_format.left_indent or Pt(0)
                    if col_idx == 2:
                        para.paragraph_format.left_indent = current_indent + Pt(2)
                    elif col_idx == 4:
                        para.paragraph_format.left_indent = current_indent + Pt(9)
                
                if col_idx == 4:
                    set_cell_margins(cell, left=100)
                
                data_index += 1
            else:
                cell = row.cells[col_idx]
                cell.text = ""
    
    print(f"Updated {data_index} data cells from {len(data_rows)} rows")
    
    # Save as temporary DOCX first
    temp_docx = output_path.replace('.pdf', '_temp.docx')
    print(f"\nSaving temporary DOCX to: {temp_docx}")
    doc.save(temp_docx)
    # Convert to PDF
    print(f"Converting to PDF: {output_path}")
    convert_docx_to_pdf(temp_docx, output_path)
    # Remove temporary DOCX
    import os
    if os.path.exists(temp_docx):
        os.remove(temp_docx)
        print(f"Removed temporary file: {temp_docx}")
    print(f"Successfully updated {len(data_rows)} cells and saved as PDF!")


def main():
    if len(sys.argv) != 4:
        print("Usage: python update_template.py <input_image> <template.docx> <output.pdf>")
        print("\nExample:")
        print("  python update_template.py input.png template.docx output.pdf")
        sys.exit(1)
    
    image_path = sys.argv[1]
    template_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # Ensure output has .pdf extension
    if not output_path.lower().endswith('.pdf'):
        output_path = output_path.rsplit('.', 1)[0] + '.pdf'
        print(f"Output will be saved as: {output_path}")
    
    # Check if files exist
    if not Path(image_path).exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    if not Path(template_path).exists():
        print(f"Error: Template file not found: {template_path}")
        sys.exit(1)
    
    # Extract data from image
    data_rows = extract_table_data_from_image(image_path)
    
    if not data_rows:
        print("Warning: No data extracted from image!")
        sys.exit(1)
    
    # Update template and convert to PDF
    update_template_with_data(template_path, output_path, data_rows)


if __name__ == "__main__":
    main()
