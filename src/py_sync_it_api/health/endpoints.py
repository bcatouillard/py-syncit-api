"""Health Check endpoints."""

import logging

from fastapi import APIRouter

from py_sync_it_api.shared.db.health import DbHealth

from .exceptions import HealthCheckException
from .schemas import HealthCheckResponse, PingResponse


class HealthCheckFilter(logging.Filter):
    """Health check filter logging.

    Args:
        logging (logging.Filter): logging.Filter object
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter logging when /health path."""
        return record.getMessage().find("/health") == -1


# Remove /credentials/health from application server logs
logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


router = APIRouter(
    tags=["Health"],
)


@router.get(
    "/ping",
    summary="Global API ping",
    operation_id="get_ping",
)
async def ping() -> PingResponse:
    """Global API ping.

    Returns the status of the service and the dependencies.

    Returns:
        PingResponse: default ping response.
    """
    return PingResponse(message="pong")


@router.get(
    "/health",
    summary="Global API Health Check",
    operation_id="get_health_status",
)
async def health_status() -> HealthCheckResponse:
    """Global API health check.

    Returns the status of the service and the dependencies.

    Returns:
        HealthCheckResponse: default health check response.
    """
    return HealthCheckResponse()


@router.get(
    "/health/ready",
    summary="Readiness API Health Check for Kubernetes Probe",
    operation_id="get_health_readiness",
)
async def readiness_health_status(
    is_db_healthy: DbHealth,
) -> HealthCheckResponse:
    """Readiness API health check.

    The /health/ready continues to respond with NOT_READY signal while the API is loading the JSON file since the API
    cannot serve any request without the file in memory. Therefore,
    it may take some time for the API to process the entire file.

    Returns the readiness state to accept incoming requests from the gateway or the upstream proxy.
    Readiness signals that the app is running normally but isn't ready to receive requests just yet.

    Raises:
        HTTPException: 503 HTTP Error if mandatory systems aren't loaded.

    Returns:
        HealthCheckResponse: default health check response.
    """
    if not is_db_healthy:
        raise HealthCheckException
    return HealthCheckResponse()


@router.get(
    "/health/live",
    summary="Liveness API Health Check for Kubernetes Probe",
    operation_id="get_health_liveness",
)
async def liveness_health_status() -> HealthCheckResponse:
    """Liveness API health check.

    The '/health/live' immediately signals LIVE, even though the app is not ready, to prevent the
    container orchestrator layer from restarting the app.

    Returns:
        HealthCheckResponse: default health check response.
    """
    return HealthCheckResponse()
