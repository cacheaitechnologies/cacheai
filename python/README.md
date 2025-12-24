# Cache AI Python API

Official Python API for Cache AI - Semantic Caching for Large Language Models

[![PyPI version](https://badge.fury.io/py/cacheai.svg)](https://badge.fury.io/py/cacheai)
[![Python Support](https://img.shields.io/pypi/pyversions/cacheai.svg)](https://pypi.org/project/cacheai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **OpenAI Compatible**: Drop-in replacement for OpenAI Python SDK
- **Semantic Caching**: Automatic caching of similar queries using advanced semantic similarity
- **Multiple LLM Backends**: Support for OpenAI, Anthropic, Google AI, and more
- **Streaming Support**: Full support for streaming responses
- **Type-Safe**: Complete type hints for better IDE support
- **Easy Integration**: Minimal code changes required

## Installation

```bash
pip install cacheai
```

## Quick Start

### Basic Usage

```python
from cacheai import Client

# Initialize client
client = Client(
    api_key="your-cacheai-api-key",
    base_url="https://api.cacheai.tech/v1"  # Optional, this is the default
)

# Create a chat completion
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)
```

### With Environment Variables

```python
import os
from cacheai import Client

# Set environment variables
os.environ["CACHEAI_API_KEY"] = "your-cacheai-api-key"
os.environ["CACHEAI_BACKEND_PROVIDER"] = "openai"
os.environ["CACHEAI_BACKEND_API_KEY"] = "your-openai-api-key"

# Initialize client (reads from environment)
client = Client()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is Python?"}]
)

print(response.choices[0].message.content)
```

### Streaming

```python
from cacheai import Client

client = Client(api_key="your-cacheai-api-key")

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Configuration

### Backend LLM Configuration

Cache AI acts as a caching layer in front of your preferred LLM provider. Configure the backend:

```python
from cacheai import Client

client = Client(
    api_key="your-cacheai-api-key",
    backend_provider="openai",        # "openai", "anthropic", "google", etc.
    backend_api_key="your-openai-key",  # Backend LLM API key
)

# Or use environment variables:
# CACHEAI_BACKEND_PROVIDER=openai
# CACHEAI_BACKEND_API_KEY=sk-...
```

### Cache Control

```python
from cacheai import Client

# Disable caching (for debugging/testing)
client = Client(
    api_key="your-cacheai-api-key",
    enable_cache=False
)

# Or via environment variable:
# CACHEAI_ENABLE_CACHE=false
```

## Advanced Usage

### Context Manager

```python
from cacheai import Client

with Client(api_key="your-api-key") as client:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
# Connection is automatically closed
```

### Custom Timeout and Retries

```python
from cacheai import Client

client = Client(
    api_key="your-api-key",
    timeout=30.0,      # Request timeout in seconds
    max_retries=3      # Maximum retry attempts
)
```

### Error Handling

```python
from cacheai import Client, CacheAIError, AuthenticationError, RateLimitError

client = Client(api_key="your-api-key")

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except CacheAIError as e:
    print(f"API error: {e}")
```

## API Reference

### Client

```python
Client(
    api_key: Optional[str] = None,           # Cache AI API key
    base_url: Optional[str] = None,          # API base URL
    timeout: float = 60.0,                   # Request timeout
    max_retries: int = 2,                    # Max retry attempts
    enable_cache: bool = True,               # Enable semantic caching
    backend_provider: Optional[str] = None,  # Backend LLM provider
    backend_api_key: Optional[str] = None,   # Backend API key
    backend_base_url: Optional[str] = None   # Custom backend URL
)
```

### Chat Completions

```python
client.chat.completions.create(
    model: str,                              # Model ID
    messages: List[Dict[str, str]],          # Conversation messages
    temperature: Optional[float] = None,     # Sampling temperature (0-2)
    max_tokens: Optional[int] = None,        # Max tokens to generate
    top_p: Optional[float] = None,           # Nucleus sampling
    frequency_penalty: Optional[float] = None,  # Frequency penalty
    presence_penalty: Optional[float] = None,   # Presence penalty
    stop: Optional[Union[str, List[str]]] = None,  # Stop sequences
    stream: bool = False                     # Enable streaming
) -> ChatCompletion
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CACHEAI_API_KEY` | Cache AI API key | (required) |
| `CACHEAI_BASE_URL` | API base URL | `https://api.cacheai.tech/v1` |
| `CACHEAI_ENABLE_CACHE` | Enable semantic caching | `true` |
| `CACHEAI_BACKEND_PROVIDER` | Backend LLM provider | (optional) |
| `CACHEAI_BACKEND_API_KEY` | Backend LLM API key | (optional) |
| `CACHEAI_BACKEND_BASE_URL` | Custom backend URL | (optional) |

## Migration from OpenAI

Cache AI is designed to be a drop-in replacement for OpenAI:

```python
# Before (OpenAI)
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(...)

# After (Cache AI)
from cacheai import Client
client = Client(api_key="ca-...", backend_provider="openai", backend_api_key="sk-...")
response = client.chat.completions.create(...)
```

## Examples

See the [examples](./examples/) directory for more usage examples:

- [Basic Chat](./examples/chat_example.py)
- [Streaming](./examples/streaming_example.py)
- [Error Handling](./examples/error_handling.py)

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Type Checking

```bash
mypy cacheai
```

### Code Formatting

```bash
black cacheai
ruff cacheai
```

## Support

- **Documentation**: [https://docs.cacheai.tech](https://docs.cacheai.tech)
- **Issues**: [GitHub Issues](https://github.com/cacheaitechnologies/cacheai/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- [Homepage](https://www.cacheaitechnologies.com)
- [Documentation](https://docs.cacheai.tech)
- [GitHub Repository](https://github.com/cacheaitechnologies/cacheai)
- [PyPI Package](https://pypi.org/project/cacheai/)
