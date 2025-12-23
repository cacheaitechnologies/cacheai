"""CacheAI Chat Completion API resource."""

from typing import List, Optional, Union, Iterator, Dict, Any
import json

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
            response_data = self._client._post("/chat/completions", json=payload)
            return ChatCompletion(**response_data)

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
