# 🚀 START HERE - CrewAI Agents System

Welcome! You now have a complete **multi-agent content creation system** ready to use.

## 📦 What You Have

```
✅ Planner Agent        📋 Creates detailed outlines
✅ Writer Agent         ✍️  Writes engaging content  
✅ Editor Agent         🔍 Reviews for quality/brand alignment
✅ Flexible Models      🔄 Ollama (local) or Claude (API)
✅ Easy Configuration   ⚙️  Just edit .env to switch models
✅ Production Ready     🚀 Error handling, docs, examples
```

## ⚡ 3-Minute Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Start Ollama (Two Terminals)

**Terminal 1 - Server:**
```bash
ollama serve
```

**Terminal 2 - Download Model:**
```bash
ollama pull tinyllama
```

### 3. Run
```bash
python main.py "machine learning basics"
```

That's it! 🎉

## 📚 Documentation (Pick One)

| Document | Best For |
|----------|----------|
| **QUICKSTART.md** | ⚡ Get running in 5 minutes |
| **README.md** | 📖 Complete user guide |
| **SETUP.md** | 🔧 Detailed setup instructions |
| **INTEGRATION.md** | 🔗 Use in your project |
| **SUMMARY.md** | 📊 System overview |

## 🎯 Common Tasks

### Run your first topic
```bash
python main.py "your topic here"
```

### Switch to Claude (better quality)
```bash
# 1. Edit .env:
#    ANTHROPIC_API_KEY=sk-ant-...
#    MODEL_TYPE=claude
# 2. Run:
python main.py "your topic"
```

### Use a different Ollama model
```bash
export MODEL_NAME=mistral:latest
python main.py "your topic"
```

### See verbose output
```bash
export VERBOSE_LEVEL=2
python main.py "your topic"
```

### Run examples
```bash
python example_usage.py 1
```

### Check system status
```bash
python utils.py status
```

## 🔧 File Guide

### Core Files
- **main.py** - Run this! Entry point for content creation
- **agents.py** - Planner, Writer, Editor agent definitions
- **config.py** - Model configuration (from langgraphagent pattern)
- **llm_factory.py** - Creates LLM instances

### Configuration
- **.env** - Model choice, API keys, verbose level
- **requirements.txt** - Dependencies

### Documentation  
- **README.md** - Full documentation
- **SETUP.md** - Detailed setup guide
- **QUICKSTART.md** - 5-minute quick start
- **INTEGRATION.md** - Integration examples
- **SUMMARY.md** - System overview
- **START_HERE.md** - This file

### Examples & Tools
- **example_usage.py** - Usage examples
- **utils.py** - Utility functions (status, setup, etc.)

## 🤖 Models Available

### Ollama (Free, Local, No API Keys)
```env
MODEL_TYPE=ollama
MODEL_NAME=tinyllama:latest    # ⚡ Smallest (2.2GB)
MODEL_NAME=mistral:latest      # ⭐ Best balanced (4.1GB)
```

### Claude (API, Higher Quality)
```env
MODEL_TYPE=claude
MODEL_NAME=claude-haiku-4-5-20251001        # Fast
MODEL_NAME=claude-sonnet-4-6                # Better
MODEL_NAME=claude-opus-4-6                  # Best
```

### Gemini (Coming Soon)
```env
MODEL_TYPE=gemini
MODEL_NAME=gemini-1.5-flash
```

## 🎨 Customize

### Change Agent Personalities
Edit `agents.py` - modify backstories, goals, roles

### Update Brand Guidelines
Edit task descriptions in `agents.py`

### Add More Agents
Follow the pattern in `agents.py`

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Run `ollama serve` in another terminal |
| "Model not found" | Run `ollama pull tinyllama` |
| "Out of memory" | Use smaller model or switch to Claude |
| "API key invalid" | Check `.env` and API provider |

## 💡 Pro Tips

- Start with **TinyLLama** to test the system (free, fast)
- Use **Claude** for production content (better quality)
- Set **VERBOSE_LEVEL=2** to see all agent actions
- Try different **TEMPERATURE** values for different tones
- **Save results** to files for later review

## 🚀 Next Steps

1. ✅ Read **QUICKSTART.md** (2 min)
2. ✅ Install dependencies (1 min)
3. ✅ Run your first topic (2 min)
4. ✅ Try with Claude (optional, 5 min setup)
5. ✅ Customize for your needs

## 🎓 Learn More

- **Question?** Check README.md
- **Setup help?** Run `python utils.py setup`
- **Code examples?** See example_usage.py
- **Integration?** See INTEGRATION.md

## 📞 Quick Commands Reference

```bash
# Run content creation
python main.py "your topic"

# Interactive mode
python main.py

# See examples
python example_usage.py 1

# Check status
python utils.py status

# See available models
python utils.py models

# Setup guide
python utils.py setup
```

## 🎉 You're Ready!

Everything is set up and working. Pick a topic and start:

```bash
python main.py "artificial intelligence"
```

Enjoy creating! 🚀

---

**Quick links:**
- [5-minute quickstart](QUICKSTART.md)
- [Full setup guide](SETUP.md)  
- [Integration examples](INTEGRATION.md)
- [System overview](SUMMARY.md)
