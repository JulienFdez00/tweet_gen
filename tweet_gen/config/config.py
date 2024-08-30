"""Main configuration file for the project."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from config.logger import get_logger

# Paths
ROOT_PATH = Path(__file__).parent.parent

# Load environment variables
load_dotenv(ROOT_PATH / ".env")

# Logging
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL", "INFO")
if LOGGER_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    LOGGER_LEVEL = "INFO"
LOGGER = get_logger(logger_level=getattr(logging, LOGGER_LEVEL))
