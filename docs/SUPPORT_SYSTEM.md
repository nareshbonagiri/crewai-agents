# Customer Support Agent System

A production-ready customer support system with **Senior Support Agent** and **Quality Assurance Agent** featuring web scraping and fact-checking capabilities.

## 🎯 Quick Start

```bash
# Basic usage
python support_main.py "How do I reset my password?"

# With documentation reference
python support_main.py "How do I enable 2FA?" "https://learn.microsoft.com/en-us/defender"

# Interactive mode
python support_main.py
```

## 🤖 Agents

### 👤 Customer Support Agent
- **Role**: Senior Support Representative
- **Characteristics**:
  - Friendly and empathetic
  - 10+ years of experience
  - Never delegates tasks
  - Takes full ownership of inquiries
  - Deep product knowledge
- **Capabilities**:
  - Direct customer interaction
  - Web scraping for reference information
  - Context-aware responses
  - Maintains interaction memory

### ✅ Quality Assurance Agent
- **Role**: Support QA Specialist
- **Characteristics**:
  - Fact-checking expert
  - Quality validator
  - Memory management
  - Accuracy focused
- **Capabilities**:
  - Response validation
  - Fact verification
  - Quality scoring
  - Memory tracking
  - Recommendation generation

## 🛠️ Tools

### ScrapeWebsiteTool
Extracts text content from websites for reference and fact-checking.

```python
from agents_support import ScrapeWebsiteTool

tool = ScrapeWebsiteTool()
content = tool.execute("https://learn.microsoft.com/en-us/defender")
```

**Features**:
- HTML cleaning and text extraction
- Automatic tag removal
- Whitespace normalization
- Content limiting (first 4000 chars)
- Error handling for connection issues

### WebsiteSearchTool
Searches website content for specific information relevant to queries.

```python
from agents_support import WebsiteSearchTool

tool = WebsiteSearchTool()
result = tool.execute(
    query="two-factor authentication",
    url="https://learn.microsoft.com/en-us/defender"
)
```

**Features**:
- Query-based content search
- Relevant section extraction
- Sentence matching
- Top results filtering

## 📊 Workflow

### Step 1: Inquiry Resolution
- Customer Support Agent receives inquiry
- Optionally scrapes reference documentation
- Generates friendly, helpful response
- Stores context in memory

### Step 2: Quality Assurance Validation
- QA Agent analyzes support response
- Validates against documentation (if provided)
- Scores response on 6 criteria:
  - **Accuracy** (0-10)
  - **Completeness** (0-10)
  - **Clarity** (0-10)
  - **Tone** (0-10)
  - **Helpfulness** (0-10)
  - **Actionability** (0-10)
- Provides improvement recommendations
- Updates memory with interaction data

## 💾 Memory System

Both agents maintain memory for tracking:

### Support Agent Memory
- Current inquiry
- Customer interactions
- Reference URLs accessed
- Generated responses

### QA Agent Memory
- All interactions
- Quality scores per response
- Common issues tracking
- Improvement patterns

```python
# Access memory
results = crew.execute(inquiry, reference_url)
print(results['support_memory'])
print(results['qa_memory'])
```

## 🔧 Configuration

Configure via `.env` file:

```bash
# Model type: ollama, claude, gemini
MODEL_TYPE=ollama

# Model name
MODEL_NAME=llama3.2:latest

# Temperature: 0 (deterministic) to 1 (creative)
MODEL_TEMPERATURE=0.7

# Verbose level: 0 (minimal), 1 (normal), 2 (verbose)
VERBOSE_LEVEL=2
```

## 📚 Usage Examples

### Basic Support Request
```bash
python support_main.py "How do I update my profile information?"
```

### With Documentation Reference
```bash
python support_main.py \
  "How do I enable two-factor authentication?" \
  "https://learn.microsoft.com/en-us/defender"
```

### In Python Code
```python
from agents_support import create_support_crew

crew = create_support_crew()

result = crew.execute(
    customer_inquiry="How do I reset my password?",
    reference_url="https://help.example.com/security"
)

print(result['support_response'])
print(result['qa_validation'])
```

### Batch Processing
```python
from agents_support import create_support_crew

inquiries = [
    "How do I reset my password?",
    "How do I enable 2FA?",
    "What's the data privacy policy?",
]

crew = create_support_crew()

for inquiry in inquiries:
    result = crew.execute(inquiry)
    print(f"Q: {inquiry}")
    print(f"A: {result['support_response']}\n")
```

## 🧪 Testing

### Test with Microsoft Documentation
```bash
python support_main.py \
  "How do I manage device security?" \
  "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-security/bitlocker/"
```

### Test with Different Models

**TinyLLaMA (fastest)**
```bash
export MODEL_NAME=tinyllama:latest
python support_main.py "How do I reset my password?"
```

**Mistral (balanced)**
```bash
export MODEL_NAME=mistral:latest
python support_main.py "How do I reset my password?"
```

**Claude (most capable)**
```bash
export MODEL_TYPE=claude
export MODEL_NAME=claude-haiku-4-5-20251001
export ANTHROPIC_API_KEY=your-key-here
python support_main.py "How do I reset my password?"
```

## 📊 Output Format

The system returns a comprehensive result dictionary:

```python
{
    "inquiry": str,              # Original customer question
    "support_response": str,     # Support agent's response
    "qa_validation": str,        # QA agent's validation report
    "reference_url": str,        # Used reference URL (if any)
    "support_memory": dict,      # Support agent's memory
    "qa_memory": dict            # QA agent's memory
}
```

### Result Example
```
{
    "inquiry": "How do I enable two-factor authentication?",
    "support_response": "Great question! Two-factor authentication (2FA) adds an extra layer of security to your account...",
    "qa_validation": "ACCURACY: 9/10\nCOMPLETENESS: 8/10\nCLARITY: 9/10\nTONE: 9/10\nHELPFULNESS: 9/10\nACTIONABILITY: 8/10\n\nOverall Quality: 8.7/10",
    "support_memory": {
        "inquiry": "How do I enable two-factor authentication?",
        "response": "..."
    },
    "qa_memory": {
        "interactions": [...],
        "quality_scores": [...],
        "common_issues": {}
    }
}
```

## 🎯 Verbose Output Levels

### Level 0: Minimal
- Only final results
- No intermediate steps

### Level 1: Normal (Default)
- Headers for each agent
- Final responses

### Level 2: Verbose (Recommended)
- All intermediate steps
- API calls information
- Tool execution details
- Memory operations

Set via environment:
```bash
export VERBOSE_LEVEL=2
python support_main.py "your question"
```

## 🔐 Security

- `.env` with API keys is never committed
- Use `.env.example` as template
- Website scraping has error handling
- Timeout protection (10 seconds)
- URL validation and sanitization

## 🚀 Advanced Features

### Custom Tools Integration
```python
from agents_support import CustomerSupportAgent

agent = CustomerSupportAgent()
# Add custom tools
agent.custom_tools = [your_custom_tool]
```

### Memory Analysis
```python
crew = create_support_crew()
result = crew.execute(inquiry)

# Access QA memory
qa_memory = result['qa_memory']
avg_quality = sum(qa_memory['quality_scores']) / len(qa_memory['quality_scores'])
print(f"Average Quality Score: {avg_quality:.1f}/10")
```

### Response Customization
Modify agent backstories and goals in `agents_support.py` for:
- Different tone (formal, casual, technical)
- Specific product knowledge
- Custom validation criteria
- Domain-specific expertise

## 🐛 Troubleshooting

**Connection Error to Ollama**
```bash
# Start Ollama
ollama serve

# In another terminal, pull model
ollama pull llama3.2
```

**Timeout on Large Documents**
- Use smaller reference documents
- Increase timeout in `ScrapeWebsiteTool.execute()`
- Use Claude API for faster responses

**Out of Memory**
```bash
# Use smaller model
export MODEL_NAME=tinyllama:latest
```

## 📈 Performance Notes

| Model | Speed | Quality | Recommendations |
|-------|-------|---------|-----------------|
| TinyLLaMA | ⚡⚡⚡ | ⭐⭐ | Quick testing |
| Neural Chat | ⚡⚡ | ⭐⭐⭐ | Good for chat |
| Mistral | ⚡⚡ | ⭐⭐⭐ | Balanced |
| Llama 3.2 | ⚡ | ⭐⭐⭐⭐ | Best quality |
| Claude | ⚡ | ⭐⭐⭐⭐⭐ | Highest quality |

## 🔗 See Also

- [INTEGRATION.md](INTEGRATION.md) - Integration examples
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [SETUP.md](SETUP.md) - Detailed setup
- [README.md](README.md) - Project overview

## 📝 License

MIT

---

**Ready to support customers?** Start with: `python support_main.py`
