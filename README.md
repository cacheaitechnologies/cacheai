# CacheAI

Official Python API and tools for CacheAI - Semantic Caching for Large Language Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

CacheAI provides semantic caching for large language models, significantly reducing API costs and latency by intelligently caching similar queries. This repository contains official API and integration tools for various programming languages and platforms.

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
- [API Documentation](https://docs.cacheai.tech)
- [Website](https://www.cacheaitechnologies.com)

## Getting an API Key

1. Visit [CacheAI Technologies](https://www.cacheaitechnologies.com)
2. Sign up for an account
3. Generate your API key from the dashboard

## Support

- **Documentation**: [https://docs.cacheai.tech](https://docs.cacheai.tech)
- **Issues**: [GitHub Issues](https://github.com/cacheaitechnologies/cacheai/issues)
- **Email**: info@cacheaitechnologies.com

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Homepage](https://www.cacheaitechnologies.com)
- [Documentation](https://docs.cacheai.tech)
- [Python Package (PyPI)](https://pypi.org/project/cacheai/)

---

© 2025 CacheAI Technologies, Inc.
