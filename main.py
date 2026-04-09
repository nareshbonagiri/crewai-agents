"""
Main entry point for Content Creation Agents
Run content creation workflow: Planning → Writing → Editing
Using simple Ollama API calls - Python 3.9+ compatible
"""

import sys
from dotenv import load_dotenv
from config import get_model_config, get_model_info, validate_model_config
from agents_simple import create_content_crew

# Load environment variables
load_dotenv()

# Validate config
validate_model_config()


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_section(text: str):
    """Print a section divider"""
    print("\n" + "-" * 70)
    print(f"  {text}")
    print("-" * 70)


def run_content_creation(topic: str):
    """Run the content creation workflow"""

    print_header(f"🚀 Content Creation Workflow")
    print(f"\n📝 Topic: {topic}")
    print(f"🤖 Model: {get_model_info()}")
    print(f"📊 Verbose Level: {get_model_config()['verbose']}")

    try:
        print_section("Creating agents and tasks...")
        crew = create_content_crew()
        print("✅ Crew created successfully")

        print_section("Starting workflow execution...")
        print("\n📍 Step 1️⃣  : PLANNING")
        print("📍 Step 2️⃣  : WRITING")
        print("📍 Step 3️⃣  : EDITING")
        print("\nThis may take a minute or two...\n")

        # Run the crew
        result = crew.execute(topic)

        print_section("✅ WORKFLOW COMPLETED")
        print("\n📋 FINAL RESULTS\n")

        # Handle both dict and string results
        if isinstance(result, dict):
            print("=" * 70)
            print("📋 PLAN:")
            print("=" * 70)
            print(result.get("plan", ""))

            print("\n" + "=" * 70)
            print("✍️  CONTENT:")
            print("=" * 70)
            print(result.get("content", ""))

            print("\n" + "=" * 70)
            print("🔍 EDITORIAL FEEDBACK:")
            print("=" * 70)
            print(result.get("feedback", ""))
        else:
            print(result)

        return result

    except Exception as e:
        print_header("❌ ERROR")
        print(f"\n{type(e).__name__}: {str(e)}\n")

        if "connection" in str(e).lower():
            print("💡 TIP: Make sure Ollama is running:")
            print("   ollama serve")
            print("\n   Or check if your model is downloaded:")
            print("   ollama list")
            print("   ollama pull tinyllama  # to download tinyllama")

        sys.exit(1)


def print_usage():
    """Print usage instructions"""
    print_header("💡 Usage Examples")
    print("""
    Basic:
      python main.py "machine learning basics"
      python main.py "how to write better code"

    With verbose output:
      export VERBOSE_LEVEL=2
      python main.py "your topic here"

    Switch models (edit .env or use):
      export MODEL_TYPE=ollama
      export MODEL_NAME=tinyllama:latest
      python main.py "topic"

      # For Claude (requires ANTHROPIC_API_KEY):
      export MODEL_TYPE=claude
      export MODEL_NAME=claude-haiku-4-5-20251001
      python main.py "topic"

    Available Ollama models:
      - tinyllama:latest   (⚡ Smallest, fastest)
      - neural-chat:latest (🗣️ Good for chat)
      - phi:latest         (⚙️ Efficient)
      - mistral:latest     (⭐ Good balance)
      - gemma2:latest      (🎯 Flexible)
    """)


def main():
    """Main function"""

    # Get topic from command line or prompt
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        print_header("📝 Content Creation with CrewAI")
        topic = input("\n🎯 Enter the topic you want to write about:\n> ").strip()

        if not topic:
            print_usage()
            return

    # Run the workflow
    run_content_creation(topic)


if __name__ == "__main__":
    main()
