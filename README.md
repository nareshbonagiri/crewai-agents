# CrewAI Agents - Multi-Agent Content Creation System

A simple, production-ready multi-agent system for content creation with **Planner**, **Writer**, and **Editor** agents.

## 🎯 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Ollama (if using local models)
ollama serve

# 3. In another terminal, pull a model
ollama pull llama3.2

# 4. Run the system
python main.py "your topic here"
```

## 🤖 Agents

- **📋 Planner** - Creates detailed outlines and structure
- **✍️ Writer** - Writes engaging, comprehensive content
- **🔍 Editor** - Reviews for quality and brand alignment

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
├── main.py                 # Entry point - run this!
├── agents_simple.py        # Planner, Writer, Editor agents
├── config.py              # Configuration system
├── llm_factory.py         # LLM factory
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
│
├── docs/                  # Documentation
│   ├── README.md         # This file
│   ├── SETUP.md          # Detailed setup guide
│   ├── QUICKSTART.md     # 5-minute quickstart
│   ├── START_HERE.md     # Getting started guide
│   ├── SUMMARY.md        # System overview
│   └── INTEGRATION.md    # Integration examples
│
├── examples/             # Example usage
│   └── example_usage.py  # Usage patterns
│
├── alt-implementations/  # Alternative implementations
│   ├── agents.py        # Original CrewAI version (needs Python 3.10+)
│   └── agents_langchain.py  # LangChain version
│
└── utils/               # Utility code
    └── __init__.py
```

## 📚 Documentation

Start with one of these:

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Get running in 5 minutes ⚡
- **[START_HERE.md](docs/START_HERE.md)** - Overview and next steps
- **[SETUP.md](docs/SETUP.md)** - Detailed setup instructions
- **[INTEGRATION.md](docs/INTEGRATION.md)** - Integration examples

## 🚀 Usage Examples

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

Use in your Python code:

```python
from agents_simple import create_content_crew

crew = create_content_crew()
result = crew.execute("your topic")

print(result["plan"])      # The outline
print(result["content"])   # The written content
print(result["feedback"])  # Editorial feedback
```

See [INTEGRATION.md](docs/INTEGRATION.md) for 10+ examples.

## 📊 Status

✅ **Production Ready**
- Tested with Ollama (llama3.2:latest)
- Python 3.9+ compatible
- Simple, maintainable code
- Comprehensive documentation

## 📝 License

MIT

## 🙋 Support

- Check [docs/](docs/) for comprehensive guides
- Run `python main.py -h` for help
- See [docs/INTEGRATION.md](docs/INTEGRATION.md) for code examples

---

**Ready to get started?** → [QUICKSTART.md](docs/QUICKSTART.md)
