"""
Logging configuration and utilities.

Provides centralized logging setup for the application.
"""

import logging
import sys
from app.config import get_settings


def setup_logging() -> logging.Logger:
    """
    Configure application logging.

    Sets up logging with appropriate level and format.

    Returns:
        logging.Logger: Configured logger instance.
    """
    settings = get_settings()

    logger = logging.getLogger("deliverease_crypto_api")
    logger.setLevel(getattr(logging, settings.log_level, logging.INFO))

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.log_level, logging.INFO))

    # Formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logging()
