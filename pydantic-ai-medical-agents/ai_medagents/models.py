from pydantic_ai.models.openai import OpenAIModel
# from pydantic_ai.models.ollama import OllamaModel

import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# OpenRouter models for medical analysis
def get_medical_model(model_name: str = "openai/gpt-4o-mini"):
    api_key = OPENROUTER_API_KEY
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    return OpenAIModel(
        model_name, base_url="https://openrouter.ai/api/v1", api_key=api_key
    )


# # Ollama models for local processing
# def get_local_model(model_name: str = "deepseek-r1"):
#     """Get Ollama model for local processing"""
#     return OllamaModel(
#         model_name=model_name,
#         base_url="http://10.0.0.82:11434/v1"
#     )

# Default models
DEFAULT_MODEL = get_medical_model()
# LOCAL_MODEL = get_local_model()
