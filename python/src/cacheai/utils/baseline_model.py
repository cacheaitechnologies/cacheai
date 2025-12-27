"""Baseline model utility for calling baseline LLMs on no cache hit."""

from typing import Dict, Any, List, Optional
import requests
from cacheai.exceptions import APIError, ValidationError


def call_baseline_model(
    model: str,
    messages: List[Dict[str, str]],
    baseline_model_provider: str,
    baseline_model_api_key: str,
    baseline_model_base_url: Optional[str] = None,
    timeout: float = 60.0,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Call Baseline model API (OpenAI-compatible).
    
    Args:
        model: Model ID
        messages: List of messages
        baseline_model_provider: Baseline model provider (openai, etc.)
        baseline_model_api_key: API key for baseline model
        baseline_model_base_url: Custom base URL (optional)
        timeout: Request timeout in seconds
        **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
    Returns:
        Response data in ChatCompletion format
        
    Raises:
        ValidationError: If provider is unsupported or config is invalid
        APIError: If API call fails
    """
    # Set default base URL based on provider
    if not baseline_model_base_url:
        if baseline_model_provider == "openai":
            baseline_model_base_url = "https://api.openai.com/v1"
        else:
            raise ValidationError(f"Unsupported baseline model provider: {baseline_model_provider}")
        
    # Call Baseline model API (OpenAI-compatible)
    url = f"{baseline_model_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {baseline_model_api_key}",
        "Content-Type": "application/json",
    }
    
    # Build request payload
    payload = {
        "model": model,
        "messages": messages,
    }
    
    # Add optional parameters
    # Note: OpenAI's newer models (o1, gpt-4o, gpt-5.2, etc.) use max_completion_tokens instead of max_tokens
    for key in ["temperature", "top_p", "frequency_penalty", "presence_penalty", "stop"]:
        if key in kwargs and kwargs[key] is not None:
            payload[key] = kwargs[key]
    
    # Handle max_tokens vs max_completion_tokens
    # Newer models require max_completion_tokens, older models use max_tokens
    if "max_completion_tokens" in kwargs and kwargs["max_completion_tokens"] is not None:
        payload["max_completion_tokens"] = kwargs["max_completion_tokens"]
    elif "max_tokens" in kwargs and kwargs["max_tokens"] is not None:
        # For newer models, convert max_tokens to max_completion_tokens
        payload["max_completion_tokens"] = kwargs["max_tokens"]
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
        result = response.json()
        return result
        
    except requests.exceptions.RequestException as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_json = e.response.json()
                error_detail = f" - Details: {error_json}"
            except:
                error_detail = f" - Response text: {e.response.text}"
        
        raise APIError(f"Baseline model API call failed: {e}{error_detail}")
