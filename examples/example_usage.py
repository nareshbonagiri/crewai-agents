"""
Example usage of the content creation system
Shows how to use the crew programmatically

Run from root: python examples/example_usage.py [1|2|3|4]
"""

import sys
import os

# Add parent directory to path so we can import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from config import get_model_config, get_model_info, validate_model_config
from agents_simple import create_content_crew

# Load environment variables
load_dotenv()

# Validate config
validate_model_config()


def example_1_simple_topic():
    """Example 1: Create content about a simple topic"""
    print("\n" + "="*70)
    print("  EXAMPLE 1: Simple Topic")
    print("="*70)

    topic = "Benefits of remote work"
    print(f"\n📝 Topic: {topic}")
    print(f"🤖 Model: {get_model_info()}")

    crew = create_content_crew()
    result = crew.execute(topic)

    print("\n✅ Result Summary:")
    print(f"  Plan:     {len(result['plan'])} characters")
    print(f"  Content:  {len(result['content'])} characters")
    print(f"  Feedback: {len(result['feedback'])} characters")


def example_2_technical_topic():
    """Example 2: Create technical content"""
    print("\n" + "="*70)
    print("  EXAMPLE 2: Technical Topic")
    print("="*70)

    topic = "Python async/await patterns"
    print(f"\n📝 Topic: {topic}")
    print(f"🤖 Model: {get_model_info()}")

    crew = create_content_crew()
    result = crew.execute(topic)

    print("\n✅ Result Summary:")
    print(f"  Plan:     {len(result['plan'])} characters")
    print(f"  Content:  {len(result['content'])} characters")
    print(f"  Feedback: {len(result['feedback'])} characters")


def example_3_business_topic():
    """Example 3: Create business content"""
    print("\n" + "="*70)
    print("  EXAMPLE 3: Business Topic")
    print("="*70)

    topic = "Strategies for startup growth"
    print(f"\n📝 Topic: {topic}")
    print(f"🤖 Model: {get_model_info()}")

    crew = create_content_crew()
    result = crew.execute(topic)

    print("\n✅ Result Summary:")
    print(f"  Plan:     {len(result['plan'])} characters")
    print(f"  Content:  {len(result['content'])} characters")
    print(f"  Feedback: {len(result['feedback'])} characters")


def example_4_with_custom_config():
    """Example 4: Show how to use different models"""
    print("\n" + "="*70)
    print("  EXAMPLE 4: Model Configuration Info")
    print("="*70)

    config = get_model_config()
    print(f"\nCurrent Configuration:")
    print(f"  Type:        {config['type']}")
    print(f"  Model:       {config['model']}")
    print(f"  Temperature: {config['temperature']}")
    print(f"  Verbose:     {config['verbose']}")

    print("\n💡 To switch models, edit .env:")
    print("""
    # Use different Ollama model
    MODEL_NAME=mistral:latest

    # Use Claude
    MODEL_TYPE=claude
    MODEL_NAME=claude-haiku-4-5-20251001

    # Use Gemini
    MODEL_TYPE=gemini
    MODEL_NAME=gemini-1.5-flash
    """)


if __name__ == "__main__":
    print(f"\n🚀 Content Creation Examples\n")
    print(f"Current Model: {get_model_info()}")

    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num == "1":
            example_1_simple_topic()
        elif example_num == "2":
            example_2_technical_topic()
        elif example_num == "3":
            example_3_business_topic()
        elif example_num == "4":
            example_4_with_custom_config()
        else:
            print("Usage: python example_usage.py [1|2|3|4]")
            print("  1 - Simple topic example")
            print("  2 - Technical topic example")
            print("  3 - Business topic example")
            print("  4 - Show configuration info")
    else:
        print("\nUsage: python example_usage.py [1|2|3|4]\n")
        print("Examples:")
        print("  python example_usage.py 1  # Simple topic")
        print("  python example_usage.py 2  # Technical topic")
        print("  python example_usage.py 3  # Business topic")
        print("  python example_usage.py 4  # Configuration info\n")
