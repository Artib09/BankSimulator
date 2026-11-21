"""Reusable decorators for logging and measuring operations."""

import functools
import logging
import time
from typing import Any, Callable


logger = logging.getLogger(__name__)


def log_operation(function: Callable) -> Callable:
    """Log the start and successful completion of a function.

    Exceptions are logged and re-raised, so the original function
    behaviour is not changed.
    """

    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info("Started: %s", function.__qualname__)

        try:
            result = function(*args, **kwargs)
        except Exception:
            logger.exception("Failed: %s", function.__qualname__)
            raise

        logger.info("Succeeded: %s", function.__qualname__)
        return result

    return wrapper


def measure_time(
    warning_threshold: float | None = None,
) -> Callable:
    """Measure execution time of a function.

    Args:
        warning_threshold: Optional time in seconds. If execution takes
            longer than this value, the result is logged as a warning.
            Otherwise, it is logged as debug information.
    """

    def decorator(function: Callable) -> Callable:
        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()

            try:
                return function(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start

                if warning_threshold is not None and elapsed > warning_threshold:
                    logger.warning(
                        "%s finished after %.6f s",
                        function.__qualname__,
                        elapsed,
                    )
                else:
                    logger.debug(
                        "%s finished after %.6f s",
                        function.__qualname__,
                        elapsed,
                    )

        return wrapper

    return decorator


def log_account_operation(method: Callable) -> Callable:
    """Log an account operation using the account identifier.

    The decorated method must be an instance method of an object
    exposing an ``id`` property.
    """

    @functools.wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        operation = method.__name__
        account_id = self.id

        logger.info(
            "Started: %s | account_id=%s",
            operation,
            account_id,
        )

        try:
            result = method(self, *args, **kwargs)
        except ValueError:
            # Error from account operations
            raise
        except Exception:
            logger.exception(
                "Failed: %s | account_id=%s",
                operation,
                account_id,
            )
            raise

        logger.info(
            "Succeeded: %s | account_id=%s",
            operation,
            account_id,
        )

        return result
    return wrapper