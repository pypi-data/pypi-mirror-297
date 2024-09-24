import logging
from decimal import Decimal
from enum import Enum
from logging import (
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)

from komoutils.logger.logger import KomoLogger


def log_encoder(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, Enum):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


__all__ = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "KomoLogger",
    "log_encoder"
]
logging.setLoggerClass(KomoLogger)
