"""
Configuration management for the application.
Handles paths, settings, and environment variables.
"""

from pathlib import Path
from typing import Optional
import os


class AppConfig:
    """Application configuration settings."""
    
    # Project root
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    # Directories
    SRC_DIR = PROJECT_ROOT / "src"
    TEMPLATES_DIR = PROJECT_ROOT / "templates"
    EXPORTS_DIR = PROJECT_ROOT / "exports"
    TESTS_DIR = PROJECT_ROOT / "tests"
    DOCS_DIR = PROJECT_ROOT / "docs"
    
    # Files
    DEFAULT_TEMPLATE = TEMPLATES_DIR / "AR_Template.docx"
    REQUIREMENTS_FILE = SRC_DIR / "requirements.txt"
    
    # Google Sheets settings
    GOOGLE_SHEETS_TIMEOUT = 10
    
    # Export settings
    EXPORT_CLEAN_ON_SHEETS_RUN = True
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        for directory in [cls.EXPORTS_DIR, cls.TEMPLATES_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_template_path(cls, template_name: Optional[str] = None) -> Path:
        """
        Get the path to a template file.
        
        Args:
            template_name: Name of the template. If None, uses default.
        
        Returns:
            Path to the template file
        """
        if template_name is None:
            return cls.DEFAULT_TEMPLATE
        
        return cls.TEMPLATES_DIR / template_name
    
    @classmethod
    def get_export_dir(cls, date_string: Optional[str] = None) -> Path:
        """
        Get the export directory for a specific date.
        
        Args:
            date_string: Date string (YYYY-MM-DD). If None, uses today's date.
        
        Returns:
            Path to the export directory
        """
        from datetime import datetime
        
        if date_string is None:
            date_string = datetime.now().strftime("%Y-%m-%d")
        
        return cls.EXPORTS_DIR / date_string
