import typing

from app.clients.hibp.types import HIBPResponse


__all__ = [
    "HIBPError",
    "HIBPAuthError",
    "HIBPRateLimitError",
    "HIBPClientError",
    "HIBPServerError",
    "HIBPResponseError",
]


class HIBPError(Exception):
    """Base exception for HIBP API errors."""

    def __init__(
        self,
        message: str = "An error occurred with the HIBP API",
        code: typing.Optional[int] = None,
        response: typing.Optional[HIBPResponse] = None,
    ):
        self.message = message
        self.code = code
        self.response = response
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class HIBPAuthError(HIBPError):
    """Exception raised for authentication errors (401, 403)."""

    def __init__(
        self,
        message: str = "Authentication failed. Invalid API key or insufficient permissions.",
        code: typing.Optional[int] = None,
        response: typing.Optional[HIBPResponse] = None,
    ):
        super().__init__(message, code, response)


class HIBPRateLimitError(HIBPError):
    """Exception raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please retry after some time.",
        code: int = 429,
        response: typing.Optional[HIBPResponse] = None,
        retry_after: typing.Optional[int] = None,
    ):
        super().__init__(message, code, response)
        self.retry_after = retry_after

    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after:
            return f"{base} (Retry after {self.retry_after}s)"
        return base


class HIBPClientError(HIBPError):
    """Exception raised for client errors (4xx)."""

    pass


class HIBPServerError(HIBPError):
    """Exception raised for server errors (5xx)."""

    def __init__(
        self,
        message: str = "HIBP server error occurred.",
        code: typing.Optional[int] = None,
        response: typing.Optional[HIBPResponse] = None,
    ):
        super().__init__(message, code, response)


class HIBPResponseError(HIBPError):
    """Exception raised when response parsing fails."""

    def __init__(self, message: str = "Failed to parse HIBP API response"):
        super().__init__(message)
