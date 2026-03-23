import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_FILE = "revenueops.log"

LOG_DIR = Path(".")
LOG_DIR.mkdir(exist_ok=True)


def setup_logger() -> logging.Logger:

    logger = logging.getLogger("revenueops")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(LOG_FORMAT)

    # console handler (docker logs)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # rotating file handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10_000_000,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    return logger.getChild(name)