"""
Logging configuration.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path


def configure_logging() -> logging.Logger:

    logdir = Path("logs")
    logdir.mkdir(exist_ok=True)

    logfile = logdir / datetime.now().strftime(
        "download_%Y%m%d_%H%M%S.log"
    )

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file = logging.FileHandler(logfile)
    file.setFormatter(formatter)

    logger.handlers.clear()

    logger.addHandler(console)
    logger.addHandler(file)

    logger.info("Log file: %s", logfile)

    return logger
