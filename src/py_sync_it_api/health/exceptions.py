"""Health Check exceptions."""

from fastapi import HTTPException


class HealthCheckException(HTTPException):  # pragma: no cover
    """HTTPException dedicated to the health check liveness."""

    def __init__(
        self,
        detail: str = "App not loaded yet",
        status_code: int = 503,
    ) -> None:
        """Init HealthCheckLiveness503."""
        super().__init__(
            detail=f"""{detail}""",
            status_code=status_code,
        )
