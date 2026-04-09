"""
Customer Support System - Main Entry Point
Run: python support_main.py "your question" [optional_reference_url]

Examples:
  python support_main.py "How do I reset my password?"
  python support_main.py "How do I enable 2FA?" "https://learn.microsoft.com/en-us/defender"
"""

import sys
from dotenv import load_dotenv
from config import get_model_config, get_model_info, validate_model_config
from agents_support import create_support_crew

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


def run_support_workflow(inquiry: str, reference_url: str = None):
    """Run the support resolution workflow"""

    print_header(f"🎯 Customer Support System")
    print(f"\n👥 Inquiry: {inquiry}")
    if reference_url:
        print(f"📚 Reference: {reference_url}")
    print(f"🤖 Model: {get_model_info()}")
    print(f"📊 Verbose Level: {get_model_config()['verbose']}")

    try:
        print_section("Creating support crew...")
        crew = create_support_crew()
        print("✅ Crew created successfully")

        print_section("Starting support workflow...")
        print("\n📍 Step 1️⃣  : SUPPORT INQUIRY RESOLUTION")
        print("📍 Step 2️⃣  : QUALITY ASSURANCE VALIDATION")
        print("\nProcessing...\n")

        # Run the crew
        result = crew.execute(inquiry, reference_url)

        print_section("✅ SUPPORT WORKFLOW COMPLETED")
        print("\n📋 FINAL RESULTS\n")

        # Display results
        print("=" * 70)
        print("👤 CUSTOMER SUPPORT RESPONSE:")
        print("=" * 70)
        print(result.get("support_response", ""))

        print("\n" + "=" * 70)
        print("✅ QUALITY ASSURANCE VALIDATION:")
        print("=" * 70)
        print(result.get("qa_validation", ""))

        print("\n" + "=" * 70)
        print("💾 SYSTEM MEMORY:")
        print("=" * 70)
        print("\n📌 Support Agent Memory:")
        print(result.get("support_memory", {}))
        print("\n📌 QA Agent Memory:")
        import json

        qa_memory = result.get("qa_memory", {})
        print(json.dumps(qa_memory, indent=2))

        return result

    except Exception as e:
        print_header("❌ ERROR")
        print(f"\n{type(e).__name__}: {str(e)}\n")

        if "connection" in str(e).lower():
            print("💡 TIP: Make sure Ollama is running:")
            print("   ollama serve")
            print("\n   Or check if your model is downloaded:")
            print("   ollama list")
            print("   ollama pull llama3.2  # to download llama3.2")

        sys.exit(1)


def print_usage():
    """Print usage instructions"""
    print_header("💡 Usage Examples")
    print(
        """
    Basic (without reference):
      python support_main.py "How do I reset my password?"
      python support_main.py "How do I enable two-factor authentication?"

    With documentation reference:
      python support_main.py "How do I enable 2FA?" "https://learn.microsoft.com/en-us/defender"
      python support_main.py "Password reset" "https://help.example.com/security"

    With verbose output:
      export VERBOSE_LEVEL=2
      python support_main.py "your question here"

    Switch models:
      export MODEL_TYPE=ollama
      export MODEL_NAME=tinyllama:latest
      python support_main.py "question"

    Available Ollama models:
      - tinyllama:latest   (⚡ Smallest, fastest)
      - neural-chat:latest (🗣️ Good for chat)
      - mistral:latest     (⭐ Good balance)
      - llama3.2:latest    (🎯 More capable)
    """
    )


def main():
    """Main function"""

    # Get inquiry and optional reference from command line
    if len(sys.argv) > 1:
        inquiry = sys.argv[1]
        reference_url = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print_header("📝 Customer Support System")
        inquiry = input("\n👥 Enter your question:\n> ").strip()

        if not inquiry:
            print_usage()
            return

        reference_url_input = (
            input("\n📚 Enter documentation URL (optional, press Enter to skip):\n> ")
            .strip()
        )
        reference_url = reference_url_input if reference_url_input else None

    # Run the workflow
    run_support_workflow(inquiry, reference_url)


if __name__ == "__main__":
    main()
