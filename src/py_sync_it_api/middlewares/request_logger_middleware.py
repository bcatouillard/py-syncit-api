"""Request logger middleware."""

import time

from fastapi import Request
from loguru import logger
from starlette.types import ASGIApp, Receive, Scope, Send

from .constants import FILTERED_PATH


class RequestLoggerMiddleware:
    """Middleware that logs the beginning and end of each HTTP request."""

    def __init__(self, app: ASGIApp, *args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG002
        """Initialize RequestLoggerMiddleware."""
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:  # noqa: RET503
        """Process an ASGI request and log timing information.

        Args:
            scope: ASGI connection scope
            receive: ASGI receive function
            send: ASGI send function

        Returns:
            None
        """
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)
        path = request.url.path
        method = request.method
        if path not in FILTERED_PATH:
            logger.info(f"Request started: {method} {path}")

        start_time = time.time()

        async def send_wrapper(message):  # noqa: ANN001, ANN202
            if message["type"] == "http.response.start":
                status_code = message["status"]
                duration = time.time() - start_time
                if path not in FILTERED_PATH:
                    log_message = (
                        f"Request completed: {method} {path} - Status: {status_code} - Duration: {duration:.3f}s"
                    )
                    if status_code >= 400:  # noqa: PLR2004
                        logger.error(log_message)
                    else:
                        logger.info(log_message)
            await send(message)

        await self.app(scope, receive, send_wrapper)
