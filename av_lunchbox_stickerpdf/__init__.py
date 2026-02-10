"""
AV Lunch Box Sticker PDF Generator

A professional package for generating lunch box order stickers and reports from
Google Sheets and image-based order forms.

Quick Start:
    # Generate from Google Sheets
    from av_lunchbox_stickerpdf.cli import CLI
    cli = CLI()
    cli.generate_from_sheets("your-spreadsheet-id")
    
    # Generate from image
    cli.generate_from_image("order-image.png")
"""

__version__ = "2.0.0"
__author__ = "AV Team"
__description__ = "Lunch Box Sticker PDF Generator"

from . import core, data, report, cli, config, utils

# Common imports
from .core import Order, BoxType, RiceType, PDFGenerator
from .data import GoogleSheetsClient, OrderExtractor, ImageOCRExtractor
from .report import SummaryGenerator, SummaryWriter
from .cli import CLI

__all__ = [
    # Core
    'Order',
    'BoxType',
    'RiceType',
    'PDFGenerator',
    # Data
    'GoogleSheetsClient',
    'OrderExtractor',
    'ImageOCRExtractor',
    # Report
    'SummaryGenerator',
    'SummaryWriter',
    # CLI
    'CLI',
    # Modules
    'core',
    'data',
    'report',
    'cli',
    'config',
    'utils',
    # Version
    '__version__',
]
