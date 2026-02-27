"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", name: Optional[str] = None) -> logging.Logger:
    """
    Set up logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        name: Logger name. If None, uses the package logger.
    
    Returns:
        Configured logger
    """
    
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    log_level = level_map.get(level.upper(), logging.INFO)
    
    logger_name = name or "av_lunchbox"
    logger = logging.getLogger(logger_name)
    
    # Only add handlers if they haven't been added yet
    if not logger.handlers:
        logger.setLevel(log_level)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s │ %(name)-20s │ %(levelname)-8s │ %(message)s',
            datefmt='%H:%M:%S',
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module. Uses the package-wide logger hierarchy.
    
    Args:
        module_name: The module name (e.g., 'core.pdf_generator')
    
    Returns:
        Logger for the module
    """
    return logging.getLogger(f"av_lunchbox.{module_name}")


# Initialize the root package logger on import
logger = setup_logging()
