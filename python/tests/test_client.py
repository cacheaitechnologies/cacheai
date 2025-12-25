"""Basic tests for Cache AI Python API."""

import pytest
from cacheai import Client
from cacheai.exceptions import CacheAIError


def test_client_initialization():
    """Test client initialization."""
    client = Client(api_key="test-key")
    assert client.api_key == "test-key"
    assert client.base_url == "https://api.cacheai.tech/v1"
    assert client.enable_cache is True


def test_client_initialization_with_custom_url():
    """Test client initialization with custom URL."""
    client = Client(api_key="test-key", base_url="https://custom.api/v1")
    assert client.base_url == "https://custom.api/v1"


def test_client_initialization_without_api_key():
    """Test that client raises error without API key."""
    with pytest.raises(ValueError, match="API key is required"):
        Client()


def test_client_cache_control():
    """Test cache control configuration."""
    client = Client(api_key="test-key", enable_cache=False)
    assert client.enable_cache is False


def test_client_baseline_configuration():
    """Test baseline LLM configuration."""
    client = Client(
        api_key="test-key",
        baseline_model_provider="openai",
        baseline_model_api_key="sk-test"
    )
    assert client.baseline_model_provider == "openai"
    assert client.baseline_model_api_key == "sk-test"


def test_client_has_chat_resource():
    """Test that client has chat resource."""
    client = Client(api_key="test-key")
    assert hasattr(client, "chat")
    assert hasattr(client.chat, "completions")


def test_client_context_manager():
    """Test client as context manager."""
    with Client(api_key="test-key") as client:
        assert client.api_key == "test-key"
    # Client should be closed after context


def test_client_timeout_and_retries():
    """Test custom timeout and retries configuration."""
    client = Client(
        api_key="test-key",
        timeout=30.0,
        max_retries=5
    )
    assert client.timeout == 30.0
    assert client.max_retries == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
