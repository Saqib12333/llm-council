"""Ollama API client for making LLM requests to Ollama Cloud models."""

import asyncio
from typing import List, Dict, Any, Optional
from ollama import AsyncClient
from .config import OLLAMA_HOST


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 300.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Ollama API.

    Args:
        model: Ollama model identifier (e.g., "gpt-oss:120b-cloud")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds (increased for cloud models)

    Returns:
        Response dict with 'content' and optional 'thinking', or None if failed
    """
    try:
        client = AsyncClient(host=OLLAMA_HOST, timeout=timeout)
        
        response = await client.chat(
            model=model,
            messages=messages,
            stream=False
        )
        
        message = response.get('message', {})
        
        return {
            'content': message.get('content'),
            'reasoning_details': message.get('thinking')  # Ollama uses 'thinking' for reasoning
        }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of Ollama model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
