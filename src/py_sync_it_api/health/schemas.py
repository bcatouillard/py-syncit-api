"""Health Check schemas."""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Object which represents the health check get response."""

    status: str = "ok"


class PingResponse(BaseModel):
    """Object which represents the ping get response."""

    message: str = "pong"
