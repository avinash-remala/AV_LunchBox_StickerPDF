"""
PDF/Document generation module.
Generates Word documents and PDFs from order data.
"""

import sys
from pathlib import Path
from typing import List, Optional
from copy import deepcopy
import subprocess
import platform

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor, Inches
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.dml import MSO_THEME_COLOR
except ImportError:
    print("Installing python-docx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "python-docx", "--break-system-packages"])
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor, Inches
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.dml import MSO_THEME_COLOR

from ..core.models import Order


class PDFGenerator:
    """Generates PDF documents from order data."""
    
    def __init__(self, template_path: str):
        """
        Initialize the PDF generator.
        
        Args:
            template_path: Path to the Word template file
        """
        self.template_path = template_path
    
    def generate(self, orders: List[Order], output_path: str) -> bool:
        """
        Generate a PDF from orders.
        
        Args:
            orders: List of Order objects
            output_path: Path for the output PDF file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # First generate the DOCX
            docx_path = str(output_path).replace('.pdf', '.docx')
            self._generate_docx(orders, docx_path)
            
            # Then convert to PDF
            return self._convert_docx_to_pdf(docx_path, output_path)
        
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def _generate_docx(self, orders: List[Order], output_path: str) -> bool:
        """
        Generate a Word document from orders.
        
        Args:
            orders: List of Order objects
            output_path: Path for the output DOCX file
        
        Returns:
            True if successful, False otherwise
        """
        print(f"Loading template: {self.template_path}")
        doc = Document(self.template_path)
        table = doc.tables[0]
        data_columns = [0, 2, 4]
        
        # Convert orders to data rows
        data_rows = [
            {
                'name': order.name,
                'address': order.address,
                'box_type': order.box_type,
                'rice_type': order.rice_type,
            }
            for order in orders
        ]
        
        initial_row_count = len(table.rows)
        print(f"Template has {initial_row_count} rows initially")
        
        # Add rows if needed
        rows_needed = len(data_rows)
        if rows_needed > initial_row_count:
            additional_rows_needed = rows_needed - initial_row_count
            print(f"Need to add {additional_rows_needed} new rows for {len(data_rows)} data items")
            
            if initial_row_count > 0:
                reference_row = table.rows[0]
                tbl = table._element
                
                for _ in range(additional_rows_needed):
                    new_row = deepcopy(reference_row._element)
                    tbl.append(new_row)
        
        # Fill rows with data
        data_index = 0
        for row_idx, row in enumerate(table.rows):
            for col_idx in data_columns:
                if data_index < len(data_rows):
                    data = data_rows[data_index]
                    cell_text = f"{data['name']}\n{data['address']}\n{data['box_type']} - {data['rice_type']}"
                    
                    cell = row.cells[col_idx]
                    cell.text = ""
                    
                    for idx, line in enumerate(cell_text.split('\n')):
                        if idx > 0:
                            cell.add_paragraph()
                        para = cell.paragraphs[idx]
                        
                        if idx == 2:
                            para.clear()
                            run = para.add_run(line)
                            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            run.font.size = Pt(8)
                        else:
                            para.text = line
                            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    
                    data_index += 1
        
        # Save DOCX
        doc.save(output_path)
        print(f"DOCX file saved as: {output_path}")
        return True
    
    def _convert_docx_to_pdf(self, docx_path: str, pdf_path: str) -> bool:
        """
        Convert DOCX to PDF using available tools.
        
        Args:
            docx_path: Path to the DOCX file
            pdf_path: Path for the output PDF file
        
        Returns:
            True if successful, False otherwise
        """
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                # Try LibreOffice
                result = subprocess.run([
                    "libreoffice", "--headless", "--convert-to", "pdf",
                    "--outdir", str(Path(pdf_path).parent),
                    docx_path
                ], capture_output=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"PDF converted successfully to: {pdf_path}")
                    return True
            
            elif system == "Windows":
                # Try LibreOffice
                result = subprocess.run([
                    "soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", str(Path(pdf_path).parent),
                    docx_path
                ], capture_output=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"PDF converted successfully to: {pdf_path}")
                    return True
            
            elif system == "Linux":
                # Try LibreOffice
                result = subprocess.run([
                    "libreoffice", "--headless", "--convert-to", "pdf",
                    "--outdir", str(Path(pdf_path).parent),
                    docx_path
                ], capture_output=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"PDF converted successfully to: {pdf_path}")
                    return True
        
        except Exception as e:
            print(f"Error converting to PDF: {e}")
        
        # Fallback: just keep DOCX
        print(f"Could not convert to PDF. DOCX file available at: {docx_path}")
        return False
