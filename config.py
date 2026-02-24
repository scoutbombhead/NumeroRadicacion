"""
Configuration and logging setup for NumeroRadicacion project
"""

import logging
import os
from datetime import datetime

# ============================================================================
# PATHS AND URLS
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL = "https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion"
EXCEL_FILE_PATH = os.path.join(BASE_DIR, "NumeroRadicacion.xlsx")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE_PATH = os.path.join(LOG_DIR, f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

def setup_logging():
    """
    Configure logging to save to both console and file
    """
    # Create logs directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("NumeroRadicacion")
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger globally
logger = setup_logging()
