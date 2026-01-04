# Cache AI

Official Python API and tools for Cache AI - Semantic Caching for Large Language Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Cache AI provides semantic caching for large language models, significantly reducing API costs and latency by intelligently caching similar queries. This repository contains official API and integration tools for various programming languages and platforms.

## Features

- 🚀 **Semantic Caching**: Intelligent caching based on semantic similarity
- 🔌 **OpenAI Compatible**: Drop-in replacement for OpenAI SDK
- ⚡ **High Performance**: Reduce latency and API costs significantly
- 🛡️ **Enterprise Ready**: Secure, scalable, and production-tested

## Repository Structure

```
cacheai/
└── python/          # Python API
```

## Quick Start

### Python

```bash
cd python
pip install cacheai
```

```python
from cacheai import Client

client = Client(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

See [Python API documentation](./python/README.md) for more details.

## Documentation

- [Python API](./python/README.md)
- [Website](https://www.cacheaitechnologies.com)

## Getting an API Key

Please contact us at **info@cacheaitechnologies.com** for any questions.

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Website](https://www.cacheaitechnologies.com)
- [Python Package (PyPI)](https://pypi.org/project/cacheai/)

---

© 2026 CacheAI Technologies, Inc.
