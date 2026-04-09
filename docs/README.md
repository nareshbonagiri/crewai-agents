# CrewAI Content Creation System

A simple multi-agent system for content creation with **Planner**, **Writer**, and **Editor** agents.

## 🎯 What It Does

1. **Planner Agent** 📋 - Creates a detailed outline and plan for your topic
2. **Writer Agent** ✍️ - Writes comprehensive content following the plan
3. **Editor Agent** 🔍 - Reviews the content and provides feedback based on brand guidelines

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your Model

Edit `.env` file to choose your model:

```env
# For Ollama (local, recommended for quick start)
MODEL_TYPE=ollama
MODEL_NAME=tinyllama:latest

# For Claude API
# MODEL_TYPE=claude
# MODEL_NAME=claude-haiku-4-5-20251001
# (requires ANTHROPIC_API_KEY in .env)

# For Gemini (Google)
# MODEL_TYPE=gemini
# MODEL_NAME=gemini-1.5-flash
# (requires GOOGLE_API_KEY in .env and langchain-google-genai installed)
```

### 3. Start Ollama (if using local models)

```bash
ollama serve
```

In another terminal, pull the model:

```bash
ollama pull tinyllama  # ~2.2GB - smallest model
ollama pull neural-chat  # ~4.7GB - good for chat
ollama pull phi  # ~2.6GB - efficient
```

List available models:

```bash
ollama list
```

## 🚀 Usage

### Basic Usage

```bash
python main.py "your topic here"
```

### Examples

```bash
# Machine learning topic
python main.py "machine learning basics"

# Coding best practices
python main.py "how to write clean code"

# Any topic you want
python main.py "benefits of remote work"
```

### Interactive Mode

```bash
python main.py
# Then enter your topic when prompted
```

## 📊 Verbose Levels

Control output detail:

```bash
# Minimal output
export VERBOSE_LEVEL=0
python main.py "topic"

# Normal output (default)
export VERBOSE_LEVEL=1
python main.py "topic"

# Verbose output
export VERBOSE_LEVEL=2
python main.py "topic"
```

## 🔄 Switching Models

### Quick Switch

```bash
# Use a different Ollama model
export MODEL_NAME=mistral:latest
python main.py "topic"

# Use Claude (requires API key)
export MODEL_TYPE=claude
export MODEL_NAME=claude-haiku-4-5-20251001
python main.py "topic"
```

### Edit .env File

Open `.env` and change:

```env
MODEL_TYPE=ollama
MODEL_NAME=tinyllama:latest
```

## 📦 Available Models

### Ollama (Local - Recommended for Start)

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| tinyllama | 2.2GB | ⚡⚡⚡ | ⭐ | `ollama pull tinyllama` |
| neural-chat | 4.7GB | ⚡⚡ | ⭐⭐ | `ollama pull neural-chat` |
| phi | 2.6GB | ⚡⚡⚡ | ⭐ | `ollama pull phi` |
| mistral | 4.1GB | ⚡⚡ | ⭐⭐⭐ | `ollama pull mistral` |
| gemma2 | 5.5GB | ⚡⚡ | ⭐⭐⭐ | `ollama pull gemma2` |

### Claude (API - Higher Quality)

```env
MODEL_TYPE=claude
```

Models:
- `claude-haiku-4-5-20251001` - Fast, cheap
- `claude-sonnet-4-6` - Balanced
- `claude-opus-4-6` - Most capable

Requires: `ANTHROPIC_API_KEY` in `.env`

### Gemini (Google - Coming Later)

```env
MODEL_TYPE=gemini
```

Models:
- `gemini-1.5-flash` - Fast
- `gemini-1.5-pro` - More capable
- `gemini-2.0-flash` - Latest

Requires: `GOOGLE_API_KEY` in `.env` and `pip install langchain-google-genai`

## 🛠️ Customization

### Change Agent Personalities

Edit `agents.py` to modify:

- Agent backstories
- Task descriptions
- Brand guidelines in the Editor task

### Add More Agents

Extend the system with more agents (e.g., Researcher, Reviewer) by:

1. Creating new agent in `agents.py`
2. Creating new task in `agents.py`
3. Adding to crew in `create_content_crew()`

## 📋 Project Structure

```
crewai-agents/
├── .env                 # Configuration (model, API keys)
├── config.py           # Model configuration
├── llm_factory.py      # LLM creation logic
├── agents.py           # Planner, Writer, Editor agents
├── main.py             # Entry point
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🐛 Troubleshooting

### "Connection refused" Error

Make sure Ollama is running:

```bash
ollama serve
```

In another terminal, pull the model:

```bash
ollama pull tinyllama
```

### "Model not found" Error

List available models:

```bash
ollama list
```

Download the model:

```bash
ollama pull <model-name>
```

### API Key Issues

For Claude or Gemini, ensure API keys are in `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### Out of Memory

Use a smaller model:

```env
MODEL_NAME=tinyllama:latest  # Smallest
```

Or switch to Claude (uses cloud resources):

```env
MODEL_TYPE=claude
MODEL_NAME=claude-haiku-4-5-20251001
```

## 📚 Learn More

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Models](https://ollama.ai/library)
- [LangChain Documentation](https://python.langchain.com/)

## 📝 Next Steps

1. ✅ Set up `.env` with your model choice
2. ✅ Install Ollama and a model (or add API keys)
3. ✅ Run: `python main.py "your topic"`
4. ✅ Experiment with different topics and models
5. ✅ Customize agents and brand guidelines

Happy creating! 🚀
