# CrewAI Agents - Multi-Agent Systems

Production-ready multi-agent systems for **content creation** and **customer support** with specialized agents and tools.

## 🎯 Quick Start

### Content Creation System
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Ollama (if using local models)
ollama serve

# 3. In another terminal, pull a model
ollama pull llama3.2

# 4. Run content creation
python main.py "your topic here"
```

### Customer Support System
```bash
# Run support system
python support_main.py "How do I reset my password?"

# Or with documentation reference
python support_main.py "Your question" "https://documentation.url"
```

## 🤖 Available Agent Systems

### Content Creation Agents
- **📋 Planner** - Creates detailed outlines and structure
- **✍️ Writer** - Writes engaging, comprehensive content
- **🔍 Editor** - Reviews for quality and brand alignment

### Customer Support Agents
- **👤 Support Agent** - Senior representative, friendly, never delegates
- **✅ QA Agent** - Validates responses, fact-checks, tracks quality with memory
- **🔧 Tools**: Web scraping, website search, documentation reference

## 🛠️ Configuration

Edit `.env` to choose your model:

```bash
# Local (free, no API keys)
MODEL_TYPE=ollama
MODEL_NAME=llama3.2:latest

# Claude API (requires ANTHROPIC_API_KEY)
MODEL_TYPE=claude
MODEL_NAME=claude-haiku-4-5-20251001
```

Copy `.env.example` to `.env` and add your configuration:
```bash
cp .env.example .env
```

## 📁 Project Structure

```
.
├── main.py                     # Content creation entry point
├── support_main.py             # Customer support entry point
├── agents_simple.py            # Content creation agents
├── agents_support.py           # Support agents + tools
├── config.py                   # Configuration system
├── llm_factory.py              # LLM factory
├── requirements.txt            # Dependencies
├── .env.example                # Configuration template
│
├── docs/                       # Documentation
│   ├── README.md              # This file
│   ├── QUICKSTART.md          # 5-minute quickstart
│   ├── SETUP.md               # Detailed setup guide
│   ├── START_HERE.md          # Getting started guide
│   ├── SUMMARY.md             # System overview
│   ├── INTEGRATION.md         # Content integration examples
│   ├── SUPPORT_SYSTEM.md      # Support system guide
│   └── SUPPORT_INTEGRATION.md # Support integration examples
│
├── examples/                   # Example usage
│   └── example_usage.py       # Content creation examples
│
├── alt-implementations/        # Alternative implementations
│   ├── agents.py             # Original CrewAI version (Python 3.10+)
│   └── agents_langchain.py   # LangChain version
│
└── utils/                      # Utility code
    └── __init__.py
```

## 📚 Documentation

### Content Creation System
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Get running in 5 minutes ⚡
- **[START_HERE.md](docs/START_HERE.md)** - Overview and next steps
- **[SETUP.md](docs/SETUP.md)** - Detailed setup instructions
- **[INTEGRATION.md](docs/INTEGRATION.md)** - Integration examples

### Customer Support System
- **[SUPPORT_SYSTEM.md](docs/SUPPORT_SYSTEM.md)** - Support system guide
- **[SUPPORT_INTEGRATION.md](docs/SUPPORT_INTEGRATION.md)** - 20+ integration examples

## 🚀 Usage Examples

### Content Creation
```bash
# Basic
python main.py "machine learning basics"

# Interactive mode
python main.py

# With verbose output
export VERBOSE_LEVEL=2
python main.py "your topic"

# Switch models
export MODEL_TYPE=claude
python main.py "your topic"
```

### Customer Support
```bash
# Basic support question
python support_main.py "How do I reset my password?"

# With documentation reference
python support_main.py "How do I enable 2FA?" "https://learn.microsoft.com/en-us/defender"

# Interactive mode
python support_main.py

# Verbose output
export VERBOSE_LEVEL=2
python support_main.py "Your question"
```

## 📦 Available Models

### Ollama (Local, Free)
- `tinyllama:latest` - Smallest, fastest
- `neural-chat:latest` - Good for chat
- `mistral:latest` - Good balance
- `llama3.2:latest` - Flexible

### Claude (API)
- `claude-haiku-4-5-20251001` - Fast, cheap
- `claude-sonnet-4-6` - Balanced
- `claude-opus-4-6` - Most capable

### Gemini (Coming Soon)
- `gemini-1.5-flash` - Fast
- `gemini-1.5-pro` - More capable

## ⚙️ Requirements

- Python 3.9+
- Ollama (for local models) or API keys for Claude/Gemini
- ~2GB disk space for a small Ollama model

## 🐛 Troubleshooting

**"Connection refused" error:**
```bash
# Make sure Ollama is running
ollama serve
```

**"Model not found":**
```bash
# Pull the model
ollama pull llama3.2
```

**Out of memory:**
```bash
# Use a smaller model
export MODEL_NAME=tinyllama:latest
```

## 🔐 Security

- `.env` is never committed (see `.gitignore`)
- Copy `.env.example` to `.env` and add your secrets
- API keys stay local

## 🤝 Integration

### Content Creation in Python
```python
from agents_simple import create_content_crew

crew = create_content_crew()
result = crew.execute("your topic")

print(result["plan"])      # The outline
print(result["content"])   # The written content
print(result["feedback"])  # Editorial feedback
```

### Customer Support in Python
```python
from agents_support import create_support_crew

crew = create_support_crew()
result = crew.execute("How do I reset my password?")

print(result["support_response"])  # Support agent response
print(result["qa_validation"])     # QA validation report
print(result["support_memory"])    # Interaction memory
```

See [INTEGRATION.md](docs/INTEGRATION.md) and [SUPPORT_INTEGRATION.md](docs/SUPPORT_INTEGRATION.md) for 30+ examples.

## 📊 Status

✅ **Production Ready**
- **Content Creation System**: Tested with Ollama (llama3.2:latest)
- **Customer Support System**: Tested with web scraping and fact-checking
- Python 3.9+ compatible
- Simple, maintainable code
- Comprehensive documentation (40+ examples)
- Memory tracking and conversation history

## 📝 License

MIT

## 🙋 Support

### Content Creation
- Check [docs/](docs/) for comprehensive guides
- See [INTEGRATION.md](docs/INTEGRATION.md) for 10+ code examples
- Run `python main.py -h` for help

### Customer Support
- See [SUPPORT_SYSTEM.md](docs/SUPPORT_SYSTEM.md) for complete guide
- See [SUPPORT_INTEGRATION.md](docs/SUPPORT_INTEGRATION.md) for 20+ examples
- Run `python support_main.py -h` for help

---

**Ready to get started?** → [QUICKSTART.md](docs/QUICKSTART.md)
