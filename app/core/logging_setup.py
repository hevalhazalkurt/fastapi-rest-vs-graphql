import logging
import sys


def setup_logging() -> logging.Logger:
    """
    Sets up a basic logger
    """
    log_format = "[%(levelname)s]: %(message)s (%(filename)s:%(lineno)d)"

    logging.basicConfig(level=logging.INFO, format=log_format, stream=sys.stdout, force=True)

    logger = logging.getLogger("app")

    return logger


logger = setup_logging()
