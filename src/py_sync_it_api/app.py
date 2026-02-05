"""Boostrap app."""

import contextlib

import fastapi_versionizer
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRoute
from loguru import logger

from py_logger import setup_logger
from py_sync_it_api.middlewares.request_logger_middleware import RequestLoggerMiddleware

from .exceptions import ApiError, UnprocessableEntityError
from .exceptions_handler import (
    fallback_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from .shared.router import router as global_router
from .shared.settings import Settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    """Permits to manage setup and teardown of the FastAPI instance."""
    try:
        setup_logger(debug_mode=Settings.get().DEBUG)
    except Exception as e:
        logger.error("Logger Initialization Failed", e)
        raise

    yield


def bootstrap() -> FastAPI:
    """Helper function that bootstrap FastAPI App."""
    # This should be filled as possible as it will appear in the swagger
    app = FastAPI(
        debug=Settings.get().DEBUG,
        title="SyncIt API",
        summary="SyncIt API",
        description="Sync It API",
        version="0.0.1",
        dependencies=[],
        swagger_ui_init_oauth={},
        swagger_ui_parameters={},
        middleware=[],
        exception_handlers={
            RequestValidationError: validation_exception_handler,
            HTTPException: http_exception_handler,
            Exception: fallback_exception_handler,
        },
        lifespan=lifespan,
        terms_of_service="All rights reserved",
        log_config=None,
        log_level=None,
    )
    app.add_middleware(RequestLoggerMiddleware)

    for route in global_router.routes:
        if isinstance(route, APIRoute):
            route.responses.update(
                {
                    **UnprocessableEntityError.response(),
                    **ApiError.response(),
                    "default": {"model": ApiError.model},
                },
            )

    app.include_router(global_router)

    api_versions = fastapi_versionizer.Versionizer(
        app=app,
        prefix_format="/v{major}",
        semantic_version_format="{major}",
        include_main_docs=False,
        include_main_openapi_route=False,
        include_versions_route=False,
        include_version_docs=True,
        include_version_openapi_route=True,
    ).versionize()

    major_api_versions = [v[0] for v in api_versions]

    @app.get("/", include_in_schema=False)
    @app.get("/docs", include_in_schema=False)
    async def docs_redirect():  # noqa: ANN202
        """Redirects to docs."""
        return RedirectResponse(url=f"/v{major_api_versions[-1]}/docs")

    @app.get("/redoc", include_in_schema=False)
    async def redoc_redirect():  # noqa: ANN202
        """Redirects to docs."""
        return RedirectResponse(url=f"/v{major_api_versions[-1]}/redoc")

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_redirect():  # noqa: ANN202
        """Redirects to docs."""
        return RedirectResponse(url=f"/v{major_api_versions[-1]}/openapi.json")

    return app


app = bootstrap()  # pragma: no cover
