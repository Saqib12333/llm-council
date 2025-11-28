"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Council members - list of Ollama cloud model identifiers
# Using Ollama Cloud models (requires `ollama signin` on the machine)
COUNCIL_MODELS = [
    "gpt-oss:120b-cloud",
    "qwen3-coder:480b-cloud",
    "deepseek-v3.1:671b-cloud",
    "kimi-k2-thinking:cloud",
    "glm-4.6:cloud",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "deepseek-v3.1:671b-cloud"

# Ollama API host (local Ollama server handles cloud model routing)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Data directory for conversation storage
DATA_DIR = "data/conversations"
