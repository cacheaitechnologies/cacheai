"""Basic chat completion example using Cache AI Python API."""

import os
from cacheai import Client, CacheAIError

def main():
    """Run a basic chat completion example."""
    
    # Initialize client
    # You can set API keys via environment variables:
    # export CACHEAI_API_KEY="your-cacheai-api-key"
    # export CACHEAI_BACKEND_PROVIDER="openai"
    # export CACHEAI_BACKEND_API_KEY="your-openai-api-key"
    
    try:
        client = Client(
            api_key=os.getenv("CACHEAI_API_KEY", "your-cacheai-api-key"),
            backend_provider=os.getenv("CACHEAI_BACKEND_PROVIDER", "openai"),
            backend_api_key=os.getenv("CACHEAI_BACKEND_API_KEY", "your-openai-api-key"),
        )
        
        print("=" * 60)
        print("Cache AI Python API - Chat Completion Example")
        print("=" * 60)
        print()
        
        # Example 1: Simple chat
        print("Example 1: Simple Chat")
        print("-" * 60)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "What is LLM?"}
            ]
        )
        
        print(f"User: What is LLM?")
        print(f"Assistant: {response.choices[0].message.content}")
        print()
        
        print("=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)
        
    except CacheAIError as e:
        print(f"Error: {e}")
        print("\nPlease set the following environment variables:")
        print("  CACHEAI_API_KEY")
        print("  CACHEAI_BACKEND_PROVIDER")
        print("  CACHEAI_BACKEND_API_KEY")


if __name__ == "__main__":
    main()
