# logger.py
import logging
import os


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

    # Create log directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger