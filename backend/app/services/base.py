import typing
from typing import Any, Optional

from fastapi import HTTPException


class ServiceError(Exception):
    """Custom Service Error Exception. Services should prefer raising this exception."""

    def __init__(
        self,
        message: str,
        service_name: str,
        http_status: int = 500,
    ):
        self.message = message
        self.service_name = service_name
        self.http_status = http_status
        super().__init__(self.message)

    def as_http_exception(self) -> "HTTPException":
        return HTTPException(status_code=self.http_status, detail=self.message)


ServiceStatus = typing.TypedDict(
    "ServiceStatus",
    {
        "name": str,
        "status": str,
        "error": Optional[str],
    },
)


class Service:
    """Base Service Class"""

    id: str = "base"
    name: str = "Base Service"

    def __init__(self, logger: Optional[Any] = None):
        self.logger = logger
