"""
This module provides functions to process markdown files and convert Mermaid diagrams to PNG images.
"""

import logging


def setup_logging(verbose: bool) -> None:
    """
    Set up logging configuration.

    Args:
        verbose (bool): If True, set the logging level to DEBUG. If False, set it to INFO.

    Returns:
        None
    """
    level = logging.DEBUG if verbose else logging.INFO

    # Create a custom formatter with timestamp, level, and message
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Create a StreamHandler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create a FileHandler to log to a file
    file_handler = logging.FileHandler("mermaidpix.log")
    file_handler.setFormatter(formatter)

    # Create the logger and set the handlers
    logger = logging.getLogger("mermaidpix")
    logger.setLevel(level)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")
