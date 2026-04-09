"""
LLM Factory for Creating Model Instances
Supports Ollama (local), Claude (API), and Gemini (Google)
"""

from typing import Optional, Any
from config import get_model_config, get_model_info, validate_model_config

try:
    from langchain_ollama import ChatOllama
except ImportError:
    ChatOllama = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def create_llm(model_type: Optional[str] = None) -> BaseChatModel:
    """
    Create LLM instance based on configuration

    Args:
        model_type: Optional override for model type ("ollama", "claude", "gemini")

    Returns:
        BaseChatModel instance
    """
    # Validate config
    validate_model_config()

    config = get_model_config()
    model_type = model_type or config["type"]
    model_name = config["model"]
    temperature = config["temperature"]

    if model_type == "ollama":
        print(f"🐫 Loading Ollama: {model_name}")
        return ChatOllama(
            model=model_name,
            temperature=temperature,
            base_url="http://localhost:11434",  # Default Ollama port
        )

    elif model_type == "claude":
        print(f"🤖 Loading Claude: {model_name}")
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
        )

    elif model_type == "gemini":
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "Gemini support requires: pip install langchain-google-genai\n"
                "Also set GOOGLE_API_KEY in .env"
            )
        print(f"✨ Loading Gemini: {model_name}")
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
        )

    else:
        raise ValueError(
            f"Unknown model type: {model_type}. "
            "Use 'ollama', 'claude', or 'gemini'"
        )


def get_llm_info() -> str:
    """Get formatted LLM info"""
    return get_model_info()


if __name__ == "__main__":
    print(f"\n{get_llm_info()}\n")
    llm = create_llm()
    print(f"✅ LLM created successfully: {type(llm).__name__}\n")
