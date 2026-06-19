"""
Simple retry helper.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry(
    operation: Callable[[], T],
    *,
    retries: int = 3,
    delay: float = 10.0,
) -> T:
    """
    Execute an operation with retry.

    Parameters
    ----------
    operation
        Zero-argument callable.

    retries
        Maximum number of attempts.

    delay
        Delay between attempts in seconds.

    Returns
    -------
    Result of the operation.

    Raises
    ------
    Exception
        Re-raises the final exception if all attempts fail.
    """

    last_exception: Exception | None = None

    for attempt in range(1, retries + 1):

        try:

            if attempt > 1:
                logger.info(
                    "Retry %d/%d",
                    attempt,
                    retries,
                )

            return operation()

        except Exception as exc:

            last_exception = exc

            if attempt == retries:
                break

            logger.warning(
                "Attempt %d/%d failed: %s",
                attempt,
                retries,
                exc,
            )

            sleep_time = delay * (2 ** (attempt - 1))

            logger.info(
                "Waiting %.1f seconds...",
                sleep_time,
            )

            time.sleep(sleep_time)

    assert last_exception is not None
    raise last_exception
