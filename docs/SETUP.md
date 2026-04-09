# CrewAI Agents Setup Guide

## 📦 What's Included

A complete multi-agent content creation system with:

- **Planner Agent** - Creates structured outlines and plans
- **Writer Agent** - Writes engaging, detailed content
- **Editor Agent** - Reviews content against brand guidelines
- **Flexible Model Support** - Ollama (local), Claude (API), or Gemini (coming soon)
- **Verbose Output** - Control detail level with `VERBOSE_LEVEL`

## 📋 File Structure

```
crewai-agents/
├── main.py              # Main entry point - run your topics here
├── agents.py            # Planner, Writer, Editor agent definitions
├── config.py            # Model configuration (Ollama, Claude, Gemini)
├── llm_factory.py       # Factory for creating LLM instances
├── utils.py             # Utility functions (status, setup, etc.)
├── example_usage.py     # Example usage patterns
├── .env                 # Configuration (model, API keys, verbose level)
├── requirements.txt     # Python dependencies
├── README.md            # User guide
├── SETUP.md            # This file
└── QUICKSTART.md        # 5-minute quick start
```

## ⚡ Quick Start (Choose One)

### Option 1: Ollama (Local, Recommended for Start)

Best for: Testing, learning, free usage, no API keys needed

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Download tiny model (2.2GB)
ollama pull tinyllama

# Terminal 3: Install and run
pip install -r requirements.txt
python main.py "your topic here"
```

### Option 2: Claude API (Higher Quality)

Best for: Production, better quality output, consistent behavior

```bash
# 1. Get API key from api.anthropic.com
# 2. Add to .env:
#    ANTHROPIC_API_KEY=sk-ant-...
# 3. Edit .env:
#    MODEL_TYPE=claude
#    MODEL_NAME=claude-haiku-4-5-20251001
# 4. Run:
pip install -r requirements.txt
python main.py "your topic here"
```

### Option 3: Gemini (Coming Soon)

Similar setup to Claude but with Google's models.

## 🔧 Configuration

### Model Selection (.env)

```env
# Ollama (Local)
MODEL_TYPE=ollama
MODEL_NAME=tinyllama:latest

# Claude (API)
MODEL_TYPE=claude
MODEL_NAME=claude-haiku-4-5-20251001
ANTHROPIC_API_KEY=sk-ant-...

# Gemini (Google)
MODEL_TYPE=gemini
MODEL_NAME=gemini-1.5-flash
GOOGLE_API_KEY=...
```

### Verbose Level

```env
VERBOSE_LEVEL=0  # Minimal output
VERBOSE_LEVEL=1  # Normal output (default)
VERBOSE_LEVEL=2  # Verbose output (see all agent actions)
```

### Temperature (Creativity)

```env
MODEL_TEMPERATURE=0.0   # Deterministic (recommended)
MODEL_TEMPERATURE=0.7   # Balanced
MODEL_TEMPERATURE=1.0   # Creative
```

## 🚀 Usage Examples

### Basic

```bash
python main.py "machine learning basics"
```

### Interactive Mode

```bash
python main.py
# Enter your topic when prompted
```

### With Custom Verbose Level

```bash
export VERBOSE_LEVEL=2
python main.py "your topic"
```

### Switch Models on the Fly

```bash
# Use Mistral instead of TinyLLama
export MODEL_NAME=mistral:latest
python main.py "your topic"

# Use Claude
export MODEL_TYPE=claude
export MODEL_NAME=claude-haiku-4-5-20251001
python main.py "your topic"
```

### Run Examples

```bash
# Show different example topics
python example_usage.py 1  # Simple topic
python example_usage.py 2  # Technical topic
python example_usage.py 3  # Business topic
python example_usage.py 4  # Config info
```

### Check System Status

```bash
# See if Ollama is running and what models are available
python utils.py status

# Show all available models
python utils.py models

# Show setup instructions
python utils.py setup

# Quick start guide
python utils.py quickstart
```

## 📊 Model Comparison

### Performance & Cost

| Model | Type | Speed | Quality | Cost | Setup |
|-------|------|-------|---------|------|-------|
| TinyLLama | Ollama | ⚡⚡⚡ | ⭐ | Free | Easy |
| Mistral | Ollama | ⚡⚡ | ⭐⭐⭐ | Free | Easy |
| Claude Haiku | API | ⚡⚡ | ⭐⭐⭐⭐ | $$ | Easy |
| Claude Sonnet | API | ⚡ | ⭐⭐⭐⭐⭐ | $$$ | Easy |
| Gemini Flash | API | ⚡⚡⚡ | ⭐⭐⭐⭐ | $ | TBD |

### When to Use Each

**Use TinyLLama** when:
- Testing the system
- Learning CrewAI
- Don't want to use API keys
- Have GPU/CPU available
- Fast iteration needed

**Use Claude** when:
- Production usage
- Higher quality output
- Consistent behavior
- Willing to pay
- Complex topics

**Use Gemini** when:
- Cost-conscious
- Google services integration
- When available (TBD)

## 🛠️ Customization

### Modify Agent Personalities

Edit `agents.py`:

```python
def create_writer_agent():
    return Agent(
        role="Content Writer",
        goal="Your custom goal",
        backstory="Your custom backstory",
        # ... rest of config
    )
```

### Change Brand Guidelines

Edit `agents.py` in `create_editing_task()`:

```python
# Update the BRAND ALIGNMENT section with your principles:
# - Your principle 1
# - Your principle 2
```

### Add More Agents

1. Create agent function in `agents.py`
2. Create task function in `agents.py`
3. Add to crew in `create_content_crew()`

Example:

```python
def create_researcher_agent():
    return Agent(
        role="Researcher",
        goal="Research and validate content",
        # ...
    )
```

## 🐛 Troubleshooting

### "Connection refused" (Ollama not running)

```bash
# Terminal 1:
ollama serve
```

### "Model not found"

```bash
# List available
ollama list

# Download one
ollama pull tinyllama
ollama pull mistral
ollama pull neural-chat
```

### "API key invalid" (Claude/Gemini)

1. Check API key in `.env`
2. Ensure it's valid and not expired
3. Check the provider's dashboard

### Out of Memory

Use a smaller model:

```env
MODEL_NAME=tinyllama:latest  # Smallest
```

Or use Claude (cloud-based):

```env
MODEL_TYPE=claude
```

### "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📚 How It Works

### The Workflow

```
User Input: "your topic"
    ↓
[PLANNER] Creates outline and structure
    ↓
[WRITER] Writes content based on plan
    ↓
[EDITOR] Reviews content and gives feedback
    ↓
Output: Complete content + editorial feedback
```

### Key Features

1. **Sequential Workflow** - Tasks run in order (planning → writing → editing)
2. **Context Passing** - Each agent gets output from previous agents
3. **Verbose Output** - See exactly what each agent is doing
4. **Flexible Models** - Switch between local/API models easily
5. **Brand Alignment** - Editor ensures consistency with guidelines

## 🔄 Switching Between Models

### Without Restarting

```bash
# Just change env var and run
export MODEL_NAME=mistral:latest
python main.py "new topic"
```

### Permanently

Edit `.env`:

```env
MODEL_TYPE=ollama
MODEL_NAME=mistral:latest
```

## 📈 Next Steps

1. ✅ Choose a model (Ollama for start, Claude for production)
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Configure `.env`
4. ✅ Run a topic: `python main.py "your topic"`
5. ✅ Customize agents for your use case
6. ✅ Integrate with your application

## 💡 Tips

- Start with TinyLLama (free, fast) to test
- Use Claude for important content (better quality)
- Adjust temperature for different styles
- Customize editor guidelines for your brand
- Save results to file for review

## 🤝 Integration

To use programmatically:

```python
from agents import create_content_crew

crew = create_content_crew("your topic")
result = crew.kickoff()
print(result)
```

## 📞 Support

- Check README.md for more details
- See example_usage.py for code examples
- Run `python utils.py setup` for setup help
- Check CrewAI docs: https://docs.crewai.com/

Happy creating! 🚀
