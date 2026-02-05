"""Top level logging module."""

import logging
import os
import sys
from typing import Any

from loguru import logger


def setup_logger(debug_mode: bool = False, correlation_id: Any = None):  # noqa: ANN201, ANN401, C901
    """Configure Loguru logger.

    Args:
        debug_mode: Enables debug logging if True.
        correlation_id: your FastAPI ContextVar set by correlationId middleware

    Returns:
        Logger: logger instantiated.
    """
    # Remove default logger handler
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Correlation ID filter
    def correlation_filter(record: Any) -> dict[str, str]:  # noqa: ANN401
        try:
            record["correlation_id"] = correlation_id.get()
            return record["correlation_id"]
        except Exception:  # noqa: BLE001
            return record

    def format_callable(record: Any) -> str:  # noqa: ANN401
        format_separator = " | "
        format_fields = {
            "time": "<green>{time:YYYY-MM-DD HH:mm:SS.SSS zz}</green>",
            "level": "<level>{level: <8}</level>",
            "correlation_id": "[{correlation_id}]",
            "location": "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>",
            "message": "<level>{message}</level>",
            "exception": "{exception}",
            "extra": "extra: {extra}",
            "ending_required_when_format_is_a_callable": "\n",
        }
        if not correlation_id or correlation_id.get():
            del format_fields["correlation_id"]
        if not record["extra"]:
            del format_fields["extra"]
        if not record["exception"]:
            del format_fields["exception"]
        return format_separator.join(format_fields.values())

    # Loguru sink configuration
    sink_kwargs = {
        "format": format_callable,
        "filter": correlation_filter,
        "level": logging.DEBUG if debug_mode else logging.INFO,
    }
    logger.remove(0)  # Remove default logger
    if sys.stdout.isatty() or os.getenv("PYCHARM_HOSTED"):
        # Pretty logging for console
        logger.add(sys.stdout, **sink_kwargs)
        logger.info("Setup logger for console environment with pretty messages.")
    else:
        # JSON logging for non-console
        sink_kwargs["serialize"] = True  # Log in JSON format
        logger.add(sys.stdout, **sink_kwargs)
        logger.info("Setup logger for non-console environment in JSON format.")

    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: Any) -> None:  # noqa: ANN401
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_back and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

    # Redirect standard loggers
    loggers = (
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "asyncio",
        "starlette",
        "httpx",
        "httpcore",
    )
    for logger_name in loggers:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True

    # Set httpx and httpcore log levels to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    return logger
