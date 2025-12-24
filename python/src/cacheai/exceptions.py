"""Cache AI Python API exceptions."""

from typing import Optional


class CacheAIError(Exception):
    """Base exception for all CacheAI errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(CacheAIError):
    """Raised when authentication fails (401)."""

    pass


class PermissionDeniedError(CacheAIError):
    """Raised when permission is denied (403)."""

    pass


class NotFoundError(CacheAIError):
    """Raised when resource is not found (404)."""

    pass


class RateLimitError(CacheAIError):
    """Raised when rate limit is exceeded (429)."""

    pass


class APIError(CacheAIError):
    """Raised when API returns an error (500+)."""

    pass


class TimeoutError(CacheAIError):
    """Raised when request times out."""

    pass


class ConnectionError(CacheAIError):
    """Raised when connection fails."""

    pass


class ValidationError(CacheAIError):
    """Raised when request validation fails."""

    pass
