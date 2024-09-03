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

# Tweet Selection
MINIMUM_FAV_COUNT = 8
MAX_EXTERIOR_CONTEXT_TOKENS = 8192

# ackend
# Backend API
BACKEND_API_HOST = os.environ.get("BACKEND_API_HOST", "0.0.0.0")
BACKEND_API_PORT = int(os.environ.get("BACKEND_API_PORT", 8000))
BACKEND_URL = os.environ.get("BACKEND_URL")
if not BACKEND_URL:
    BACKEND_URL = f"http://{BACKEND_API_HOST}:{BACKEND_API_PORT}"

BACKEND_API_TITLE = "Tweet Generator backend API"
BACKEND_API_VERSION = "1.0.0"
BACKEND_API_DESCRIPTION = "The backend API that exposes the tweet generation functionality."

# LLM
MODEL = "gpt-4o-2024-08-06"
TEMPERATURE = 0.5

# Frontend
PATH_LOGO = "frontend/media/sidebar_logo.png"
