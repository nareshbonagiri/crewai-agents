"""
Utility functions for CrewAI agents
"""

import os
import subprocess
from pathlib import Path
from typing import List
from config import OLLAMA_MODELS, CLAUDE_MODELS, GEMINI_MODELS


def check_ollama_running() -> bool:
    """Check if Ollama is running"""
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            timeout=2
        )
        return result.returncode == 0
    except Exception:
        return False


def get_ollama_models() -> List[str]:
    """Get list of available Ollama models"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            models = [line.split()[0] for line in lines if line.strip()]
            return models
    except Exception:
        pass
    return []


def print_model_options():
    """Print available model options"""
    print("\n" + "="*70)
    print("  Available Models")
    print("="*70)

    print("\n🐫 Ollama (Local):")
    print("   Model               Size    Speed   Quality")
    print("   " + "-"*50)
    for name, model in OLLAMA_MODELS.items():
        print(f"   {name:18} [4-5GB]  ⚡⚡⚡   ⭐⭐⭐")

    print("\n🤖 Claude (API):")
    for name, model in CLAUDE_MODELS.items():
        print(f"   {name:18} [API]    ⚡⚡    ⭐⭐⭐⭐⭐")

    print("\n✨ Gemini (Google):")
    for name, model in GEMINI_MODELS.items():
        print(f"   {name:18} [API]    ⚡⚡    ⭐⭐⭐⭐")


def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*70)
    print("  Setup Instructions")
    print("="*70)

    print("""
1. Install dependencies:
   pip install -r requirements.txt

2. Choose your model and configure .env:

   For Ollama (local - no API keys needed):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   a) Start Ollama:
      ollama serve

   b) In another terminal, download a model:
      ollama pull tinyllama    # Smallest (2.2GB)
      ollama pull neural-chat   # Good (4.7GB)
      ollama pull mistral       # Better (4.1GB)

   c) Edit .env:
      MODEL_TYPE=ollama
      MODEL_NAME=tinyllama:latest

   For Claude (requires API key):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   a) Edit .env:
      MODEL_TYPE=claude
      MODEL_NAME=claude-haiku-4-5-20251001
      ANTHROPIC_API_KEY=sk-ant-...

   For Gemini (requires API key):
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   a) Install: pip install langchain-google-genai
   b) Edit .env:
      MODEL_TYPE=gemini
      MODEL_NAME=gemini-1.5-flash
      GOOGLE_API_KEY=...

3. Run content creation:
   python main.py "your topic here"

4. Check examples:
   python example_usage.py 1
    """)


def print_quick_start():
    """Print quick start guide"""
    print("\n" + "="*70)
    print("  🚀 Quick Start (5 minutes)")
    print("="*70)

    print("""
1. Terminal 1 - Start Ollama:
   $ ollama serve

2. Terminal 2 - Download a model:
   $ ollama pull tinyllama
   # Wait for download to complete

3. Terminal 3 - Install and run:
   $ pip install -r requirements.txt
   $ python main.py "machine learning basics"

That's it! The agents will create content for you.

💡 To use Claude instead (faster, better quality):
   - Get API key from api.anthropic.com
   - Add ANTHROPIC_API_KEY to .env
   - Change MODEL_TYPE=claude in .env
   - Run: python main.py "your topic"
    """)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            print("\n🔍 System Status:")
            print(f"  Ollama running: {'✅ Yes' if check_ollama_running() else '❌ No'}")
            print(f"  Available models: {get_ollama_models()}")
        elif cmd == "models":
            print_model_options()
        elif cmd == "setup":
            print_setup_instructions()
        elif cmd == "quickstart":
            print_quick_start()
        else:
            print("Usage: python utils.py [status|models|setup|quickstart]")
    else:
        print("\n📚 Utility Commands:")
        print("  python utils.py status      - Check system status")
        print("  python utils.py models      - Show available models")
        print("  python utils.py setup       - Show setup instructions")
        print("  python utils.py quickstart  - Quick start guide\n")
