# Quick Start (5 Minutes)

## 🎯 Goal
Get the CrewAI content creation system running in 5 minutes.

## ⚡ Step-by-Step

### Step 1: Install Dependencies (2 min)

```bash
cd /Users/naresh.bonagiri/Repos/learnagents/crewai-agents
pip install -r requirements.txt
```

### Step 2: Start Ollama (1 min)

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
ollama pull tinyllama
# Wait for download (~2.2GB)
```

### Step 3: Run Your First Topic (2 min)

**Terminal 3:**
```bash
cd /Users/naresh.bonagiri/Repos/learnagents/crewai-agents
python main.py "machine learning basics"
```

## 📊 What You'll See

```
======================================================================
  🚀 Content Creation Workflow
======================================================================

📝 Topic: machine learning basics
🤖 Model: 🐫 Ollama: tinyllama:latest
📊 Verbose Level: 2

----------------------------------------------------------------------
  Creating agents and tasks...
----------------------------------------------------------------------
✅ Crew created successfully

----------------------------------------------------------------------
  Starting workflow execution...
----------------------------------------------------------------------

📍 Step 1️⃣  : PLANNING
📍 Step 2️⃣  : WRITING
📍 Step 3️⃣  : EDITING

This may take a minute or two...

[You'll see detailed agent execution]

======================================================================
✅ WORKFLOW COMPLETED
======================================================================
```

## 🎨 Next: Try Different Topics

```bash
python main.py "python best practices"
python main.py "remote work benefits"
python main.py "artificial intelligence"
```

## 🚀 Next: Use Claude (Better Quality)

1. Get API key from [api.anthropic.com](https://api.anthropic.com)
2. Add to `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   MODEL_TYPE=claude
   MODEL_NAME=claude-haiku-4-5-20251001
   ```
3. Run:
   ```bash
   python main.py "your topic"
   ```

## 🛠️ Next: Customize

Edit `.env` to change:
- `MODEL_NAME` - Use different models
- `VERBOSE_LEVEL` - 0 (quiet), 1 (normal), 2 (verbose)
- `MODEL_TEMPERATURE` - 0 (deterministic), 1 (creative)

## 📚 Next: Learn More

- `python utils.py quickstart` - This guide
- `python utils.py status` - System status
- `python utils.py models` - Available models
- `python example_usage.py 1` - Example code
- `README.md` - Full documentation

## ✅ Troubleshooting

**"Connection refused"**
```bash
# Make sure Ollama is running in Terminal 1
ollama serve
```

**"Model not found"**
```bash
# Make sure you pulled it
ollama list
ollama pull tinyllama
```

**"Out of memory"**
```bash
# Use a smaller model or Claude API
export MODEL_TYPE=claude
python main.py "topic"
```

## 🎉 You're All Set!

You now have a working multi-agent content creation system. 

**Try:**
```bash
python main.py "AI and machine learning"
python main.py "best practices for coding"
python main.py "benefits of automation"
```

Enjoy! 🚀
