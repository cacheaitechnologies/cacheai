"""CacheAI Cache Management API resource."""

from typing import Optional, Dict, Any
import logging

from cacheai.exceptions import (
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class Cache:
    """Cache management resource."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def update(
        self,
        cache_key: str,
        *,
        output: Optional[str] = None,
        model_id: Optional[str] = None,
        converter_type: Optional[str] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Update cache entry by cache_key.

        Args:
            cache_key: Cache key (CacheDB key / hash value from CacheKeyConverter)
            output: Updated generated result
            model_id: Updated model ID
            converter_type: Updated converter type
            **kwargs: Additional fields to update

        Returns:
            Update result dictionary

        Raises:
            ValidationError: If no fields to update are provided
            AuthenticationError: If authentication fails
            PermissionDeniedError: If user doesn't own the cache
            NotFoundError: If cache entry not found
        """
        logger.info(f"Updating cache by cache_key: {cache_key}")

        # Build request payload
        payload = {}

        # Add update fields
        if output is not None:
            payload["output"] = output
        if model_id is not None:
            payload["model_id"] = model_id
        if converter_type is not None:
            payload["converter_type"] = converter_type

        # Add additional fields
        payload.update(kwargs)

        # Validate that there are fields to update
        if not payload:
            raise ValidationError(
                "At least one field to update must be provided (output, model_id, converter_type, etc.)"
            )

        logger.debug(f"Update payload: {payload}")

        # Make API request using update method
        try:
            response_data = self._client._update(f"/cache/{cache_key}", json=payload)
            logger.info(f"Cache update successful: {response_data.get('cache_key')}")
            logger.debug(f"Updated fields: {response_data.get('updated_fields')}")
            return response_data
        except Exception as e:
            logger.error(f"Cache update failed: {e}")
            raise

    def get(
        self,
        cache_key: str,
    ) -> Dict[str, Any]:
        """
        Get cache entry by cache_key.

        Args:
            cache_key: Cache key (CacheDB key)

        Returns:
            Cache entry data

        Raises:
            AuthenticationError: If authentication fails
            PermissionDeniedError: If user doesn't have access
            NotFoundError: If cache entry not found
        """
        logger.info(f"Getting cache: cache_key={cache_key}")

        try:
            response_data = self._client._get(f"/cache/{cache_key}")
            logger.debug(f"Cache retrieved: {response_data}")
            return response_data
        except Exception as e:
            logger.error(f"Cache retrieval failed: {e}")
            raise
