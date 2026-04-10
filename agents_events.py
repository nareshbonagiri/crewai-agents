"""
Event Management Multi-Agent System
Venue Coordinator, Logistics Manager, Marketing Agent
Direct Ollama API calls with SerperDev and Web Scraping tools
Python 3.9+ compatible
"""

import requests
import json
import re
import os
from typing import Dict, Optional, List
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from config import get_model_config

load_dotenv()


# ============================================================================
# PYDANTIC MODELS - Structured Event Outputs
# ============================================================================

class VenueDetails(BaseModel):
    """Structured venue information"""
    venue_name: str
    address: str
    city: str
    capacity: int
    price_estimate: str = Field(default="TBD", description="~$X/hr format")
    amenities: List[str] = Field(default_factory=list)
    accessibility_features: List[str] = Field(default_factory=list)
    contact_info: str
    website: Optional[str] = None
    rating: Optional[str] = None
    suitability_notes: str


class LogisticsDetails(BaseModel):
    """Structured logistics plan"""
    catering_provider: str
    menu_options: List[str] = Field(default_factory=list)
    equipment_list: List[str] = Field(default_factory=list)
    setup_timeline: str
    breakdown_timeline: str
    transportation_notes: str
    contingency_plan: str
    estimated_cost_range: str = Field(default="TBD", description="$X-$Y format")
    staff_requirements: str = Field(default="TBD", description="~N staff")


class MarketingPlan(BaseModel):
    """Structured marketing strategy"""
    channels: List[str] = Field(default_factory=list)
    target_audience: str
    key_messaging: str
    promotional_timeline: str
    participant_email_template: str
    social_media_strategy: str
    registration_recommendations: str


# ============================================================================
# TOOLS
# ============================================================================

class SerperDevTool:
    """Search the internet using Serper API"""

    name = "serper_search"
    description = "Search the internet for current venue, catering, marketing information"

    def __init__(self):
        self.api_key = os.getenv("SERPERDEV_API_KEY", "")
        self.base_url = "https://google.serper.dev/search"

    def execute(self, query: str) -> str:
        """Execute a web search query"""
        if not self.api_key:
            return "⚠️  SERPERDEV_API_KEY not set in .env. Cannot perform web search."

        try:
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "q": query,
                "num": 5,
            }

            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("organic", [])

                if not results:
                    return f"📍 No results found for: {query}"

                formatted = f"🔍 Search Results for '{query}':\n\n"
                for i, result in enumerate(results[:5], 1):
                    formatted += f"{i}. {result.get('title', 'N/A')}\n"
                    formatted += f"   {result.get('snippet', 'N/A')}\n"
                    formatted += f"   Link: {result.get('link', 'N/A')}\n\n"

                return formatted
            else:
                return f"❌ Serper API error: {response.status_code}"

        except requests.exceptions.Timeout:
            return "⏱️  Serper search timed out"
        except Exception as e:
            return f"❌ Serper search error: {str(e)}"

    def __str__(self) -> str:
        return f"Tool: {self.name} - {self.description}"


class ScrapeWebsiteTool:
    """Extract text content from websites"""

    name = "scrape_website"
    description = "Extract text content from a URL for information gathering"

    def execute(self, url: str) -> str:
        """Scrape website and return cleaned text"""
        if not url:
            return "❌ No URL provided"

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return f"❌ Failed to fetch {url} (status: {response.status_code})"

            # Remove script and style tags
            content = re.sub(r"<script[^>]*>.*?</script>", "", response.text, flags=re.DOTALL)
            content = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL)

            # Remove HTML tags
            content = re.sub(r"<[^>]+>", "", content)

            # Normalize whitespace
            content = re.sub(r"\s+", " ", content).strip()

            # Limit to first 4000 characters
            return content[:4000]

        except requests.exceptions.Timeout:
            return f"⏱️  Timeout while scraping {url}"
        except Exception as e:
            return f"❌ Scrape error: {str(e)}"

    def __str__(self) -> str:
        return f"Tool: {self.name} - {self.description}"


# ============================================================================
# BASE AGENT
# ============================================================================

class SimpleAgent:
    """Base agent using direct Ollama API"""

    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.config = get_model_config()
        self.model = self.config["model"]
        self.ollama_url = "http://localhost:11434"
        self.verbose = self.config["verbose"]

    def print_header(self, text: str):
        """Print formatted header"""
        if self.verbose > 0:
            print(f"\n{'='*70}")
            print(f"  {text}")
            print(f"{'='*70}\n")

    def print_step(self, text: str):
        """Print step indicator"""
        if self.verbose > 0:
            print(f"📍 {text}")

    def print_response(self, label: str, text: str):
        """Print response with ellipsis if too long"""
        if self.verbose > 0:
            display = text if len(text) < 300 else text[:300] + "..."
            print(f"{label}\n{display}")

    def call_ollama(self, prompt: str) -> str:
        """Call Ollama API with the prompt"""
        try:
            if self.verbose > 1:
                print(f"🔄 Calling Ollama ({self.model})...")

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.config["temperature"],
                    "stream": False,
                },
                timeout=300,
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            raise Exception(
                f"❌ Cannot connect to Ollama at {self.ollama_url}\n"
                "Make sure Ollama is running: ollama serve"
            )
        except requests.exceptions.Timeout:
            raise Exception("⏱️  Ollama request timed out")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

class VenueCoordinator(SimpleAgent):
    """Identifies and books appropriate venues"""

    def __init__(self):
        super().__init__(
            role="Senior Venue Coordinator",
            goal="Identify and secure the most appropriate venue for events based on requirements",
            backstory="""You are a senior venue coordinator with 12+ years of experience in event logistics.
You have a deep network of venues worldwide and understand venue selection criteria including
capacity, amenities, location, pricing, accessibility, and suitability for different event types.
You make data-driven venue selections and always verify availability and contact information.""",
        )
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()

    def find_venue(self, event_city: str, event_topic: str) -> VenueDetails:
        """Find and analyze best venue for the event"""
        self.print_header(f"🏢 VENUE COORDINATOR: Finding venue for {event_topic} in {event_city}")

        # Step 1: Search for venues
        self.print_step(f"Searching for {event_topic} venues in {event_city}...")
        search_query = f"best event venues {event_topic} {event_city}"
        search_results = self.search_tool.execute(search_query)

        if self.verbose > 1:
            print(search_results[:200] + "...")

        # Step 2: Attempt to scrape a venue website
        venue_website = None
        if "http" in search_results:
            urls = re.findall(r"https?://[^\s]+", search_results)
            if urls:
                venue_website = urls[0].rstrip(".")
                self.print_step(f"Scraping venue website: {venue_website[:50]}...")
                scraped_content = self.scrape_tool.execute(venue_website)
                if self.verbose > 1:
                    print(f"Scraped {len(scraped_content)} characters")

        # Step 3: Generate venue selection prompt
        prompt = f"""You are {self.backstory}

Based on the search results and any scraped venue information, analyze and select the best venue.

Event Details:
- Topic: {event_topic}
- City: {event_city}

Search Results:
{search_results[:1000]}

{f'Additional Info from Website: {self.scrape_tool.execute(venue_website)[:500]}' if venue_website else ''}

Generate a JSON response with the following structure (MUST be valid JSON):
{{
    "venue_name": "Venue Name",
    "address": "Full address",
    "city": "{event_city}",
    "capacity": 200,
    "price_estimate": "~$X-$Y per hour",
    "amenities": ["WiFi", "Parking", "Catering available", "AV equipment"],
    "accessibility_features": ["Wheelchair accessible", "Accessible parking", "Accessible restrooms"],
    "contact_info": "Phone and email if available",
    "website": "Website URL if found",
    "rating": "4.5/5 or similar if found",
    "suitability_notes": "Why this venue is ideal for {event_topic}"
}}

Return ONLY the JSON, no other text."""

        self.print_step("Generating venue analysis...")
        response = self.call_ollama(prompt)

        # Step 4: Parse JSON response
        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                venue_json = json.loads(json_match.group())
                venue = VenueDetails(**venue_json)
                self.print_response("✅ Venue Selected:", f"{venue.venue_name} ({venue.city})")
                return venue
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback: Create minimal venue from response
        venue = VenueDetails(
            venue_name=f"Recommended {event_topic} Venue",
            address="Location to be confirmed",
            city=event_city,
            capacity=200,
            contact_info="To be determined",
            suitability_notes=response[:200],
        )
        return venue


class LogisticsManager(SimpleAgent):
    """Plans logistics including catering and equipment"""

    def __init__(self):
        super().__init__(
            role="Senior Logistics Manager",
            goal="Plan all logistics aspects of events including catering, equipment, and contingency measures",
            backstory="""You are a senior logistics manager with 10+ years of experience managing large events.
You understand catering requirements, AV equipment needs, setup timelines, staffing requirements,
and contingency planning. You ensure flawless execution of all logistics aspects.""",
        )
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()

    def plan_logistics(
        self, expected_participants: int, tentative_date: str, venue: VenueDetails
    ) -> LogisticsDetails:
        """Plan all logistics for the event"""
        self.print_header(f"📦 LOGISTICS MANAGER: Planning for {expected_participants} participants")

        # Step 1: Search for catering
        self.print_step("Searching for catering options...")
        catering_query = f"catering services {venue.city} {expected_participants} people"
        catering_results = self.search_tool.execute(catering_query)

        # Step 2: Search for equipment
        self.print_step("Searching for equipment rental...")
        equipment_query = f"AV equipment rental event {venue.city}"
        equipment_results = self.search_tool.execute(equipment_query)

        # Step 3: Generate logistics plan
        prompt = f"""You are {self.backstory}

Plan comprehensive logistics for an event with the following details:

Event Details:
- Expected Participants: {expected_participants}
- Date: {tentative_date}
- Venue: {venue.venue_name} ({venue.city})
- Venue Capacity: {venue.capacity}
- Venue Contact: {venue.contact_info}

Catering Search Results:
{catering_results[:500]}

Equipment Search Results:
{equipment_results[:500]}

Generate a detailed JSON logistics plan with this structure (MUST be valid JSON):
{{
    "catering_provider": "Selected catering provider name",
    "menu_options": ["Option 1: Menu description", "Option 2: Menu description"],
    "equipment_list": ["Projector", "Sound system", "Stage lighting", "Registration table setup"],
    "setup_timeline": "Detailed timeline from load-in to event start",
    "breakdown_timeline": "Detailed timeline for post-event breakdown",
    "transportation_notes": "Parking, load dock, and attendee transportation considerations",
    "contingency_plan": "Backup plans for key logistics elements",
    "estimated_cost_range": "$X,000 - $Y,000",
    "staff_requirements": "~N staff members needed for setup, registration, and event management"
}}

Return ONLY the JSON, no other text."""

        self.print_step("Generating logistics plan...")
        response = self.call_ollama(prompt)

        # Step 4: Parse JSON response
        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                logistics_json = json.loads(json_match.group())
                logistics = LogisticsDetails(**logistics_json)
                self.print_response("✅ Logistics Plan Created:", f"Catering: {logistics.catering_provider}")
                return logistics
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback
        logistics = LogisticsDetails(
            catering_provider="To be determined",
            menu_options=["Professional catering menu to be selected"],
            equipment_list=["Standard AV setup", "Registration area", "Seating"],
            setup_timeline="Load-in 2 hours before event start",
            breakdown_timeline="2-3 hours post-event",
            transportation_notes="Accessible parking available",
            contingency_plan=response[:200],
            staff_requirements="~5-10 staff",
        )
        return logistics


class MarketingAgent(SimpleAgent):
    """Creates marketing and communication strategies"""

    def __init__(self):
        super().__init__(
            role="Senior Marketing & Communications Manager",
            goal="Effectively market the event and create compelling communication with participants",
            backstory="""You are a senior marketing and communications manager with 11+ years of experience.
You understand multi-channel marketing, audience engagement, social media strategy, and
participant communication. You create campaigns that drive attendance and participant engagement.""",
        )
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()

    def create_marketing_plan(
        self, event_topic: str, expected_participants: int, event_date: str, venue: VenueDetails
    ) -> MarketingPlan:
        """Create comprehensive marketing strategy"""
        self.print_header(f"📢 MARKETING AGENT: Creating marketing strategy for {event_topic}")

        # Step 1: Research similar events and marketing strategies
        self.print_step("Researching marketing strategies for similar events...")
        marketing_query = f"{event_topic} event marketing strategy {expected_participants} attendees"
        marketing_results = self.search_tool.execute(marketing_query)

        # Step 2: Generate marketing plan
        prompt = f"""You are {self.backstory}

Create a comprehensive marketing and communication plan for an event with these details:

Event Details:
- Topic: {event_topic}
- Expected Participants: {expected_participants}
- Date: {event_date}
- Venue: {venue.venue_name} ({venue.city})
- Location: {venue.address}

Marketing Research Results:
{marketing_results[:500]}

Generate a detailed JSON marketing plan with this structure (MUST be valid JSON):
{{
    "channels": ["LinkedIn", "Twitter/X", "Email", "Event websites", "Industry partnerships"],
    "target_audience": "Detailed description of ideal participants",
    "key_messaging": "Core message for the event",
    "promotional_timeline": "Timeline for marketing activities (e.g., 8 weeks out: press release, 4 weeks: social media push)",
    "participant_email_template": "Professional email template for participant communication",
    "social_media_strategy": "Strategy for different social platforms",
    "registration_recommendations": "Recommended registration process and incentives"
}}

Return ONLY the JSON, no other text."""

        self.print_step("Generating marketing strategy...")
        response = self.call_ollama(prompt)

        # Step 3: Parse JSON response
        try:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                marketing_json = json.loads(json_match.group())
                marketing = MarketingPlan(**marketing_json)
                self.print_response("✅ Marketing Plan Created:", f"Channels: {', '.join(marketing.channels[:3])}")
                return marketing
        except (json.JSONDecodeError, ValueError):
            pass

        # Fallback
        marketing = MarketingPlan(
            channels=["LinkedIn", "Email", "Industry partnerships"],
            target_audience="Professionals interested in " + event_topic,
            key_messaging=response[:100],
            promotional_timeline="8 weeks out: announcement, 4 weeks: social push, 2 weeks: reminder campaign",
            participant_email_template="Professional event email",
            social_media_strategy="Weekly posts on topic, speaker highlights, event updates",
            registration_recommendations="Early bird discounts, group rates, professional development credit",
        )
        return marketing


# ============================================================================
# CREW ORCHESTRATOR
# ============================================================================

class EventCrew:
    """Orchestrates event planning workflow"""

    def __init__(self):
        self.venue_coordinator = VenueCoordinator()
        self.logistics_manager = LogisticsManager()
        self.marketing_agent = MarketingAgent()

    def execute(
        self, event_city: str, event_topic: str, expected_participants: int, tentative_date: str
    ) -> Dict:
        """
        Execute event planning workflow:
        1. Venue Coordinator finds venue (sequential)
        2. Logistics Manager and Marketing Agent run in parallel with venue context
        """
        print("\n🎪 EVENT MANAGEMENT CREW INITIALIZING")
        print("=" * 70)

        try:
            # Phase 1: Sequential - Venue must be selected first
            venue = self.venue_coordinator.find_venue(event_city, event_topic)

            # Phase 2: Parallel execution
            print("\n⚡ PARALLEL PHASE: Logistics and Marketing planning...")
            print("=" * 70)

            with ThreadPoolExecutor(max_workers=2) as executor:
                logistics_future = executor.submit(
                    self.logistics_manager.plan_logistics, expected_participants, tentative_date, venue
                )
                marketing_future = executor.submit(
                    self.marketing_agent.create_marketing_plan, event_topic, expected_participants, tentative_date, venue
                )

                logistics = logistics_future.result()
                marketing = marketing_future.result()

            # Compile results
            result = {
                "event_city": event_city,
                "event_topic": event_topic,
                "expected_participants": expected_participants,
                "event_date": tentative_date,
                "venue": venue.model_dump(),
                "logistics": logistics.model_dump(),
                "marketing": marketing.model_dump(),
            }

            print("\n✅ EVENT PLANNING COMPLETE")
            print("=" * 70)

            return result

        except Exception as e:
            print(f"\n❌ Error in event planning: {str(e)}")
            raise


def create_event_crew() -> EventCrew:
    """Factory function to create event crew"""
    return EventCrew()


# ============================================================================
# TEST / MAIN
# ============================================================================

if __name__ == "__main__":
    # Test scenario: AI & Machine Learning Summit in San Francisco
    crew = create_event_crew()

    result = crew.execute(
        event_city="San Francisco",
        event_topic="AI & Machine Learning Summit",
        expected_participants=200,
        tentative_date="2026-07-20",
    )

    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)

    print("\n🏢 VENUE DETAILS:")
    print(json.dumps(result["venue"], indent=2))

    print("\n📦 LOGISTICS PLAN:")
    print(json.dumps(result["logistics"], indent=2))

    print("\n📢 MARKETING STRATEGY:")
    print(json.dumps(result["marketing"], indent=2))
