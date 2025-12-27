"""
Example: Using Cache AI with Baseline model fallback

This example demonstrates how Cache AI automatically falls back to a Baseline
model (OpenAI) when there is no cache hit.

Using timestamp-based prompts ensures no cache hit for testing purposes.
"""

from cacheai import Client
from datetime import datetime
import random
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get API keys from environment variables
cacheai_api_key = os.getenv("CACHEAI_API_KEY")
baseline_model_provider = os.getenv("CACHEAI_BASELINE_MODEL_PROVIDER", "openai")
baseline_model_api_key = os.getenv("CACHEAI_BASELINE_MODEL_API_KEY")

if not cacheai_api_key:
    raise ValueError(
        "CACHEAI_API_KEY environment variable is required.\n"
        "Set it with: export CACHEAI_API_KEY=your-cacheai-api-key"
    )

if not baseline_model_api_key:
    raise ValueError(
        "CACHEAI_BASELINE_MODEL_API_KEY environment variable is required.\n"
        "Set it with: export CACHEAI_BASELINE_MODEL_API_KEY=your-baseline-model-api-key"
    )

# Initialize Cache AI client with Baseline model configuration
client = Client(
    api_key=cacheai_api_key,
    base_url="https://api.cacheai.tech/v1",
    # Baseline model configuration (used on no cache hit)
    baseline_model_provider=baseline_model_provider,
    baseline_model_api_key=baseline_model_api_key,
)

# Generate unique prompt using current timestamp (ensures no cache hit)
now = datetime.now()
date_str = now.strftime("%Y%m%d")  # YYYYMMDD
time_str = now.strftime("%H%M%S")  # HHMMSS
random_str = random.randint(0, 9999)  # Random number 0-9999

prompt = f"What is {date_str} + {time_str} + {random_str}?"

print(f"Prompt: {prompt}")
print("This will trigger Baseline model call (no cache hit expected)\n")

try:
    # Make a chat completion request
    # Since the prompt is unique, it will call the Baseline model
    response = client.chat.completions.create(
        model="gpt-5.2",  # Default model for OpenAI baseline
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100,
    )

    print("Response:")
    print(f"Full response object: {response}")
    print(f"\nModel: {response.model}")
    print(f"Usage: {response.usage}")
    
    if response.choices and len(response.choices) > 0:
        choice = response.choices[0]
        print(f"Choice: {choice}")
        if hasattr(choice, 'message'):
            print(f"Message: {choice.message}")
            print(f"Content: {choice.message.content}")
        else:
            print("No message in choice")
    else:
        print("No choices in response")
    
    # Check if this was from cache or Baseline model
    if hasattr(response, 'cache_hit'):
        print(f"\nCache Hit: {response.cache_hit}")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
