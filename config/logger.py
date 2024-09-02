"""Custom logger for the frontend."""
import logging
import sys
from logging import Logger

from loguru import logger as loguru_logger

_logger_instance = loguru_logger


def get_logger(logger_level: int = logging.INFO) -> Logger:
    global _logger_instance
    if _logger_instance is not None:
        # Remove all handlers
        _logger_instance.remove()
        _logger_instance.add(sys.stderr, level=logger_level)
    else:
        _logger_instance = logging.getLogger(__name__)
        _logger_instance.setLevel(logger_level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_level)
        _logger_instance.addHandler(console_handler)
    return _logger_instance
