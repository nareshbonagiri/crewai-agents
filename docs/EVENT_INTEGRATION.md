# Event Management System Integration Examples

Complete examples for integrating the Event Management System into your applications.

## 📦 Basic Integration

### Simple Event Planning
```python
from agents_events import create_event_crew

crew = create_event_crew()

result = crew.execute(
    event_city="San Francisco",
    event_topic="AI & Machine Learning Summit",
    expected_participants=200,
    tentative_date="2026-07-20"
)

print("Venue:", result['venue']['venue_name'])
print("Cost Range:", result['logistics']['estimated_cost_range'])
print("Marketing Channels:", result['marketing']['channels'])
```

### Access Individual Components
```python
from agents_events import create_event_crew

crew = create_event_crew()
result = crew.execute("Austin", "Tech Conference", 150, "2026-08-15")

# Venue details
venue = result['venue']
print(f"Venue: {venue['venue_name']}")
print(f"Capacity: {venue['capacity']} people")
print(f"Contact: {venue['contact_info']}")

# Logistics
logistics = result['logistics']
print(f"Catering: {logistics['catering_provider']}")
print(f"Staff needed: {logistics['staff_requirements']}")

# Marketing
marketing = result['marketing']
print(f"Promotion timeline: {marketing['promotional_timeline']}")
```

## 🔧 Tool Usage

### Using SerperDevTool Directly
```python
from agents_events import SerperDevTool

tool = SerperDevTool()

# Search for venues
results = tool.execute("luxury conference venues Austin Texas")
print(results)

# Search for catering
catering = tool.execute("premium catering services 200 people Austin")
print(catering)
```

### Using ScrapeWebsiteTool Directly
```python
from agents_events import ScrapeWebsiteTool

tool = ScrapeWebsiteTool()

# Get venue details from website
content = tool.execute("https://example-venue.com")
print(f"Scraped {len(content)} characters")

# Extract specific information
if "wheelchair" in content.lower():
    print("✓ Venue has wheelchair accessibility")
if "wifi" in content.lower():
    print("✓ WiFi available")
```

## 🎯 Advanced Usage

### Custom Agent Configuration

Extend agents for specific event types:

```python
from agents_events import VenueCoordinator

class FestivalVenueCoordinator(VenueCoordinator):
    def __init__(self):
        super().__init__()
        self.backstory = """You are an expert in festival and outdoor event venues.
        You understand staging requirements, accessibility for large crowds,
        parking capacity, and weather contingencies. You have 15+ years
        finding perfect outdoor venues for music festivals and large gatherings."""

    def find_festival_venue(self, event_city: str, expected_capacity: int) -> dict:
        # Specialized venue finding for festivals
        return self.find_venue(f"music festival or outdoor concert venue", event_city)

# Usage
coordinator = FestivalVenueCoordinator()
venue = coordinator.find_festival_venue("Denver", 5000)
```

### Extract and Analyze Results

```python
from agents_events import create_event_crew
import json

crew = create_event_crew()
result = crew.execute("New York", "Data Science Conference", 300, "2026-09-15")

# Count amenities
amenities_count = len(result['venue']['amenities'])
print(f"Venue amenities: {amenities_count}")

# List all equipment
equipment = result['logistics']['equipment_list']
print("Equipment needed:")
for item in equipment:
    print(f"  • {item}")

# Marketing channels
channels = result['marketing']['channels']
print(f"Marketing will use {len(channels)} channels: {', '.join(channels)}")
```

## 🌐 Web Integration

### Flask Integration
```python
from flask import Flask, request, jsonify
from agents_events import create_event_crew

app = Flask(__name__)
crew = create_event_crew()

@app.route('/api/plan-event', methods=['POST'])
def plan_event():
    data = request.json
    
    try:
        result = crew.execute(
            event_city=data.get('city'),
            event_topic=data.get('topic'),
            expected_participants=data.get('participants', 100),
            tentative_date=data.get('date')
        )
        
        return jsonify({
            'status': 'success',
            'venue': result['venue'],
            'logistics': result['logistics'],
            'marketing': result['marketing']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Test with curl:
# curl -X POST http://localhost:5000/api/plan-event \
#   -H "Content-Type: application/json" \
#   -d '{"topic":"Tech Summit","city":"SF","participants":200,"date":"2026-07-20"}'
```

### FastAPI Integration
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents_events import create_event_crew

app = FastAPI()

class EventRequest(BaseModel):
    topic: str
    city: str
    participants: int = 100
    date: str  # YYYY-MM-DD

class EventResponse(BaseModel):
    venue: dict
    logistics: dict
    marketing: dict

crew = create_event_crew()

@app.post("/events/plan", response_model=EventResponse)
async def plan_event(request: EventRequest):
    try:
        result = crew.execute(
            event_city=request.city,
            event_topic=request.topic,
            expected_participants=request.participants,
            tentative_date=request.date
        )
        
        return EventResponse(
            venue=result['venue'],
            logistics=result['logistics'],
            marketing=result['marketing']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test with curl:
# curl -X POST http://localhost:8000/events/plan \
#   -H "Content-Type: application/json" \
#   -d '{"topic":"AI Summit","city":"NY","participants":150,"date":"2026-06-15"}'
```

## 💬 Interactive Chat Interface

### Event Planning Chatbot
```python
from agents_events import create_event_crew
import json

def event_planning_chat():
    """Interactive chat for event planning"""
    crew = create_event_crew()
    
    print("\n🎪 Event Planning Assistant")
    print("=" * 50)
    print("I'll help you plan your event!\n")
    
    while True:
        topic = input("Event topic (or 'exit'): ").strip()
        if topic.lower() == 'exit':
            break
        
        city = input("Event city: ").strip()
        if city.lower() == 'exit':
            break
        
        try:
            participants = int(input("Expected participants: ").strip())
        except ValueError:
            print("Invalid number")
            continue
        
        date = input("Event date (YYYY-MM-DD): ").strip()
        if date.lower() == 'exit':
            break
        
        print("\n⏳ Planning your event...")
        
        try:
            result = crew.execute(city, topic, participants, date)
            
            print("\n✅ Event Plan Ready!\n")
            print(f"Venue: {result['venue']['venue_name']}")
            print(f"Capacity: {result['venue']['capacity']} people")
            print(f"Catering: {result['logistics']['catering_provider']}")
            print(f"Marketing: {', '.join(result['marketing']['channels'][:3])}")
            
            details = input("\nSee full details? (yes/no): ").strip().lower()
            if details == 'yes':
                print(json.dumps(result, indent=2))
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    event_planning_chat()
```

## 🔄 Workflow Integration

### Multi-Event Planning Workflow
```python
from agents_events import create_event_crew
from datetime import datetime, timedelta

class EventPlanningWorkflow:
    def __init__(self):
        self.crew = create_event_crew()
        self.planned_events = []
    
    def plan_event(self, topic: str, city: str, participants: int, date: str):
        """Plan an individual event"""
        result = self.crew.execute(city, topic, participants, date)
        
        self.planned_events.append({
            'topic': topic,
            'city': city,
            'date': date,
            'result': result,
            'planned_at': datetime.now().isoformat()
        })
        
        return result
    
    def plan_series(self, events: list):
        """Plan a series of events"""
        for topic, city, participants, date in events:
            print(f"\nPlanning: {topic} in {city}...")
            self.plan_event(topic, city, participants, date)
            print(f"✓ {topic} planned")
    
    def get_summary(self):
        """Get summary of all planned events"""
        return {
            'total_events': len(self.planned_events),
            'total_participants': sum(
                e['result']['expected_participants'] 
                for e in self.planned_events
            ),
            'cities': list(set(e['city'] for e in self.planned_events)),
            'events': [
                {
                    'topic': e['topic'],
                    'venue': e['result']['venue']['venue_name'],
                    'date': e['date']
                }
                for e in self.planned_events
            ]
        }

# Usage
workflow = EventPlanningWorkflow()

events = [
    ("AI Summit", "San Francisco", 200, "2026-07-20"),
    ("Web Dev Bootcamp", "Austin", 100, "2026-08-10"),
    ("Data Science Conf", "New York", 300, "2026-09-15"),
]

workflow.plan_series(events)
print(workflow.get_summary())
```

## 📊 Performance Testing

### Load Testing
```python
from agents_events import create_event_crew
import time

def test_performance():
    """Test planning speed for multiple events"""
    crew = create_event_crew()
    
    test_events = [
        ("Tech Conference", "SF", 100, "2026-07-01"),
        ("AI Workshop", "NYC", 50, "2026-07-15"),
        ("Data Summit", "Austin", 150, "2026-08-01"),
    ]
    
    start_time = time.time()
    
    for topic, city, participants, date in test_events:
        result = crew.execute(city, topic, participants, date)
    
    elapsed = time.time() - start_time
    
    print(f"Planned {len(test_events)} events in {elapsed:.2f} seconds")
    print(f"Average: {elapsed/len(test_events):.2f} seconds per event")

test_performance()
```

### Parallel Event Planning
```python
from agents_events import create_event_crew
from concurrent.futures import ThreadPoolExecutor
import time

def plan_events_parallel(events: list):
    """Plan multiple events in parallel"""
    crew = create_event_crew()
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(crew.execute, city, topic, participants, date)
            for topic, city, participants, date in events
        ]
        
        for future in futures:
            results.append(future.result())
    
    elapsed = time.time() - start_time
    
    print(f"Planned {len(events)} events in parallel in {elapsed:.2f} seconds")
    return results
```

## 🧪 Unit Testing

### Test Event Planning
```python
import pytest
from agents_events import VenueCoordinator, LogisticsManager, MarketingAgent

def test_venue_coordinator():
    coordinator = VenueCoordinator()
    venue = coordinator.find_venue("San Francisco", "Tech Conference")
    
    assert venue.venue_name is not None
    assert venue.city == "San Francisco"
    assert venue.capacity > 0
    assert len(venue.amenities) > 0

def test_logistics_manager():
    manager = LogisticsManager()
    from agents_events import VenueDetails
    
    # Create a mock venue
    venue = VenueDetails(
        venue_name="Convention Center",
        address="123 Main St",
        city="NYC",
        capacity=500,
        contact_info="info@venue.com",
        suitability_notes="Perfect for conferences"
    )
    
    logistics = manager.plan_logistics(200, "2026-07-20", venue)
    
    assert logistics.catering_provider is not None
    assert len(logistics.equipment_list) > 0
    assert "contingency_plan" in logistics.model_dump()

def test_marketing_agent():
    agent = MarketingAgent()
    from agents_events import VenueDetails
    
    venue = VenueDetails(
        venue_name="Convention Center",
        address="123 Main St",
        city="NYC",
        capacity=500,
        contact_info="info@venue.com",
        suitability_notes="Perfect for conferences"
    )
    
    marketing = agent.create_marketing_plan("Tech Summit", 200, "2026-07-20", venue)
    
    assert len(marketing.channels) > 0
    assert len(marketing.target_audience) > 0
    assert marketing.key_messaging is not None

# Run tests
if __name__ == "__main__":
    test_venue_coordinator()
    test_logistics_manager()
    test_marketing_agent()
    print("✓ All tests passed!")
```

## 🔌 Plugin Architecture

### Custom Event Type Handler
```python
from agents_events import EventCrew, VenueCoordinator
from agents_events import VenueDetails, LogisticsDetails, MarketingPlan

class ConferenceEventCrew(EventCrew):
    """Specialized crew for conferences"""
    
    def __init__(self):
        super().__init__()
        self.event_type = "conference"
    
    def execute_conference(self, event_city: str, event_topic: str, 
                          expected_participants: int, tentative_date: str) -> dict:
        """Plan a conference with conference-specific considerations"""
        
        # Add conference-specific search terms
        conference_topic = f"{event_topic} conference"
        
        result = self.execute(event_city, conference_topic, expected_participants, tentative_date)
        
        # Enhance with conference-specific requirements
        result['conference_requirements'] = {
            'breakout_rooms': max(3, expected_participants // 50),
            'networking_space': True,
            'speaker_green_room': True,
            'simultaneous_tracks': max(2, expected_participants // 100),
        }
        
        return result

# Usage
crew = ConferenceEventCrew()
result = crew.execute_conference("Boston", "Machine Learning", 300, "2026-10-15")
print(result['conference_requirements'])
```

## 🚀 Production Deployment

### Docker Integration
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment
ENV MODEL_TYPE=ollama
ENV MODEL_NAME=llama3.2:latest
ENV VERBOSE_LEVEL=1

# Install Ollama (optional)
# RUN curl https://ollama.ai/install.sh | sh

# Run event system
CMD ["python", "event_main.py"]
```

Build and run:
```bash
docker build -t event-planning .
docker run -it event-planning "Tech Conference" "SF" 200 "2026-07-20"
```

### Environment Configuration
```bash
# .env for production
MODEL_TYPE=claude              # Use faster Claude API
MODEL_NAME=claude-haiku-4-5-20251001
MODEL_TEMPERATURE=0.5
VERBOSE_LEVEL=1

SERPERDEV_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## 📈 Result Caching

### Cache Event Plans
```python
from agents_events import create_event_crew
import json
import hashlib

class CachedEventCrew:
    def __init__(self):
        self.crew = create_event_crew()
        self.cache = {}
    
    def _get_cache_key(self, city: str, topic: str, participants: int, date: str) -> str:
        """Generate cache key from parameters"""
        params = f"{city}:{topic}:{participants}:{date}"
        return hashlib.md5(params.encode()).hexdigest()
    
    def execute(self, city: str, topic: str, participants: int, date: str) -> dict:
        """Execute with caching"""
        cache_key = self._get_cache_key(city, topic, participants, date)
        
        if cache_key in self.cache:
            print(f"✓ Using cached plan for {topic}")
            return self.cache[cache_key]
        
        result = self.crew.execute(city, topic, participants, date)
        self.cache[cache_key] = result
        return result
```

---

**Need more examples?** Check [EVENT_SYSTEM.md](EVENT_SYSTEM.md) for detailed documentation.
