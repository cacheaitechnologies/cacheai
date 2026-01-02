"""CacheAI Chat Completion API resource."""

from typing import List, Optional, Union, Iterator, Dict, Any
import json
import logging
import requests

from cacheai.types import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatMessage,
)
from cacheai.exceptions import (
    CacheAIError,
    AuthenticationError,
    APIError,
    ValidationError,
)

logger = logging.getLogger(__name__)


class Completions:
    """Chat completions resource."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def create(
        self,
        *,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[ChatCompletion, Iterator[ChatCompletionChunk]]:
        """
        Create a chat completion.

        Args:
            model: ID of the model to use
            messages: List of messages in the conversation
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum number of tokens to generate
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty (-2.0 to 2.0)
            presence_penalty: Presence penalty (-2.0 to 2.0)
            stop: Up to 4 sequences where the API will stop generating
            stream: Whether to stream back partial progress
            **kwargs: Additional parameters

        Returns:
            ChatCompletion or Iterator[ChatCompletionChunk] if streaming
        """
        # Build request payload
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }

        # Add optional parameters
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if top_p is not None:
            payload["top_p"] = top_p
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if stop is not None:
            payload["stop"] = stop

        # Add any additional parameters
        payload.update(kwargs)

        # Make API request
        if stream:
            return self._stream(payload)
        else:
            logger.info(f"Creating chat completion: model={model}")
            logger.debug(f"Request payload: {payload}")
            response_data = self._client._post("/chat/completions", json=payload)
            logger.debug(f"Response data: {response_data}")
            
            # Check if Baseline model is required (no cache hit)
            if response_data.get("requires_baseline_model"):
                logger.info("No cache hit, calling Baseline model")
                # Call Baseline model
                response_data = self._call_baseline_model(model, messages, payload)
            else:
                logger.info(f"Cache hit or direct response (requires_baseline_model={response_data.get('requires_baseline_model')})")
            
            return ChatCompletion(**response_data)

    def _call_baseline_model(
        self,
        model: str,
        messages: List[Dict[str, str]],
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Call Baseline model API when no cache hit.
        
        Args:
            model: Model ID
            messages: List of messages
            payload: Original request payload
            
        Returns:
            Response data in ChatCompletion format
        """
        from cacheai.utils.baseline_model import call_baseline_model
        
        # Get baseline configuration from client
        baseline_model_provider = self._client.baseline_model_provider
        baseline_model_api_key = self._client.baseline_model_api_key
        baseline_model_base_url = self._client.baseline_model_base_url
        
        # Validate baseline configuration
        if not baseline_model_provider:
            raise ValidationError(
                "Baseline model provider is required for Baseline model calls. "
                "Set baseline_model_provider in Client or CACHEAI_BASELINE_MODEL_PROVIDER env var."
            )
        
        if not baseline_model_api_key:
            raise ValidationError(
                "Baseline LLM API key is required for Baseline model calls. "
                "Set baseline_model_api_key in Client or CACHEAI_BASELINE_MODEL_API_KEY env var."
            )
        
        # Call Baseline model
        return call_baseline_model(
            model=model,
            messages=messages,
            baseline_model_provider=baseline_model_provider,
            baseline_model_api_key=baseline_model_api_key,
            baseline_model_base_url=baseline_model_base_url,
            timeout=self._client.timeout,
            **{k: v for k, v in payload.items() 
               if k in ["temperature", "max_tokens", "top_p", 
                       "frequency_penalty", "presence_penalty", "stop"]}
        )

    def _stream(self, payload: Dict[str, Any]) -> Iterator[ChatCompletionChunk]:
        """Stream chat completion chunks."""
        for line in self._client._stream_post("/chat/completions", json=payload):
            line = line.strip()
            if not line:
                continue
            
            # Skip "data: " prefix
            if line.startswith("data: "):
                line = line[6:]
            
            # Check for [DONE] marker
            if line == "[DONE]":
                break
            
            try:
                chunk_data = json.loads(line)
                yield ChatCompletionChunk(**chunk_data)
            except json.JSONDecodeError:
                continue


class Chat:
    """Chat API resource."""

    def __init__(self, client: Any) -> None:
        self.completions = Completions(client)
