import os
import logging
import sys

# Temporary to help debug httpx S3 connection issue in AWS
logging.getLogger("httpx").setLevel("DEBUG")


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(os.environ.get("LOGGING_LEVEL", "INFO").upper())

    # StreamHandler for the console
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    return logger
