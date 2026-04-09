# Integration Guide

## 🔗 How to Integrate CrewAI Agents into Your Project

### 1. Standalone Script

Use as a command-line tool:

```bash
python main.py "your topic"
```

### 2. Python Package Import

```python
from agents import create_content_crew

def create_article(topic: str) -> str:
    """Create article about a topic using CrewAI agents"""
    crew = create_content_crew(topic)
    result = crew.kickoff()
    return result

# Usage
article = create_article("machine learning")
print(article)
```

### 3. Within Larger Application

```python
# In your application
from crewai_agents.agents import create_content_crew
from crewai_agents.config import get_model_info, get_model_config

def generate_blog_post(title: str, topic: str) -> dict:
    """Generate blog post content"""
    print(f"Generating blog post: {title}")
    print(f"Using model: {get_model_info()}")
    
    crew = create_content_crew(topic)
    result = crew.kickoff()
    
    return {
        "title": title,
        "topic": topic,
        "content": result,
        "model": get_model_config()["model"]
    }
```

### 4. Web API Integration

```python
# Flask example
from flask import Flask, request, jsonify
from agents import create_content_crew

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic')
    
    try:
        crew = create_content_crew(topic)
        result = crew.kickoff()
        return jsonify({"status": "success", "content": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### 5. Async Integration

```python
import asyncio
from agents import create_content_crew

async def generate_multiple_topics(topics: list) -> dict:
    """Generate content for multiple topics"""
    results = {}
    
    for topic in topics:
        crew = create_content_crew(topic)
        result = crew.kickoff()
        results[topic] = result
        
        # Add delay between requests to avoid overload
        await asyncio.sleep(1)
    
    return results

# Usage
topics = ["AI basics", "Python tips", "Web development"]
results = asyncio.run(generate_multiple_topics(topics))
```

### 6. Model Configuration in Application

```python
import os
from dotenv import load_dotenv

# Load from shared .env
load_dotenv()

def initialize_agents(model_type: str = None, model_name: str = None):
    """Initialize agents with specific model"""
    if model_type:
        os.environ["MODEL_TYPE"] = model_type
    if model_name:
        os.environ["MODEL_NAME"] = model_name
    
    from agents import create_content_crew
    return create_content_crew

# Usage
init_agents = initialize_agents(
    model_type="claude",
    model_name="claude-haiku-4-5-20251001"
)
crew = init_agents("your topic")
```

### 7. Custom Agent Configuration

```python
from agents import create_planner_agent, create_writer_agent, create_editor_agent
from crewai import Crew, Task

def create_custom_crew(topic: str, custom_guidelines: str) -> Crew:
    """Create crew with custom brand guidelines"""
    
    planner = create_planner_agent()
    writer = create_writer_agent()
    editor = create_editor_agent()
    
    # Custom tasks
    planning = Task(
        description=f"Plan content about: {topic}",
        agent=planner
    )
    
    writing = Task(
        description=f"Write about: {topic}",
        agent=writer
    )
    
    editing = Task(
        description=f"Review for: {custom_guidelines}",
        agent=editor
    )
    
    writing.context = [planning]
    editing.context = [writing]
    
    return Crew(
        agents=[planner, writer, editor],
        tasks=[planning, writing, editing],
        verbose=2
    )

# Usage with custom guidelines
crew = create_custom_crew(
    topic="Python best practices",
    custom_guidelines="Ensure code examples are included"
)
result = crew.kickoff()
```

### 8. Save Results to File

```python
from agents import create_content_crew
from pathlib import Path
from datetime import datetime

def create_and_save(topic: str, output_dir: str = "outputs"):
    """Create content and save to file"""
    
    # Create crew and run
    crew = create_content_crew(topic)
    result = crew.kickoff()
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{topic.replace(' ', '_')}_{timestamp}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# {topic}\n\n")
        f.write(result)
    
    print(f"✅ Saved to: {filename}")
    return filename

# Usage
create_and_save("machine learning")
```

### 9. Error Handling

```python
from agents import create_content_crew
from config import validate_model_config

def safe_create_content(topic: str, fallback_model: str = "claude"):
    """Create content with error handling and fallback"""
    
    try:
        validate_model_config()
        crew = create_content_crew(topic)
        return crew.kickoff()
    
    except ConnectionError as e:
        print(f"⚠️  Connection error: {e}")
        print(f"Falling back to {fallback_model}...")
        
        # Switch to fallback model
        import os
        os.environ["MODEL_TYPE"] = "claude"
        
        crew = create_content_crew(topic)
        return crew.kickoff()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

# Usage
try:
    content = safe_create_content("your topic")
except Exception as e:
    print(f"Failed completely: {e}")
```

### 10. Batch Processing

```python
from agents import create_content_crew
from typing import List
import json

def process_batch(topics: List[str], output_file: str = "results.json"):
    """Process multiple topics and save results"""
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "topics": {}
    }
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] Processing: {topic}")
        
        try:
            crew = create_content_crew(topic)
            content = crew.kickoff()
            
            results["topics"][topic] = {
                "status": "success",
                "content": content
            }
        except Exception as e:
            results["topics"][topic] = {
                "status": "error",
                "error": str(e)
            }
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    return results

# Usage
topics = [
    "machine learning",
    "web development",
    "cloud computing"
]
results = process_batch(topics)
```

## 🔧 Configuration for Different Environments

### Development (Ollama)
```env
MODEL_TYPE=ollama
MODEL_NAME=tinyllama:latest
VERBOSE_LEVEL=2
```

### Testing (Claude)
```env
MODEL_TYPE=claude
MODEL_NAME=claude-haiku-4-5-20251001
VERBOSE_LEVEL=1
```

### Production (Claude)
```env
MODEL_TYPE=claude
MODEL_NAME=claude-sonnet-4-6
VERBOSE_LEVEL=0
```

### CI/CD Integration
```bash
# In your CI/CD pipeline
pip install -r requirements.txt
export MODEL_TYPE=claude
export ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
python main.py "test topic"
```

## 📦 Packaging for Distribution

### Create a Package

```
your_project/
├── setup.py
├── crewai_agents/
│   ├── __init__.py
│   ├── agents.py
│   ├── config.py
│   ├── llm_factory.py
│   └── utils.py
└── requirements.txt
```

### setup.py
```python
from setuptools import setup

setup(
    name="crewai-agents",
    version="0.1.0",
    packages=["crewai_agents"],
    install_requires=[
        "crewai==0.50.6",
        "langchain==0.1.20",
        "langchain-ollama==0.1.1",
        "langchain-anthropic==0.1.17",
        "python-dotenv==1.0.0",
    ],
    author="Your Name",
    description="Multi-agent content creation system",
)
```

### Install Locally
```bash
pip install -e .
```

### Use in Other Projects
```python
from crewai_agents.agents import create_content_crew
```

## 🚀 Deployment Options

### 1. Standalone Server
```bash
python main.py "topic"  # Run on demand
```

### 2. Background Task Worker
```python
# Using Celery
from celery import Celery
from agents import create_content_crew

app = Celery('tasks')

@app.task
def generate_content(topic):
    crew = create_content_crew(topic)
    return crew.kickoff()

# Queue task
generate_content.delay("machine learning")
```

### 3. Docker Container
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### 4. Kubernetes Job
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: crewai-content-gen
spec:
  template:
    spec:
      containers:
      - name: crewai
        image: crewai-agents:latest
        env:
        - name: MODEL_TYPE
          value: "claude"
```

## 💡 Best Practices

1. **Always validate config** before running
2. **Use try/except** for production
3. **Log all activities** for debugging
4. **Cache results** to avoid redundant processing
5. **Monitor model costs** when using APIs
6. **Test with small topics** first
7. **Use environment variables** for secrets
8. **Version your agents** for reproducibility

## 🔄 Integration Workflow

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Validate Config     │ (config.py)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Create LLM          │ (llm_factory.py)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Create Agents       │ (agents.py)
└────────┬────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Execute Crew                          │
│  ├─ Plan (Planner Agent)             │
│  ├─ Write (Writer Agent)             │
│  └─ Edit (Editor Agent)              │
└────────┬─────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Return Results  │
└─────────────────┘
```

---

For more details, see README.md, SETUP.md, or QUICKSTART.md
