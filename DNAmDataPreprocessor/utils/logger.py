import logging
import os
from typing import Dict, Any

def setup_logger(name: str, log_config: Dict[str, Any]) -> logging.Logger:
    """
    Set up logger
    
    Args:
        name: Logger Name
        log_config: Log Configuration
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid adding the processor repeatedly
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, log_config.get('level', 'INFO')))
    
    # Create Formatter
    formatter = logging.Formatter(
        log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    # Console Processor
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Processor
    log_file = log_config.get('file')
    if log_file:
        # Create log directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger