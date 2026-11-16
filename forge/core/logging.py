"""Structured logging and secret masking for FORGE."""

import json
import logging
import re
import sys
from typing import Any

SECRET_PATTERNS = [
    re.compile(r"(AIzaSy[A-Za-z0-9_-]{33})"),
    re.compile(r"(api[_-]?key[\"']?\s*[:=]\s*[\"']?)([A-Za-z0-9_\-\.]{8,})", re.IGNORECASE),
    re.compile(r"(password[\"']?\s*[:=]\s*[\"']?)([^\"'\s]{4,})", re.IGNORECASE),
    re.compile(r"(bearer\s+)([A-Za-z0-9_\-\.]{10,})", re.IGNORECASE),
]


def mask_secrets(text: str) -> str:
    """Mask known sensitive patterns from log messages."""
    if not isinstance(text, str):
        return text
    masked = text
    for pattern in SECRET_PATTERNS:
        masked = pattern.sub(r"\1[REDACTED]", masked)
    return masked


class SafeJsonFormatter(logging.Formatter):
    """JSON formatter with automatic secret redaction."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": mask_secrets(record.getMessage()),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)
        return json.dumps(log_entry)


class SafeTextFormatter(logging.Formatter):
    """Console text formatter with secret redaction."""

    def format(self, record: logging.LogRecord) -> str:
        record.msg = mask_secrets(str(record.msg))
        return super().format(record)


def setup_logger(
    name: str = "forge", log_level: str = "INFO", log_format: str = "text"
) -> logging.Logger:
    """Initialize a safe, structured logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        if log_format.lower() == "json":
            handler.setFormatter(SafeJsonFormatter())
        else:
            handler.setFormatter(
                SafeTextFormatter(
                    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
        logger.addHandler(handler)
        logger.propagate = False

    return logger


logger = setup_logger()
