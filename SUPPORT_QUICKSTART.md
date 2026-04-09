# Customer Support System - Quick Reference

## 🚀 Getting Started (2 minutes)

### Installation
```bash
# Already installed? Skip this!
pip install -r requirements.txt

# Start Ollama
ollama serve
```

### Run Support System

```bash
# Ask a simple question
python3 support_main.py "How do I reset my password?"

# Ask with documentation reference
python3 support_main.py "How do I enable 2FA?" "https://learn.microsoft.com/en-us/defender"

# Interactive mode
python3 support_main.py
```

## 📊 What You Get

### Support Response
- Friendly, empathetic support from senior agent
- Addresses customer query directly
- Offers clear next steps
- Maintains conversation context

### Quality Assurance Validation
```
Accuracy:      [0-10]
Completeness:  [0-10]
Clarity:       [0-10]
Tone:          [0-10]
Helpfulness:   [0-10]
Actionability: [0-10]
Overall Score: [0-10]

+ Key Strengths
+ Areas for Improvement
+ Enhancement Recommendations
```

### Memory Tracking
- Support agent maintains inquiry context
- QA agent tracks quality metrics
- Full interaction history available
- JSON-serializable for logging

## 🔧 Tools Available

### ScrapeWebsiteTool
Extracts text from any URL for fact-checking
```python
from agents_support import ScrapeWebsiteTool
tool = ScrapeWebsiteTool()
content = tool.execute("https://example.com")
```

### WebsiteSearchTool
Searches website for relevant information
```python
from agents_support import WebsiteSearchTool
tool = WebsiteSearchTool()
result = tool.execute(
    query="reset password",
    url="https://help.example.com"
)
```

## 💻 Use in Python

### Simple Usage
```python
from agents_support import create_support_crew

crew = create_support_crew()
result = crew.execute("Your question here")

print(result['support_response'])
print(result['qa_validation'])
```

### With Documentation
```python
crew = create_support_crew()
result = crew.execute(
    "How do I enable 2FA?",
    "https://learn.microsoft.com/en-us/defender"
)
```

### Access Memory
```python
print(result['support_memory'])
print(result['qa_memory'])
```

## 📚 Test URLs

Great documentation sources for testing:

- **Microsoft Security**: https://learn.microsoft.com/en-us/windows/security/
- **Microsoft Defender**: https://learn.microsoft.com/en-us/defender
- **GitHub Help**: https://docs.github.com/en/
- **AWS Documentation**: https://docs.aws.amazon.com/
- **Google Cloud**: https://cloud.google.com/docs

## ⚙️ Configuration

Edit `.env` file:
```bash
# Model type: ollama, claude, gemini
MODEL_TYPE=ollama
MODEL_NAME=llama3.2:latest
MODEL_TEMPERATURE=0.7
VERBOSE_LEVEL=2  # Set to 2 for detailed output
```

## 🧪 Examples to Try

### Security-Related
```bash
python3 support_main.py \
  "How do I enable two-factor authentication?" \
  "https://learn.microsoft.com/en-us/windows/security/"
```

### Account Management
```bash
python3 support_main.py \
  "How do I update my profile information?" \
  "https://learn.microsoft.com/en-us/defender"
```

### Data Privacy
```bash
python3 support_main.py \
  "What is your data privacy policy?"
```

## 🎯 System Architecture

```
User Query
    ↓
Support Agent (👤)
├─ Analyzes inquiry
├─ Scrapes reference docs (if provided)
├─ Generates friendly response
└─ Stores in memory
    ↓
QA Agent (✅)
├─ Validates accuracy
├─ Fact-checks against docs
├─ Scores on 6 metrics
└─ Updates interaction memory
    ↓
Final Output
├─ Support response
├─ QA validation report
└─ Memory data
```

## 📊 Output Levels

### VERBOSE_LEVEL=0 (Minimal)
- Final results only
- No intermediate output

### VERBOSE_LEVEL=1 (Normal)
- Headers for each step
- Final responses shown

### VERBOSE_LEVEL=2 (Recommended)
- All intermediate steps
- API call information
- Tool execution details
- Memory operations

```bash
export VERBOSE_LEVEL=2
python3 support_main.py "Your question"
```

## 🔍 Debug Tips

### Check Ollama
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# List downloaded models
ollama list

# Download model if needed
ollama pull llama3.2
```

### Verbose All Details
```bash
export VERBOSE_LEVEL=2
python3 support_main.py "test question" | tee output.log
```

### Test a Specific Tool
```python
from agents_support import ScrapeWebsiteTool

tool = ScrapeWebsiteTool()
result = tool.execute("https://learn.microsoft.com/en-us/windows")
print(f"Scraped {len(result)} characters")
```

## 📖 Documentation

- **[SUPPORT_SYSTEM.md](docs/SUPPORT_SYSTEM.md)** - Complete system guide
- **[SUPPORT_INTEGRATION.md](docs/SUPPORT_INTEGRATION.md)** - 20+ code examples
- **[agents_support.py](agents_support.py)** - Source code with docstrings

## 🚀 Next Steps

1. Run basic test:
   ```bash
   python3 support_main.py "How do I reset my password?"
   ```

2. Try with documentation:
   ```bash
   python3 support_main.py "Your question" "https://docs.url"
   ```

3. Explore integration examples:
   ```bash
   # Check SUPPORT_INTEGRATION.md for Flask, FastAPI, batch processing, etc.
   ```

4. Customize for your needs:
   - Edit agent backstories in `agents_support.py`
   - Add custom tools
   - Integrate with your application

## ⚡ Quick Command Reference

```bash
# Basic
python3 support_main.py "question"

# With docs
python3 support_main.py "question" "url"

# Interactive
python3 support_main.py

# Verbose
export VERBOSE_LEVEL=2 && python3 support_main.py "question"

# Different model
export MODEL_NAME=tinyllama:latest && python3 support_main.py "question"

# Claude (if configured)
export MODEL_TYPE=claude && python3 support_main.py "question"
```

---

**Need more?** See [SUPPORT_SYSTEM.md](docs/SUPPORT_SYSTEM.md) for comprehensive documentation.

**Questions?** Check [SUPPORT_INTEGRATION.md](docs/SUPPORT_INTEGRATION.md) for 20+ examples.
