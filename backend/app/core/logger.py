"""Logging configuration for the ARIP backend."""

import sys
from pathlib import Path
from typing import Any

from loguru import logger

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure Loguru sinks for console and rotating file logging."""
    logger.remove()
    log_level = settings.log_level.upper()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        level=log_level,
        format=log_format,
        enqueue=True,
        backtrace=settings.debug,
        diagnose=settings.debug,
    )

    log_path = Path(settings.log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        log_path,
        level=log_level,
        format=log_format,
        rotation=settings.log_rotation,
        retention=settings.log_retention,
        compression="zip",
        enqueue=True,
        backtrace=settings.debug,
        diagnose=settings.debug,
    )


def get_logger(name: str) -> Any:
    """Return a Loguru logger bound to a module name."""
    return logger.bind(name=name)
