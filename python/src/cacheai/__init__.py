"""Cache AI Python API."""

from cacheai.version import __version__
from cacheai.client import Client
from cacheai.exceptions import (
    CacheAIError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    RateLimitError,
    APIError,
    TimeoutError,
    ConnectionError,
    ValidationError,
)
from cacheai.types import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatMessage,
    Completion,
    Model,
    ModelList,
)

# Note: CacheDB-related modules (db, manager, utils) are managed in GitLab
# but not included in the public GitHub/PyPI release

__all__ = [
    "__version__",
    "Client",
    # Exceptions
    "CacheAIError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "RateLimitError",
    "APIError",
    "TimeoutError",
    "ConnectionError",
    "ValidationError",
    # Types
    "ChatCompletion",
    "ChatCompletionChunk",
    "ChatMessage",
    "Completion",
    "Model",
    "ModelList",
]
