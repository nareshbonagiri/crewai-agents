#!/usr/bin/env python3
"""
Event Management System - CLI Interface
Coordinates venue booking, logistics planning, and marketing
"""

import sys
import json
from agents_events import create_event_crew


def print_header(text: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_section(title: str, content: str, max_lines: int = 50):
    """Print a content section with title"""
    print(f"\n{title}")
    print("-" * 70)
    lines = content.split("\n")
    for line in lines[:max_lines]:
        print(line)
    if len(lines) > max_lines:
        print(f"... ({len(lines) - max_lines} more lines)")


def print_usage():
    """Print usage information"""
    print("""
🎪 EVENT MANAGEMENT SYSTEM - Usage
=====================================

Command Line Mode:
  python event_main.py "<event_topic>" "<city>" <participants> "<YYYY-MM-DD>"

  Example:
  python event_main.py "AI Summit" "San Francisco" 200 "2026-07-20"

Interactive Mode:
  python event_main.py

  (You'll be prompted for event details)

Requirements:
  - SERPERDEV_API_KEY in .env
  - Ollama running (ollama serve)
  - Model: llama3.2 or configured MODEL_NAME

Environment Variables:
  MODEL_TYPE=ollama          # Model source: ollama, claude, gemini
  MODEL_NAME=llama3.2:latest # Model name
  MODEL_TEMPERATURE=0.7      # Creativity (0-1)
  VERBOSE_LEVEL=2            # Output detail (0-2)
  SERPERDEV_API_KEY=xxx      # Your Serper API key
""")


def run_event_workflow(event_topic: str, event_city: str, participants: int, event_date: str):
    """Execute event planning workflow"""
    print_header("🎪 EVENT MANAGEMENT SYSTEM")
    print(f"📋 Event: {event_topic}")
    print(f"📍 Location: {event_city}")
    print(f"👥 Expected Participants: {participants}")
    print(f"📅 Date: {event_date}")

    try:
        crew = create_event_crew()
        result = crew.execute(event_city, event_topic, participants, event_date)

        # Display Results
        print_header("📊 EVENT PLANNING RESULTS")

        # Venue Details
        venue = result["venue"]
        venue_text = f"""
Venue Name: {venue.get('venue_name', 'N/A')}
Address: {venue.get('address', 'N/A')}
City: {venue.get('city', 'N/A')}
Capacity: {venue.get('capacity', 'N/A')} people
Price Estimate: {venue.get('price_estimate', 'N/A')}
Contact: {venue.get('contact_info', 'N/A')}
Website: {venue.get('website', 'N/A')}
Rating: {venue.get('rating', 'N/A')}
Amenities: {', '.join(venue.get('amenities', []))}
Accessibility: {', '.join(venue.get('accessibility_features', []))}
Suitability: {venue.get('suitability_notes', 'N/A')[:200]}..."""

        print_section("🏢 VENUE DETAILS", venue_text)

        # Logistics Plan
        logistics = result["logistics"]
        logistics_text = f"""
Catering Provider: {logistics.get('catering_provider', 'N/A')}
Menu Options:
  {chr(10).join('  - ' + opt for opt in logistics.get('menu_options', [])[:3])}
Equipment:
  {chr(10).join('  - ' + eq for eq in logistics.get('equipment_list', [])[:5])}
Setup Timeline: {logistics.get('setup_timeline', 'N/A')}
Breakdown Timeline: {logistics.get('breakdown_timeline', 'N/A')}
Transportation: {logistics.get('transportation_notes', 'N/A')[:150]}...
Staff Requirements: {logistics.get('staff_requirements', 'N/A')}
Cost Estimate: {logistics.get('estimated_cost_range', 'N/A')}
Contingency Plan: {logistics.get('contingency_plan', 'N/A')[:200]}..."""

        print_section("📦 LOGISTICS PLAN", logistics_text)

        # Marketing Strategy
        marketing = result["marketing"]
        marketing_text = f"""
Target Channels: {', '.join(marketing.get('channels', []))}
Target Audience: {marketing.get('target_audience', 'N/A')[:200]}...
Key Messaging: {marketing.get('key_messaging', 'N/A')[:300]}...
Promotional Timeline: {marketing.get('promotional_timeline', 'N/A')[:300]}...
Social Media Strategy: {marketing.get('social_media_strategy', 'N/A')[:300]}...
Registration: {marketing.get('registration_recommendations', 'N/A')[:200]}..."""

        print_section("📢 MARKETING STRATEGY", marketing_text)

        # Full JSON Output
        print_header("📄 COMPLETE PLAN (JSON)")
        print(json.dumps(result, indent=2))

        print_header("✅ Event Planning Complete!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if "Cannot connect to Ollama" in str(e):
            print("\n💡 Troubleshooting:")
            print("   1. Start Ollama: ollama serve")
            print("   2. Pull model: ollama pull llama3.2")
            print("   3. Try again")
        sys.exit(1)


def interactive_mode():
    """Interactive input mode"""
    print_header("🎪 EVENT MANAGEMENT SYSTEM - Interactive Mode")
    print("(Type 'exit' to quit)\n")

    while True:
        try:
            print("\n" + "="*70)
            event_topic = input("📝 Event topic (e.g., 'AI Summit'): ").strip()
            if event_topic.lower() == "exit":
                print("Goodbye!")
                break

            event_city = input("📍 City (e.g., 'San Francisco'): ").strip()
            if event_city.lower() == "exit":
                break

            participants_str = input("👥 Expected participants (e.g., 200): ").strip()
            if participants_str.lower() == "exit":
                break

            try:
                participants = int(participants_str)
            except ValueError:
                print("❌ Please enter a valid number for participants")
                continue

            event_date = input("📅 Event date (YYYY-MM-DD, e.g., 2026-07-20): ").strip()
            if event_date.lower() == "exit":
                break

            # Validate date format
            try:
                from datetime import datetime
                datetime.strptime(event_date, "%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD")
                continue

            # Run workflow
            run_event_workflow(event_topic, event_city, participants, event_date)

            again = input("\n\nPlan another event? (yes/no): ").strip().lower()
            if again != "yes":
                print("\nThank you for using Event Management System!")
                break

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] in ["-h", "--help", "help"]:
            print_usage()
            sys.exit(0)

        if len(sys.argv) == 5:
            event_topic = sys.argv[1]
            event_city = sys.argv[2]
            try:
                participants = int(sys.argv[3])
            except ValueError:
                print("❌ Error: participants must be a number")
                print_usage()
                sys.exit(1)
            event_date = sys.argv[4]

            run_event_workflow(event_topic, event_city, participants, event_date)
        else:
            print("❌ Invalid arguments")
            print_usage()
            sys.exit(1)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
