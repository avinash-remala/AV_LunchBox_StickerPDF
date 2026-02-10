"""
File and directory utilities.
"""

import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime


def clean_directory(directory: str) -> bool:
    """
    Remove all files and subdirectories from a directory.
    
    Args:
        directory: Path to the directory to clean
    
    Returns:
        True if successful, False otherwise
    """
    try:
        dir_path = Path(directory)
        
        if not dir_path.exists():
            print(f"Directory does not exist: {directory}")
            return False
        
        # Remove all contents
        for item in dir_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
                print(f"  Removed directory: {item}")
            else:
                item.unlink()
                print(f"  Removed file: {item}")
        
        print(f"✓ Cleaned directory: {directory}")
        return True
    
    except Exception as e:
        print(f"✗ Error cleaning directory: {e}")
        return False


def create_dated_export_dir(base_dir: str, date_string: Optional[str] = None) -> Path:
    """
    Create a dated export directory.
    
    Args:
        base_dir: Base export directory path
        date_string: Date string (YYYY-MM-DD). If None, uses today's date.
    
    Returns:
        Path to the created directory
    """
    if date_string is None:
        date_string = datetime.now().strftime("%Y-%m-%d")
    
    export_dir = Path(base_dir) / date_string
    export_dir.mkdir(parents=True, exist_ok=True)
    
    return export_dir


def get_timestamp_filename(extension: str = ".pdf", format_12h: bool = True) -> str:
    """
    Generate a timestamp-based filename.
    
    Args:
        extension: File extension (e.g., ".pdf", ".txt")
        format_12h: Use 12-hour format with AM/PM (default), else 24-hour format
    
    Returns:
        Timestamp filename
    """
    now = datetime.now()
    
    if format_12h:
        # Format: YYYY-MM-DD_HH:MM AM/PM
        filename = now.strftime("%Y-%m-%d_%I:%M %p")
    else:
        # Format: YYYY-MM-DD_HH:MM:SS
        filename = now.strftime("%Y-%m-%d_%H:%M:%S")
    
    return filename + extension


def list_files_in_directory(directory: str, extension: Optional[str] = None) -> List[str]:
    """
    List all files in a directory.
    
    Args:
        directory: Path to the directory
        extension: Optional file extension filter (e.g., ".pdf")
    
    Returns:
        List of file paths
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return []
    
    if extension:
        files = sorted(dir_path.glob(f"*{extension}"))
    else:
        files = sorted(dir_path.glob("*"))
    
    return [str(f) for f in files if f.is_file()]
