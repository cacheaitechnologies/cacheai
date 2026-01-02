"""
Example: Using Cache AI with Baseline model fallback

This example demonstrates how Cache AI automatically falls back to a Baseline
model (OpenAI) when there is no cache hit.

Using timestamp-based prompts ensures no cache hit for testing purposes.

Required Environment Variables:
  - CACHEAI_API_KEY: Your Cache AI API key
  - CACHEAI_BASELINE_MODEL_PROVIDER: Baseline LLM provider (default: "openai")
  - CACHEAI_BASELINE_MODEL_API_KEY: Your baseline LLM API key

Optional Environment Variables:
  - CACHEAI_BASELINE_MODEL_BASE_URL: Custom endpoint URL for baseline model
    Examples:
      - Azure OpenAI: https://your-resource.openai.azure.com/openai/deployments/your-deployment
      - Local server: http://localhost:8000/v1
      - Other OpenAI-compatible endpoints

Usage:
  export CACHEAI_API_KEY="your-cacheai-api-key"
  export CACHEAI_BASELINE_MODEL_PROVIDER="openai"
  export CACHEAI_BASELINE_MODEL_API_KEY="your-openai-api-key"
  # Optional: for custom endpoints
  # export CACHEAI_BASELINE_MODEL_BASE_URL="http://localhost:8000/v1"
  
  python baseline_model_example.py
"""

from cacheai import Client
from datetime import datetime
import random
import os
import logging

logger = logging.getLogger(__name__)


def main():
    """Main function to run the baseline model example."""
    # Get API keys from environment variables
    cacheai_api_key = os.getenv("CACHEAI_API_KEY")
    baseline_model_provider = os.getenv("CACHEAI_BASELINE_MODEL_PROVIDER", "openai")
    baseline_model_api_key = os.getenv("CACHEAI_BASELINE_MODEL_API_KEY")
    baseline_model_base_url = os.getenv("CACHEAI_BASELINE_MODEL_BASE_URL")  # Optional: Custom endpoint URL

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

    # Log configuration
    logger.info("=" * 60)
    logger.info("Cache AI Baseline Model Example - Configuration")
    logger.info("=" * 60)
    logger.info(f"CACHEAI_API_KEY: {'*' * 8}...{cacheai_api_key[-4:] if len(cacheai_api_key) > 4 else '****'}")
    logger.info(f"CACHEAI_BASELINE_MODEL_PROVIDER: {baseline_model_provider}")
    logger.info(f"CACHEAI_BASELINE_MODEL_API_KEY: {'*' * 8}...{baseline_model_api_key[-4:] if len(baseline_model_api_key) > 4 else '****'}")
    logger.info(f"CACHEAI_BASELINE_MODEL_BASE_URL: {baseline_model_base_url or 'Not set (using default)'}")
    logger.info("=" * 60)

    # Initialize Cache AI client with Baseline model configuration
    client = Client(
        api_key=cacheai_api_key,
        base_url="https://api.cacheai.tech/v1",
        # Baseline model configuration (used on no cache hit)
        baseline_model_provider=baseline_model_provider,
        baseline_model_api_key=baseline_model_api_key,
        baseline_model_base_url=baseline_model_base_url,  # Optional: for custom endpoints (Azure, local servers, etc.)
    )

    # Generate unique prompt using current timestamp (ensures no cache hit)
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")  # YYYYMMDD
    time_str = now.strftime("%H%M%S")  # HHMMSS
    random_str = random.randint(0, 9999)  # Random number 0-9999

    prompt = f"What is {date_str} + {time_str} + {random_str}?"

    logger.info(f"Prompt: {prompt}")
    logger.info("This will trigger Baseline model call (no cache hit expected)")

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

        logger.info("Response received")
        logger.debug(f"Full response object: {response}")
        logger.info(f"Model: {response.model}")
        logger.info(f"Usage: {response.usage}")
        
        if response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            logger.debug(f"Choice: {choice}")
            if hasattr(choice, 'message'):
                logger.debug(f"Message: {choice.message}")
                logger.info(f"Content: {choice.message.content}")
            else:
                logger.warning("No message in choice")
        else:
            logger.warning("No choices in response")
        
        # Check if this was from cache or Baseline model
        if hasattr(response, 'cache_hit'):
            logger.info(f"Cache Hit: {response.cache_hit}")
        
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    # Configure logging (DEBUG level to see all details)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()
