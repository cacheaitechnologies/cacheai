"""Cache AI Python API client."""

import os
from typing import Optional, Dict, Any, Iterator
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from cacheai.resources import Chat
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


class Client:
    """
    Cache AI API client.

    Example:
        ```python
        from cacheai import Client

        client = Client(
            api_key="your-api-key",
            base_url="https://api.cacheai.io/v1"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        ```
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        enable_cache: bool = True,
        baseline_model_provider: Optional[str] = None,
        baseline_model_api_key: Optional[str] = None,
        baseline_model_base_url: Optional[str] = None,
    ) -> None:
        """
        Initialize Cache AI client.

        Args:
            api_key: Cache AI API key. If not provided, reads from CACHEAI_API_KEY env var
            base_url: Base URL for API. If not provided, reads from CACHEAI_BASE_URL env var
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            enable_cache: Enable CacheAI semantic caching (default: True)
            baseline_model_provider: Baseline LLM provider (openai, anthropic, google, etc.)
            baseline_model_api_key: Baseline LLM API key
            baseline_model_base_url: Custom baseline LLM endpoint URL
        """
        self.api_key = api_key or os.getenv("CACHEAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via api_key parameter or "
                "CACHEAI_API_KEY environment variable."
            )

        self.base_url = (
            base_url
            or os.getenv("CACHEAI_BASE_URL")
            or "https://api.cacheai.tech/v1"
        )
        self.base_url = self.base_url.rstrip("/")

        self.timeout = timeout
        self.max_retries = max_retries
        self.enable_cache = enable_cache

        # Baseline model configuration
        self.baseline_model_provider = baseline_model_provider or os.getenv("CACHEAI_BASELINE_MODEL_PROVIDER")
        self.baseline_model_api_key = baseline_model_api_key or os.getenv("CACHEAI_BASELINE_MODEL_API_KEY")
        self.baseline_model_base_url = baseline_model_base_url or os.getenv("CACHEAI_BASELINE_MODEL_BASE_URL")

        # Setup session with retry strategy
        self._session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

        # Initialize resources
        self.chat = Chat(self)

    def _get_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Build request headers."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "cacheai-python/0.1.0",
        }

        # Add cache control header
        if not self.enable_cache:
            headers["X-CacheAI-Enable-Cache"] = "false"

        # Add baseline configuration headers
        if self.baseline_model_provider:
            headers["X-CacheAI-Baseline-Model-Provider"] = self.baseline_model_provider
        if self.baseline_model_api_key:
            headers["X-CacheAI-Baseline-Model-API-Key"] = self.baseline_model_api_key
        if self.baseline_model_base_url:
            headers["X-CacheAI-Baseline-Model-Base-URL"] = self.baseline_model_base_url

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle error responses and raise appropriate exceptions."""
        status_code = response.status_code
        
        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", response.text)
        except Exception:
            error_message = response.text

        if status_code == 401:
            raise AuthenticationError(
                error_message,
                status_code=status_code,
                response_body=response.text,
            )
        elif status_code == 403:
            raise PermissionDeniedError(
                error_message,
                status_code=status_code,
                response_body=response.text,
            )
        elif status_code == 404:
            raise NotFoundError(
                error_message,
                status_code=status_code,
                response_body=response.text,
            )
        elif status_code == 429:
            raise RateLimitError(
                error_message,
                status_code=status_code,
                response_body=response.text,
            )
        elif status_code >= 500:
            raise APIError(
                error_message,
                status_code=status_code,
                response_body=response.text,
            )
        else:
            raise CacheAIError(
                error_message,
                status_code=status_code,
                response_body=response.text,
            )

    def _post(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}{path}"
        headers = self._get_headers(kwargs.pop("headers", None))

        try:
            response = self._session.post(
                url,
                headers=headers,
                timeout=self.timeout,
                **kwargs,
            )

            if not response.ok:
                self._handle_error_response(response)

            return response.json()

        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out: {e}")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection failed: {e}")
        except requests.exceptions.RequestException as e:
            raise CacheAIError(f"Request failed: {e}")

    def _stream_post(self, path: str, **kwargs: Any) -> Iterator[str]:
        """Make a streaming POST request."""
        url = f"{self.base_url}{path}"
        headers = self._get_headers(kwargs.pop("headers", None))

        try:
            response = self._session.post(
                url,
                headers=headers,
                timeout=self.timeout,
                stream=True,
                **kwargs,
            )

            if not response.ok:
                self._handle_error_response(response)

            for line in response.iter_lines():
                if line:
                    yield line.decode("utf-8")

        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out: {e}")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection failed: {e}")
        except requests.exceptions.RequestException as e:
            raise CacheAIError(f"Request failed: {e}")

    def _get(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make a GET request."""
        url = f"{self.base_url}{path}"
        headers = self._get_headers(kwargs.pop("headers", None))

        try:
            response = self._session.get(
                url,
                headers=headers,
                timeout=self.timeout,
                **kwargs,
            )

            if not response.ok:
                self._handle_error_response(response)

            return response.json()

        except requests.exceptions.Timeout as e:
            raise TimeoutError(f"Request timed out: {e}")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection failed: {e}")
        except requests.exceptions.RequestException as e:
            raise CacheAIError(f"Request failed: {e}")

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
