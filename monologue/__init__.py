"""
Monologue

Log and display progress information, simply.

For convenience, all standard debug level are importable from this module
"""

from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

from .core import get_logger, PROGRESS
from . import core

get_logger = get_logger
