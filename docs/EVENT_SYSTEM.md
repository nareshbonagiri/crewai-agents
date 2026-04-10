# Event Management Multi-Agent System

A production-ready event coordination system with **Venue Coordinator**, **Logistics Manager**, and **Marketing Agent** featuring web search, venue research, and parallel execution capabilities.

## 🎯 Quick Start

```bash
# Basic usage - plan an event
python event_main.py "Tech Conference" "San Francisco" 200 "2026-07-20"

# Interactive mode
python event_main.py

# With verbose output
export VERBOSE_LEVEL=2
python event_main.py "AI Summit" "New York" 150 "2026-06-15"
```

## 🤖 Agents

### 🏢 Venue Coordinator
- **Role**: Senior Venue Coordinator
- **Characteristics**:
  - 12+ years of event logistics experience
  - Deep network of venues worldwide
  - Expert in capacity, amenities, pricing analysis
  - Data-driven venue selection
- **Capabilities**:
  - Web search for venues
  - Website scraping for venue details
  - Venue comparison and selection
  - Contact information research

### 📦 Logistics Manager
- **Role**: Senior Logistics Manager
- **Characteristics**:
  - 10+ years managing large events
  - Expert in catering and AV equipment
  - Understands setup timelines and staffing
  - Contingency planning specialist
- **Capabilities**:
  - Catering provider research
  - Equipment rental coordination
  - Setup timeline planning
  - Contingency planning

### 📢 Marketing Agent
- **Role**: Senior Marketing & Communications Manager
- **Characteristics**:
  - 11+ years of event marketing experience
  - Multi-channel campaign expert
  - Audience engagement specialist
  - Social media strategist
- **Capabilities**:
  - Marketing strategy development
  - Channel selection and planning
  - Participant communication templates
  - Social media campaign design

## 🛠️ Tools

### SerperDevTool
Searches the internet using Google Serper API for current information.

```python
from agents_events import SerperDevTool

tool = SerperDevTool()
results = tool.execute("AI conference venues San Francisco")
```

**Features**:
- Real-time web search via Serper API
- Top 5 organic results with snippets
- Link extraction for website scraping
- Error handling for API failures

**Requirements**:
- `SERPERDEV_API_KEY` in .env

### ScrapeWebsiteTool
Extracts text content from websites for detailed information gathering.

```python
from agents_events import ScrapeWebsiteTool

tool = ScrapeWebsiteTool()
content = tool.execute("https://example-venue.com")
```

**Features**:
- HTML cleaning and text extraction
- Script and style tag removal
- Whitespace normalization
- 4000-character limit for processing

## 📊 Workflow

### Sequential Phase: Venue Selection
1. Venue Coordinator receives event requirements
2. Searches for venues using SerperDev
3. Scrapes top venue website for details
4. Analyzes and selects best venue
5. Returns `VenueDetails` object

### Parallel Phase: Logistics & Marketing
1. **Logistics Manager** (parallel):
   - Searches for catering providers
   - Researches equipment rental
   - Plans setup timeline
   - Creates contingency plan
   - Returns `LogisticsDetails`

2. **Marketing Agent** (parallel):
   - Researches marketing strategies
   - Develops channel strategy
   - Creates participant templates
   - Plans promotional timeline
   - Returns `MarketingPlan`

Both tasks run concurrently using Python's `ThreadPoolExecutor`.

## 📋 Pydantic Models

### VenueDetails
```python
{
    "venue_name": str,
    "address": str,
    "city": str,
    "capacity": int,
    "price_estimate": str,           # e.g., "~$500/hour"
    "amenities": List[str],
    "accessibility_features": List[str],
    "contact_info": str,
    "website": Optional[str],
    "rating": Optional[str],         # e.g., "4.5/5"
    "suitability_notes": str         # Why this venue fits
}
```

### LogisticsDetails
```python
{
    "catering_provider": str,
    "menu_options": List[str],
    "equipment_list": List[str],
    "setup_timeline": str,
    "breakdown_timeline": str,
    "transportation_notes": str,
    "contingency_plan": str,
    "estimated_cost_range": str,     # e.g., "$15,000-$25,000"
    "staff_requirements": str         # e.g., "~10-15 staff"
}
```

### MarketingPlan
```python
{
    "channels": List[str],           # e.g., ["LinkedIn", "Email", "Twitter"]
    "target_audience": str,
    "key_messaging": str,
    "promotional_timeline": str,
    "participant_email_template": str,
    "social_media_strategy": str,
    "registration_recommendations": str
}
```

## 🔧 Configuration

Configure via `.env` file:

```bash
# Model type: ollama, claude, gemini
MODEL_TYPE=ollama

# Model name (depends on type)
MODEL_NAME=llama3.2:latest

# Temperature: 0 (deterministic) to 1 (creative)
MODEL_TEMPERATURE=0.7

# Verbose level: 0 (minimal), 1 (normal), 2 (verbose)
VERBOSE_LEVEL=2

# Serper API key for web search
SERPERDEV_API_KEY=your_api_key_here
```

## 📚 Usage Examples

### Basic Event Planning
```bash
python event_main.py "Tech Conference" "San Francisco" 200 "2026-07-20"
```

### Interactive Mode
```bash
python event_main.py
# Follow prompts to enter event details
```

### In Python Code
```python
from agents_events import create_event_crew

crew = create_event_crew()

result = crew.execute(
    event_city="San Francisco",
    event_topic="AI & Machine Learning Summit",
    expected_participants=200,
    tentative_date="2026-07-20"
)

# Access results
venue = result["venue"]
logistics = result["logistics"]
marketing = result["marketing"]
```

### Batch Event Planning
```python
from agents_events import create_event_crew

events = [
    ("AI Summit", "San Francisco", 200, "2026-07-20"),
    ("Tech Conference", "New York", 150, "2026-06-15"),
    ("Web Dev Workshop", "Austin", 100, "2026-08-10"),
]

crew = create_event_crew()

results = []
for topic, city, participants, date in events:
    result = crew.execute(city, topic, participants, date)
    results.append(result)
    print(f"✓ Planned: {topic}")
```

## 🧪 Testing

### Test Scenario: AI Summit
```bash
python event_main.py "AI & Machine Learning Summit" "San Francisco" 200 "2026-07-20"
```

### Debug with Full Verbose Output
```bash
export VERBOSE_LEVEL=2
python event_main.py "Tech Conference" "Austin" 150 "2026-08-10"
```

### Check Serper API Key
```bash
# Verify in .env
cat .env | grep SERPERDEV_API_KEY

# Test with direct tool
python -c "from agents_events import SerperDevTool; tool = SerperDevTool(); print(tool.execute('test query'))"
```

## 📊 Output Format

The system returns a comprehensive result dictionary:

```python
{
    "event_city": str,
    "event_topic": str,
    "expected_participants": int,
    "event_date": str,
    "venue": {
        "venue_name": str,
        "address": str,
        "city": str,
        "capacity": int,
        "price_estimate": str,
        "amenities": [str],
        "accessibility_features": [str],
        "contact_info": str,
        "website": Optional[str],
        "rating": Optional[str],
        "suitability_notes": str,
    },
    "logistics": {
        "catering_provider": str,
        "menu_options": [str],
        "equipment_list": [str],
        "setup_timeline": str,
        "breakdown_timeline": str,
        "transportation_notes": str,
        "contingency_plan": str,
        "estimated_cost_range": str,
        "staff_requirements": str,
    },
    "marketing": {
        "channels": [str],
        "target_audience": str,
        "key_messaging": str,
        "promotional_timeline": str,
        "participant_email_template": str,
        "social_media_strategy": str,
        "registration_recommendations": str,
    }
}
```

## 🎯 Verbose Output Levels

### Level 0: Minimal
- Only final results (JSON output)
- No intermediate steps

### Level 1: Normal (Default)
- Headers for each phase
- Final results displayed
- Section separators

### Level 2: Verbose (Recommended)
- All intermediate steps shown
- Tool execution details
- Search results preview
- Scraping progress
- API call information

Set via environment:
```bash
export VERBOSE_LEVEL=2
python event_main.py "Tech Conference" "San Francisco" 200 "2026-07-20"
```

## ⚡ Execution Model

### Sequential → Parallel Architecture
1. **Phase 1 (Sequential)**: Venue Coordinator must complete first
   - No logistics or marketing planning can start without venue selection
   - Single thread execution
   - ~2-5 minutes (depending on model speed)

2. **Phase 2 (Parallel)**: Logistics + Marketing run simultaneously
   - Both agents receive the selected venue details
   - Executed in separate threads via `ThreadPoolExecutor`
   - Completes in time of slowest task (~3-7 minutes)

3. **Total Time**: ~5-12 minutes for complete plan
   - Faster with faster models (Claude API: 2-5 minutes)
   - Slower with slower models (TinyLLaMA: 10-15 minutes)

## 🔐 Security

- `.env` with API keys is never committed (see `.gitignore`)
- Use `.env.example` as a template
- Website scraping has error handling
- 10-second timeout protection on HTTP requests
- URL validation and sanitization

## 🐛 Troubleshooting

**"Cannot connect to Ollama" error**
```bash
# Start Ollama
ollama serve

# In another terminal, pull model
ollama pull llama3.2
```

**"Serper API error" or empty search results**
- Verify `SERPERDEV_API_KEY` is set in `.env`
- Check API key is valid at https://serper.dev
- Try a simpler query first

**Timeout errors**
- Use a faster model (Claude API, Gemini)
- Reduce expected participants to simplify search
- Increase timeout in `SerperDevTool.execute()`

**Out of memory**
```bash
# Use a smaller model
export MODEL_NAME=tinyllama:latest
```

## 📈 Performance Notes

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| TinyLLaMA | ⚡⚡⚡ | ⭐⭐ | Free |
| Mistral | ⚡⚡ | ⭐⭐⭐ | Free |
| Llama 3.2 | ⚡ | ⭐⭐⭐⭐ | Free |
| Claude | ⚡⚡ | ⭐⭐⭐⭐⭐ | $ |
| Gemini | ⚡⚡⚡ | ⭐⭐⭐⭐ | $ |

## 🔗 See Also

- [EVENT_INTEGRATION.md](EVENT_INTEGRATION.md) - Integration examples
- [SUPPORT_SYSTEM.md](SUPPORT_SYSTEM.md) - Customer support agents
- [INTEGRATION.md](INTEGRATION.md) - Content creation examples
- [README.md](../README.md) - Project overview

## 📝 License

MIT

---

**Ready to plan events?** Start with: `python event_main.py "Your Event" "City" 100 "2026-07-20"`
