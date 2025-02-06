from pydantic_ai.models.openai import OpenAIModel
import os
from dotenv import load_dotenv

load_dotenv()

# Model configuration
MEDICAL_API_KEY = os.getenv("MEDICAL_API_KEY")
MEDICAL_BASE_URL = os.getenv("MEDICAL_BASE_URL", "https://openrouter.ai/api/v1")
MEDICAL_MODEL = os.getenv("MEDICAL_MODEL", "openai/gpt-4o-mini")

VISION_API_KEY = os.getenv("VISION_API_KEY")
VISION_BASE_URL = os.getenv("VISION_BASE_URL", "https://openrouter.ai/api/v1")
VISION_MODEL = os.getenv("VISION_MODEL", "openai/gpt-4o-mini")


def get_medical_model(model_name: str = MEDICAL_MODEL):
    """Get model for medical analysis"""
    if not MEDICAL_API_KEY:
        raise ValueError("MEDICAL_API_KEY environment variable not set")
    return OpenAIModel(
        model_name=model_name,
        base_url=MEDICAL_BASE_URL,
        api_key=MEDICAL_API_KEY
    )

def get_vision_model(model_name: str = VISION_MODEL):
    """Get model for vision analysis"""
    if not VISION_API_KEY:
        raise ValueError("VISION_API_KEY environment variable not set")
    return OpenAIModel(
        model_name=model_name,
        base_url=VISION_BASE_URL,
        api_key=VISION_API_KEY
    )

# Default models
DEFAULT_MODEL = get_medical_model()
DEFAULT_VISION_MODEL = get_vision_model()
