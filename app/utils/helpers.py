from typing import Any
import logging

logger = logging.getLogger("fastapi")


def log(message: Any, level: str = "error") -> None:
    {
        "debug": logger.debug,
        "warn": logger.warn,
        "error": logger.error,
        "info": logger.info,
    }[level](message)
