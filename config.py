"""
Model Configuration for CrewAI Agents
Easily switch between Ollama (local), Claude (API), and Gemini (Google)
"""

import os
from typing import Literal, Dict, Any

# Model type options
ModelType = Literal["ollama", "claude", "gemini"]

# ============================================================================
# AVAILABLE MODELS
# ============================================================================

OLLAMA_MODELS = {
    "tinyllama": "tinyllama:latest",      # Smallest, fastest
    "neural-chat": "neural-chat:latest",  # Good for chat
    "phi": "phi:latest",                  # Efficient
    "mistral": "mistral:latest",          # Good balance
    "gemma2": "gemma2:latest",            # Flexible
}

CLAUDE_MODELS = {
    "opus": "claude-opus-4-6",
    "sonnet": "claude-sonnet-4-6",
    "haiku": "claude-haiku-4-5-20251001",
}

GEMINI_MODELS = {
    "flash": "gemini-1.5-flash",
    "pro": "gemini-1.5-pro",
    "gemini2-flash": "gemini-2.0-flash",
}


# ============================================================================
# CONFIGURATION FUNCTIONS
# ============================================================================

def get_model_config() -> Dict[str, Any]:
    """Get model configuration from environment variables"""
    return {
        "type": os.getenv("MODEL_TYPE", "ollama"),
        "model": os.getenv("MODEL_NAME", "tinyllama:latest"),
        "temperature": float(os.getenv("MODEL_TEMPERATURE", "0.7")),
        "verbose": int(os.getenv("VERBOSE_LEVEL", "2")),
    }


def get_model_info() -> str:
    """Get formatted model info string"""
    config = get_model_config()
    config_type = config["type"]
    model_name = config["model"]

    if config_type == "ollama":
        return f"🐫 Ollama: {model_name}"
    elif config_type == "claude":
        return f"🤖 Claude: {model_name}"
    elif config_type == "gemini":
        return f"✨ Gemini: {model_name}"
    else:
        return f"Unknown: {model_name}"


def validate_model_config():
    """Validate that the configured model is available"""
    config = get_model_config()
    config_type = config["type"]
    model_name = config["model"]

    if config_type == "ollama":
        # Ollama models should be available in ollama list
        # We don't validate here as the user should have pulled them
        pass
    elif config_type == "claude":
        # Claude models are validated by the API
        pass
    elif config_type == "gemini":
        # Gemini models are validated by the API
        pass
    else:
        raise ValueError(
            f"Unknown model type: {config_type}. Use 'ollama', 'claude', or 'gemini'"
        )


# ============================================================================
# DISPLAY UTILITIES
# ============================================================================

if __name__ == "__main__":
    print("\n📋 Available Models:")
    print("="*60)
    print("\n🐫 Ollama (Local):")
    for key, value in OLLAMA_MODELS.items():
        print(f"  {key:20} → {value}")

    print("\n🤖 Claude (API):")
    for key, value in CLAUDE_MODELS.items():
        print(f"  {key:20} → {value}")

    print("\n✨ Gemini (Google):")
    for key, value in GEMINI_MODELS.items():
        print(f"  {key:20} → {value}")

    config = get_model_config()
    print(f"\n⚙️  Current Configuration:")
    print("="*60)
    print(f"  Type:        {config['type']}")
    print(f"  Model:       {config['model']}")
    print(f"  Temperature: {config['temperature']}")
    print(f"  Verbose:     {config['verbose']}")
