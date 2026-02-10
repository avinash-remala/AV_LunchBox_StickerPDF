#!/usr/bin/env python3
"""
AR Template Updater - GUI Version for Mac
Uses file dialogs to select files instead of command line arguments
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import os

def select_files_and_run():
    """Open file dialogs and run the updater script"""
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Make dialogs appear on top
    root.attributes('-topmost', True)
    root.update()
    
    # Select image file
    print("Selecting image file...")
    image_file = filedialog.askopenfilename(
        title="Select Image File (spreadsheet screenshot)",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )
    
    if not image_file:
        print("No image file selected. Exiting.")
        return
    
    print(f"Selected image: {image_file}")
    
    # Use template from templates/AR_Template.docx
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_file = os.path.join(script_dir, "..", "templates", "AR_Template.docx")
    
    # Check if template exists
    if not os.path.exists(template_file):
        print("Selecting template file...")
        template_file = filedialog.askopenfilename(
            title="Select Word Template (AR_Template.docx)",
            filetypes=[
                ("Word documents", "*.docx"),
                ("All files", "*.*")
            ]
        )
        
        if not template_file:
            print("No template file selected. Exiting.")
            return
    
    print(f"Using template: {template_file}")
    
    # Select output location
    print("Selecting output location...")
    output_file = filedialog.asksaveasfilename(
        title="Save Updated Template As",
        defaultextension=".pdf",
        filetypes=[("PDF documents", "*.pdf")],
        initialfile="AR_Template_Updated.pdf"
    )
    
    if not output_file:
        print("No output file selected. Exiting.")
        return
    
    print(f"Output will be saved to: {output_file}")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "generate_pdf.py")
    
    # Check if main script exists
    if not os.path.exists(main_script):
        messagebox.showerror(
            "Error",
            f"Cannot find generate_pdf.py\n\nLooked in: {script_dir}\n\nPlease make sure both scripts are in the same folder."
        )
        return
    
    try:
        print("\nProcessing...")
        print("=" * 50)
        
        # Run the main script
        result = subprocess.run(
            [sys.executable, main_script, image_file, template_file, output_file],
            capture_output=True,
            text=True
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print("=" * 50)
            print("SUCCESS!")
            messagebox.showinfo(
                "Success",
                f"Template updated successfully!\n\nOutput saved to:\n{output_file}"
            )
        else:
            print("=" * 50)
            print("ERROR!")
            if result.stderr:
                print(result.stderr)
            messagebox.showerror(
                "Error",
                f"An error occurred:\n\n{result.stderr}"
            )
    
    except Exception as e:
        print("=" * 50)
        print(f"EXCEPTION: {str(e)}")
        messagebox.showerror(
            "Error",
            f"An unexpected error occurred:\n\n{str(e)}"
        )
    
    root.destroy()


def main():
    """Main entry point"""
    print("=" * 50)
    print("AR Template Updater - GUI Version")
    print("=" * 50)
    print()
    
    # Check if tkinter is available
    try:
        import tkinter
    except ImportError:
        print("ERROR: tkinter is not installed!")
        print("Please install tkinter:")
        print("  brew install python-tk")
        sys.exit(1)
    
    # Check required packages
    try:
        import PIL
        import pytesseract
        import docx
    except ImportError as e:
        print(f"ERROR: Missing required package: {e}")
        print("\nPlease install required packages:")
        print("  pip3 install pillow pytesseract python-docx")
        sys.exit(1)
    
    # Run the GUI
    select_files_and_run()


if __name__ == "__main__":
    main()
