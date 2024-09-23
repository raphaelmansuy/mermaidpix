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
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")