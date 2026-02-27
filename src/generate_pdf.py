#!/usr/bin/env python3
"""
Update Word template with data extracted from image.
Replaces existing cell contents in the template table.

Usag                 # Pick the longest match (real names are longer than garbage like 'vy' or 'v')
            if all_name_matches:
                name = max(all_name_matches, key=len)
            else:
                name = ''
            
            # Remove leading single characters followed by space (residual garbage like "v Abhishek")
            if name and ' ' in name:
                parts = name.split()
                if len(parts[0]) == 1 and len(parts) > 1:
                    # Skip the single-letter garbage
                    name = ' '.join(parts[1:])Check if it's a box type
        box_match = box_pattern.search(line)
        if box_match:
            current_row['box_type'] = box_match.group(1)
            print(f"→ Found box type: {current_row['box_type']}")
            continueython update_template.py <input_image> <template_docx> <output_docx>

Example:
    python update_template.py input.png template.docx output.docx
"""

import sys
import re
from pathlib import Path
from datetime import datetime

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
    from docx.shared import Pt, RGBColor, Inches, Cm
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn, nsdecls
    from docx.enum.dml import MSO_THEME_COLOR
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
except ImportError:
    print("Installing python-docx...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "python-docx", "--break-system-packages"])
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor, Inches, Cm
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn, nsdecls
    from docx.enum.dml import MSO_THEME_COLOR
    from docx.opc.constants import RELATIONSHIP_TYPE as RT


def extract_table_data_from_image(image_path):
    """
    Extract table data from image using OCR and image analysis.
    Returns list of dictionaries with keys: name, address, box_type, rice_type
    
    Strategy: The image has two sections:
    1. Orders section (name + address) - appears first
    2. Box/Rice section (box types + rice types) - appears later
    
    We extract each section separately, then match by index/position.
    """
    print(f"Loading image: {image_path}")
    img = Image.open(image_path)
    
    # Perform OCR to get full text
    print("Performing OCR on image...")
    text = pytesseract.image_to_string(img)
    
    # Split into lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    print(f"OCR extracted {len(lines)} lines total")
    if lines:
        print("First 10 lines for debugging:")
        for i, line in enumerate(lines[:10]):
            print(f"  {i}: {line}")
    
    # Patterns
    phone_pattern = re.compile(r'\b\d{10}\b')
    address_pattern = re.compile(r'(2900 Plano Pkwy|3400 W Plano Pkwy)')
    box_pattern = re.compile(r'((?:Veg|Non-Veg)\s+Comfort Box|(?:\d+\s+)?(?:Comfort Box|Kabuli Chana Box|Moong Dal Box|Rajma Box))')
    rice_pattern = re.compile(r'(Pulav Rice|White Rice)')
    
    # FIRST PASS: Extract orders (name + address)
    orders = []
    for idx, line in enumerate(lines):
        # Skip header and junk
        if any(skip in line for skip in ['OAN', 'RWDN', 'ORDER NO', 'DELIVERY', 'PHONE']):
            continue
        
        # Skip lines with too many repeated characters
        if len(line) > 0:
            repeated_chars = sum(1 for i in range(len(line)-1) if line[i] == line[i+1])
            if repeated_chars > len(line) / 3:
                continue
        
        # Check if line contains address
        address_match = address_pattern.search(line)
        if address_match:
            address = address_match.group(1)
            line_remainder = line.replace(address, '').strip()
            
            # Extract phone number first
            phone_match = phone_pattern.search(line_remainder)
            if phone_match:
                line_remainder = line_remainder.replace(phone_match.group(), '').strip()
            
            # Extract NAME from what's left
            cleaned = line_remainder
            
            # Remove leading garbage
            while cleaned and not cleaned[0].isalpha():
                cleaned = cleaned[1:].strip()
            
            # Remove garbage characters
            garbage_patterns = ['»', '|', '¥', '«', '{', '}']
            for pattern in garbage_patterns:
                cleaned = cleaned.replace(pattern, ' ')
            
            cleaned = cleaned.lstrip('_- ~').rstrip('_- ~{')
            cleaned = ' '.join(cleaned.split())
            
            # Extract name sequences
            import re as regex_module
            all_name_matches = regex_module.findall(r'[A-Za-z]+(?:\s+[A-Za-z]+)*', cleaned)
            
            if all_name_matches:
                name = max(all_name_matches, key=len)
            else:
                name = ''
            
            # Clean up common OCR artifacts in names
            # Remove leading garbage patterns like "vy", "v", "a", etc. (single/double letter junk)
            if name:
                parts = name.split()
                # Remove leading single or double-letter garbage words
                while parts and len(parts[0]) <= 2 and parts[0].lower() in ['v', 'vy', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az']:
                    parts.pop(0)
                name = ' '.join(parts)
            
            # Handle concatenated names (like "SaiCharanKurella" -> "Sai Charan Kurella")
            # Split on capital letters if the name has no spaces and looks like multiple words
            if name and ' ' not in name and len(name) > 4:
                # Check if it looks like concatenated words (multiple capital letters)
                capital_positions = [i for i, c in enumerate(name) if c.isupper()]
                if len(capital_positions) >= 2:
                    # Split the name at capital letter positions
                    split_name = []
                    for i, pos in enumerate(capital_positions):
                        start = pos
                        end = capital_positions[i + 1] if i + 1 < len(capital_positions) else len(name)
                        split_name.append(name[start:end])
                    name = ' '.join(split_name)
            
            # Remove leading single letters followed by space (residual garbage)
            if name and ' ' in name:
                parts = name.split()
                if len(parts[0]) == 1 and len(parts) > 1:
                    name = ' '.join(parts[1:])
            
            # Only add if we have a real name
            if name and len(name) > 3:
                orders.append({'name': name, 'address': address})
    
    # SECOND PASS: Extract all box types and rice types (they appear later in the document)
    box_types = []
    rice_types = []
    for line in lines:
        box_match = box_pattern.search(line)
        if box_match:
            box_type = box_match.group(1)
            box_types.append(box_type)
        
        rice_match = rice_pattern.search(line)
        if rice_match:
            rice_type = rice_match.group(1)
            rice_types.append(rice_type)
    
    print(f"\nExtracted: {len(orders)} orders, {len(box_types)} box types, {len(rice_types)} rice types")
    
    # COMBINE: Match by index position
    # The assumption is that box_types[i] and rice_types[i] correspond to orders[i]
    num_rows = max(len(orders), len(box_types), len(rice_types))
    data_rows = []
    
    for i in range(num_rows):
        row_data = {
            'name': orders[i]['name'] if i < len(orders) else '',
            'address': orders[i]['address'] if i < len(orders) else '',
            'box_type': box_types[i] if i < len(box_types) else '',
            'rice_type': rice_types[i] if i < len(rice_types) else ''
        }
        data_rows.append(row_data)
        print(f"Row {i+1}: {row_data}")
    
    print(f"\nExtracted {len(data_rows)} complete rows from image")
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


def get_marker_for_box_rice(box_type, rice_type):
    """
    Determine the marker and font size increase based on box and rice type combinations.
    
    Returns: (marker_string, font_size_increase_pt)
    - Veg Comfort Box + Pulav Rice: --- VP --- + 2pt
    - Non-Veg Comfort Box + Pulav Rice: --- NVP --- + 2pt
    - Veg Comfort Box + White Rice: --- VW --- + 2pt
    - Non-Veg Comfort Box + White Rice: --- NVW --- + 2pt
    - Non-Veg Special Box: --- NVSP --- + 2pt
    - Veg Special Box: --- VSP --- + 2pt
    """
    # Check for Non-Veg FIRST to avoid matching "Veg" in "Non-Veg"
    is_non_veg = "Non-Veg" in box_type
    is_veg = "Veg" in box_type and not is_non_veg
    is_comfort_box = "Comfort Box" in box_type
    is_special_box = "Special Box" in box_type
    is_pulav = "Pulav Rice" in rice_type
    
    if is_special_box:
        if is_non_veg:
            return "--- NVSP ---", 2
        elif is_veg:
            return "--- VSP ---", 2
    
    if is_comfort_box:
        if is_veg and is_pulav:
            return "--- VP ---", 2
        elif is_non_veg and is_pulav:
            return "--- NVP ---", 2
        elif is_veg and not is_pulav:
            return "--- VW ---", 2
        elif is_non_veg and not is_pulav:
            return "--- NVW ---", 2
    
    return "", 0


def create_watermark_image(logo_path, opacity=0.20, cell_size=(200, 80), output_path=None):
    """
    Convert a logo to a grayscale watermark with specified opacity.
    
    Args:
        logo_path: Path to the original logo image
        opacity: Opacity level (0.0-1.0). Default 20%
        cell_size: Target (width, height) in pixels
        output_path: Where to save. If None, saves next to logo.
    
    Returns:
        Path to watermark image, or None on failure
    """
    try:
        if not Path(logo_path).exists():
            print(f"Logo not found: {logo_path}")
            return None

        print(f"Creating watermark from: {logo_path} (opacity={opacity*100:.0f}%)")

        img = Image.open(logo_path).convert("RGBA")
        grayscale = img.convert("L")

        # Build alpha: original alpha * opacity, ensuring visible pixels stay visible
        orig_alpha = img.split()[3]
        alpha = orig_alpha.point(lambda p: max(1, int(p * opacity)) if p > 10 else 0)

        gray_rgba = Image.merge("RGBA", (grayscale, grayscale, grayscale, alpha))

        gray_rgba.thumbnail(cell_size, Image.LANCZOS)

        # Save directly (no canvas — avoids compositing that destroys alpha)
        if output_path is None:
            output_path = str(Path(logo_path).parent / f"{Path(logo_path).stem}_watermark.png")

        gray_rgba.save(output_path, "PNG")
        print(f"✓ Watermark saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error creating watermark: {e}")
        return None


def get_watermark_path():
    """Get or create the watermark image. Returns path or None."""
    script_dir = Path(__file__).parent.parent
    watermark_path = script_dir / "assets" / "logo_watermark.png"
    logo_path = script_dir / "assets" / "logo.png"

    if watermark_path.exists():
        return str(watermark_path)
    if logo_path.exists():
        return create_watermark_image(str(logo_path), output_path=str(watermark_path))
    return None


def insert_watermark_into_cell(doc, cell, watermark_path):
    """
    Insert a watermark image into a cell as a behind-text anchored image.
    Sized and positioned to fit centred within the cell (6.47cm × 2.54cm).
    """
    from lxml import etree

    if not watermark_path or not Path(watermark_path).exists():
        return

    para = cell.paragraphs[0]
    part = para.part

    rel_id = part.relate_to(
        part.package.get_or_add_image_part(watermark_path),
        RT.IMAGE,
    )

    with Image.open(watermark_path) as img:
        img_width_px, img_height_px = img.size

    # Cell is ~6.47cm wide × 2.54cm tall.
    # Fit watermark to ~80% of cell height, then reduce by 20%.
    max_height = Cm(2.0 * 0.8)   # 20% smaller
    max_width  = Cm(5.0 * 0.8)   # 20% smaller

    aspect = img_width_px / img_height_px
    # Height-constrained sizing
    cy = int(max_height)
    cx = int(cy * aspect)
    # If too wide, constrain by width instead
    if cx > int(max_width):
        cx = int(max_width)
        cy = int(cx / aspect)

    # Left-aligned with 3px margin from left border
    # 3px ≈ 2.25pt ≈ 28575 EMU
    h_offset = 28575
    # Top-aligned with small margin (~3px) from top border
    v_offset = 28575

    unique_id = id(cell) & 0xFFFFFFFF
    anchor_xml = (
        f'<wp:anchor distT="0" distB="0" distL="0" distR="0" '
        f'simplePos="0" relativeHeight="0" behindDoc="1" locked="1" '
        f'layoutInCell="1" allowOverlap="0" '
        f'{nsdecls("wp", "a", "pic", "r")}>'
        f'  <wp:simplePos x="0" y="0"/>'
        f'  <wp:positionH relativeFrom="column">'
        f'    <wp:posOffset>{h_offset}</wp:posOffset>'
        f'  </wp:positionH>'
        f'  <wp:positionV relativeFrom="paragraph">'
        f'    <wp:posOffset>{v_offset}</wp:posOffset>'
        f'  </wp:positionV>'
        f'  <wp:extent cx="{cx}" cy="{cy}"/>'
        f'  <wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'  <wp:wrapNone/>'
        f'  <wp:docPr id="{unique_id}" name="Watermark {unique_id}"/>'
        f'  <wp:cNvGraphicFramePr>'
        f'    <a:graphicFrameLocks noChangeAspect="1"/>'
        f'  </wp:cNvGraphicFramePr>'
        f'  <a:graphic>'
        f'    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'      <pic:pic>'
        f'        <pic:nvPicPr>'
        f'          <pic:cNvPr id="{unique_id}" name="watermark.png"/>'
        f'          <pic:cNvPicPr/>'
        f'        </pic:nvPicPr>'
        f'        <pic:blipFill>'
        f'          <a:blip r:embed="{rel_id}"/>'
        f'          <a:stretch>'
        f'            <a:fillRect/>'
        f'          </a:stretch>'
        f'        </pic:blipFill>'
        f'        <pic:spPr>'
        f'          <a:xfrm>'
        f'            <a:off x="0" y="0"/>'
        f'            <a:ext cx="{cx}" cy="{cy}"/>'
        f'          </a:xfrm>'
        f'          <a:prstGeom prst="rect">'
        f'            <a:avLst/>'
        f'          </a:prstGeom>'
        f'        </pic:spPr>'
        f'      </pic:pic>'
        f'    </a:graphicData>'
        f'  </a:graphic>'
        f'</wp:anchor>'
    )

    anchor_element = etree.fromstring(anchor_xml)
    drawing = OxmlElement('w:drawing')
    drawing.append(anchor_element)

    if not para.runs:
        run_element = OxmlElement('w:r')
        para._element.append(run_element)
    else:
        run_element = para.runs[0]._element
    run_element.append(drawing)


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
    
    # Get watermark path (auto-creates from logo if needed)
    watermark_path = get_watermark_path()
    if watermark_path:
        print(f"✓ Watermark enabled: {watermark_path}")
    else:
        print("ℹ No watermark (place logo at assets/logo.png to enable)")
    
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
                    
                    # For the third line (box_type - rice_type), add markers with special formatting
                    if idx == 2:
                        # Clear the paragraph
                        para.clear()
                        
                        # Add the text
                        run = para.add_run(line)
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        
                        # Get marker based on box/rice combination
                        marker, font_size_increase = get_marker_for_box_rice(data['box_type'], data['rice_type'])
                        
                        # Get current font size (default to 11pt if not set)
                        current_font_size = run.font.size
                        if current_font_size is None:
                            current_font_size = Pt(11)
                        else:
                            # Convert to Pt if it's in twips (EMU)
                            if isinstance(current_font_size, int):
                                current_font_size = Pt(current_font_size / 100)
                        
                        # Add marker in a separate paragraph if applicable
                        if marker:
                            # Create a new paragraph for markers
                            marker_para = cell.add_paragraph()
                            marker_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            marker_run = marker_para.add_run(marker)
                            marker_run.bold = True
                            # Set marker font size to base + 2pt
                            marker_run.font.size = current_font_size + Pt(font_size_increase)
                            
                            print(f"  Line 3: Added marker '{marker}' in separate paragraph (bold, +{font_size_increase}pt) for {data['box_type']} - {data['rice_type']}")
                    elif idx == 0:
                        # Name line - make it bold
                        para.clear()
                        run = para.add_run(line)
                        run.bold = True
                        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        current_indent = para.paragraph_format.left_indent or Pt(0)
                        if col_idx == 2:
                            para.paragraph_format.left_indent = current_indent + Pt(2)
                        elif col_idx == 4:
                            para.paragraph_format.left_indent = current_indent + Pt(9)
                        # Insert watermark behind text on the first paragraph
                        if watermark_path:
                            insert_watermark_into_cell(doc, cell, watermark_path)
                    else:
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


def cleanup_exports_folder(exports_dir="exports", keep_current_date=True):
    """
    Clean up the exports folder by deleting all files and folders.
    
    Args:
        exports_dir: The directory to clean (default: exports)
        keep_current_date: If True, keep only today's folder (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        exports_path = Path(exports_dir)
        
        if not exports_path.exists():
            print(f"Exports folder doesn't exist yet: {exports_dir}")
            return True
        
        # Get list of items to delete
        items_to_delete = list(exports_path.iterdir())
        
        if not items_to_delete:
            print(f"Exports folder is already empty: {exports_dir}")
            return True
        
        print(f"\n{'='*60}")
        print(f"Cleaning up exports folder: {exports_dir}")
        print(f"{'='*60}")
        
        today = datetime.now().strftime("%Y-%m-%d")
        deleted_count = 0
        
        for item in items_to_delete:
            # Skip today's folder if keep_current_date is True
            if keep_current_date and item.is_dir() and item.name == today:
                print(f"✓ Keeping current date folder: {item.name}")
                continue
            
            try:
                if item.is_file():
                    item.unlink()
                    print(f"✓ Deleted file: {item.name}")
                    deleted_count += 1
                elif item.is_dir():
                    import shutil
                    shutil.rmtree(item)
                    print(f"✓ Deleted folder: {item.name}/")
                    deleted_count += 1
            except Exception as e:
                print(f"✗ Failed to delete {item.name}: {e}")
                return False
        
        print(f"\n✓ Cleanup complete! Deleted {deleted_count} item(s)")
        print(f"{'='*60}\n")
        return True
        
    except Exception as e:
        print(f"✗ Error during cleanup: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_template.py <template.docx> [--google-sheet <spreadsheet_id>] [--image <input_image>]")
        print("\nExamples:")
        print("  # Read from Google Sheet (today's date):")
        print("  python update_template.py template.docx --google-sheet 1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI")
        print("\n  # Read from image (OCR):")
        print("  python update_template.py template.docx --image input.png")
        print("\nThe PDF will be saved with today's date and time (e.g., 2026-02-09_03-45-PM.pdf)")
        sys.exit(1)
    
    template_path = sys.argv[1]
    
    # Parse arguments
    use_google_sheets = '--google-sheet' in sys.argv
    use_image = '--image' in sys.argv
    
    image_path = None
    spreadsheet_id = None
    
    if use_google_sheets:
        # Format: python script.py template.docx --google-sheet <id>
        try:
            sheet_idx = sys.argv.index('--google-sheet')
            spreadsheet_id = sys.argv[sheet_idx + 1]
        except (ValueError, IndexError):
            print("Error: --google-sheet requires a spreadsheet ID")
            sys.exit(1)
    elif use_image:
        # Format: python script.py template.docx --image input.png
        try:
            img_idx = sys.argv.index('--image')
            image_path = sys.argv[img_idx + 1]
        except (ValueError, IndexError):
            print("Error: --image requires an image path")
            sys.exit(1)
    else:
        # Legacy format: python script.py input.png template.docx (detect by file extension)
        if len(sys.argv) >= 3 and Path(sys.argv[1]).suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
            image_path = sys.argv[1]
            template_path = sys.argv[2]
        else:
            print("Error: Please provide either --google-sheet <id> or --image <path>")
            sys.exit(1)
    
    # Check if files exist
    if not Path(template_path).exists():
        print(f"Error: Template file not found: {template_path}")
        sys.exit(1)
    
    # Extract data based on source
    if spreadsheet_id:
        print(f"\nReading data from Google Sheet: {spreadsheet_id}")
        
        # Clean up exports folder before processing Google Sheets data
        cleanup_exports_folder("exports", keep_current_date=False)
        
        try:
            from google_sheets_handler import get_todays_lunch_orders
            data_rows = get_todays_lunch_orders(spreadsheet_id)
        except ImportError:
            print("Error: google_sheets_handler module not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading from Google Sheet: {e}")
            sys.exit(1)
    elif image_path:
        if not Path(image_path).exists():
            print(f"Error: Image file not found: {image_path}")
            sys.exit(1)
        print(f"\nExtracting data from image: {image_path}")
        data_rows = extract_table_data_from_image(image_path)
    else:
        print("Error: Please provide either --google-sheet <id> or --image <path>")
        sys.exit(1)
    
    if not data_rows:
        print("Warning: No data extracted!")
        sys.exit(1)
    
    # Generate output path with proper folder structure
    now = datetime.now()
    date_folder = now.strftime("%Y-%m-%d")
    date_time = now.strftime("%Y-%m-%d_%I:%M %p")
    
    # Determine output directory based on data source
    if spreadsheet_id:
        # For Google Sheets: save to exports/YYYY-MM-DD/
        output_dir = Path("exports") / date_folder
    else:
        # For image: save to exports/ (legacy behavior)
        output_dir = Path("exports")
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / f"{date_time}.pdf")
    
    print(f"Output will be saved to: {output_path}")
    
    # Cleanup exports folder (optional)
    cleanup_exports_folder("exports", keep_current_date=True)
    
    # Update template and convert to PDF
    update_template_with_data(template_path, output_path, data_rows)
    
    # Generate and save summary with the same timestamp and location
    try:
        from summary_generator import save_summary
        summary_filename = f"{date_time}.txt"
        summary_path = save_summary(data_rows, str(output_dir), summary_filename)
        if summary_path:
            print(f"✓ Summary generated successfully")
    except ImportError:
        print("Warning: summary_generator module not found - skipping summary generation")
    except Exception as e:
        print(f"Warning: Error generating summary: {e}")


if __name__ == "__main__":
    main()
