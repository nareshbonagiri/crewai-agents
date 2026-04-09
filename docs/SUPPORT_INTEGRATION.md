# Support System Integration Examples

Complete examples for integrating the Customer Support System into your applications.

## 📦 Basic Integration

### Simple Support Request
```python
from agents_support import create_support_crew

# Create crew
crew = create_support_crew()

# Process inquiry
result = crew.execute("How do I reset my password?")

# Access results
print(result['support_response'])
print(result['qa_validation'])
```

### With Documentation Reference
```python
from agents_support import create_support_crew

crew = create_support_crew()

result = crew.execute(
    customer_inquiry="How do I enable two-factor authentication?",
    reference_url="https://learn.microsoft.com/en-us/defender"
)

print("Support Response:")
print(result['support_response'])
print("\nQA Validation:")
print(result['qa_validation'])
```

## 🔧 Batch Processing

Process multiple customer inquiries:

```python
from agents_support import create_support_crew

# List of customer inquiries
inquiries = [
    "How do I reset my password?",
    "How do I enable two-factor authentication?",
    "What data do you collect?",
    "How do I update my profile?",
    "What's your privacy policy?",
]

# Create crew once
crew = create_support_crew()

results = []
for inquiry in inquiries:
    result = crew.execute(inquiry)
    results.append(result)
    print(f"✓ Processed: {inquiry[:50]}...")

# Analyze results
total_quality = sum(
    float(r['qa_validation'].split('\n')[6].split(':')[1].split('/')[0])
    for r in results
    if 'qa_validation' in r
)
avg_quality = total_quality / len(results)
print(f"\nAverage Quality Score: {avg_quality:.1f}/10")
```

## 🧪 Custom Tool Usage

### Using ScrapeWebsiteTool Directly
```python
from agents_support import ScrapeWebsiteTool

tool = ScrapeWebsiteTool()

# Scrape a website
content = tool.execute("https://learn.microsoft.com/en-us/windows")
print(content[:500])

# Use in your own application
if "security" in content.lower():
    print("✓ Security information found")
```

### Using WebsiteSearchTool Directly
```python
from agents_support import WebsiteSearchTool, ScrapeWebsiteTool

search_tool = WebsiteSearchTool()
scrape_tool = ScrapeWebsiteTool()

# Search for specific information
result = search_tool.execute(
    query="password reset procedure",
    url="https://help.example.com/account",
    scrape_tool=scrape_tool
)

print("Found information:")
print(result)
```

## 🎯 Advanced Usage

### Custom Support Agent Configuration

Modify agent personality for different use cases:

```python
from agents_support import CustomerSupportAgent, create_support_crew

# Create custom support agent
class TechnicalSupportAgent(CustomerSupportAgent):
    def __init__(self):
        super().__init__()
        # Override backstory for technical support
        self.backstory = """You are a senior technical support specialist with 15+ years of experience.
        You are knowledgeable, precise, and detail-oriented. You provide technical solutions without 
        oversimplifying complex topics. You're excellent at debugging and troubleshooting."""

# Use in workflow
agent = TechnicalSupportAgent()
response = agent.process_inquiry("How do I configure SSL certificates?")
print(response)
```

### Extract Quality Metrics

```python
from agents_support import create_support_crew
import re

crew = create_support_crew()
result = crew.execute("How do I reset my password?")

# Parse validation report
validation = result['qa_validation']

# Extract scores
scores = {}
metrics = ['Accuracy', 'Completeness', 'Clarity', 'Tone', 'Helpfulness', 'Actionability']

for metric in metrics:
    match = re.search(f'{metric}.*?(\\d+)\\s*/', validation)
    if match:
        scores[metric] = int(match.group(1))

print("Quality Scores:")
for metric, score in scores.items():
    print(f"  {metric}: {score}/10")

# Calculate average
avg = sum(scores.values()) / len(scores) if scores else 0
print(f"\nAverage Quality: {avg:.1f}/10")
```

### Memory-Based Analytics

```python
from agents_support import create_support_crew
import json

crew = create_support_crew()

# Process multiple inquiries and track patterns
inquiries = [
    "How do I reset my password?",
    "How do I reset my account?",
    "I forgot my password",
]

for inquiry in inquiries:
    result = crew.execute(inquiry)
    
    # Access memory
    qa_memory = result['qa_memory']
    
    print(f"Inquiry: {inquiry}")
    print(f"Interactions tracked: {len(qa_memory['interactions'])}")
    print(f"Quality scores: {qa_memory['quality_scores']}")
    print()

# Aggregate memory data
final_memory = crew.qa_agent.memory
print("Final Memory State:")
print(json.dumps(final_memory, indent=2))
```

## 🌐 Web Integration

### Flask Integration
```python
from flask import Flask, request, jsonify
from agents_support import create_support_crew

app = Flask(__name__)
crew = create_support_crew()

@app.route('/api/support', methods=['POST'])
def support_endpoint():
    data = request.json
    inquiry = data.get('inquiry')
    reference_url = data.get('reference_url')
    
    try:
        result = crew.execute(inquiry, reference_url)
        return jsonify({
            'status': 'success',
            'support_response': result['support_response'],
            'qa_validation': result['qa_validation'],
            'quality_score': 7.5  # Extract from validation
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Usage:
# curl -X POST http://localhost:5000/api/support \
#   -H "Content-Type: application/json" \
#   -d '{"inquiry": "How do I reset my password?"}'
```

### FastAPI Integration
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents_support import create_support_crew

app = FastAPI()

class SupportRequest(BaseModel):
    inquiry: str
    reference_url: str = None

class SupportResponse(BaseModel):
    support_response: str
    qa_validation: str
    quality_score: float

crew = create_support_crew()

@app.post("/support", response_model=SupportResponse)
async def handle_support(request: SupportRequest):
    try:
        result = crew.execute(request.inquiry, request.reference_url)
        
        # Extract quality score from validation
        validation = result['qa_validation']
        quality_score = 7.5  # Parse from validation
        
        return SupportResponse(
            support_response=result['support_response'],
            qa_validation=result['qa_validation'],
            quality_score=quality_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Usage:
# curl -X POST http://localhost:8000/support \
#   -H "Content-Type: application/json" \
#   -d '{"inquiry": "How do I reset my password?"}'
```

## 💬 Chat Integration

### Chat-Based Support System
```python
from agents_support import create_support_crew

def support_chat():
    """Interactive chat with support system"""
    crew = create_support_crew()
    
    print("🤖 Support Chat (type 'exit' to quit)")
    print("="*50)
    
    while True:
        inquiry = input("\n👥 Your question: ").strip()
        
        if inquiry.lower() in ['exit', 'quit']:
            print("Thank you for using our support system!")
            break
        
        if not inquiry:
            continue
        
        print("\n⏳ Processing...\n")
        
        try:
            result = crew.execute(inquiry)
            
            print("💬 Support Response:")
            print("-"*50)
            print(result['support_response'][:500] + "...")
            print("\n✅ Quality Assessment:")
            print("-"*50)
            # Extract first line of validation
            validation_lines = result['qa_validation'].split('\n')
            for line in validation_lines[:5]:
                print(line)
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    support_chat()
```

## 🔄 Workflow Integration

### Multi-Step Support Resolution
```python
from agents_support import create_support_crew

class SupportWorkflow:
    def __init__(self):
        self.crew = create_support_crew()
        self.conversation_history = []
    
    def handle_inquiry(self, inquiry: str, reference_url: str = None):
        """Handle inquiry and track conversation"""
        result = self.crew.execute(inquiry, reference_url)
        
        # Store in history
        self.conversation_history.append({
            'inquiry': inquiry,
            'response': result['support_response'],
            'validation': result['qa_validation'],
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
        
        return result
    
    def get_conversation_summary(self):
        """Get summary of all interactions"""
        total_interactions = len(self.conversation_history)
        print(f"Total Interactions: {total_interactions}")
        
        for i, interaction in enumerate(self.conversation_history, 1):
            print(f"\n{i}. Q: {interaction['inquiry']}")
            print(f"   Response length: {len(interaction['response'])} chars")

# Usage
workflow = SupportWorkflow()
workflow.handle_inquiry("How do I reset my password?")
workflow.handle_inquiry("How do I enable 2FA?", "https://learn.microsoft.com/en-us/defender")
workflow.get_conversation_summary()
```

## 📊 Performance Testing

### Load Testing
```python
from agents_support import create_support_crew
import time

def test_performance():
    """Test system performance"""
    crew = create_support_crew()
    
    inquiries = [
        "How do I reset my password?",
        "How do I enable 2FA?",
        "What's your data policy?",
    ]
    
    start_time = time.time()
    
    for inquiry in inquiries:
        result = crew.execute(inquiry)
    
    elapsed = time.time() - start_time
    
    print(f"Processed {len(inquiries)} inquiries in {elapsed:.2f} seconds")
    print(f"Average time per inquiry: {elapsed/len(inquiries):.2f} seconds")

test_performance()
```

## 🧪 Unit Testing

### Test Support Agent
```python
import pytest
from agents_support import CustomerSupportAgent

def test_customer_support_agent():
    agent = CustomerSupportAgent()
    
    # Test basic response
    response = agent.process_inquiry("How do I reset my password?")
    
    assert isinstance(response, str)
    assert len(response) > 0
    assert "password" in response.lower()

def test_qa_validation():
    from agents_support import SupportQAAgent
    
    qa_agent = SupportQAAgent()
    
    inquiry = "How do I reset my password?"
    response = "Click on forgot password..."
    
    validation = qa_agent.validate_response(inquiry, response)
    
    assert 'validation' in validation
    assert isinstance(validation['validation'], str)

# Run tests
if __name__ == "__main__":
    test_customer_support_agent()
    test_qa_validation()
    print("✓ All tests passed!")
```

## 🔌 Plugin Architecture

### Create Custom Tools
```python
from agents_support import CustomerSupportAgent

class CustomDatabaseTool:
    def __init__(self):
        self.name = "customer_database"
        self.description = "Look up customer information"
    
    def execute(self, customer_id: str) -> str:
        # Your custom implementation
        return f"Customer {customer_id} found"

# Extend support agent
class EnhancedSupportAgent(CustomerSupportAgent):
    def __init__(self):
        super().__init__()
        self.database_tool = CustomDatabaseTool()
    
    def process_inquiry_with_customer_context(self, customer_id: str, inquiry: str):
        # Look up customer
        customer_info = self.database_tool.execute(customer_id)
        
        # Create enhanced prompt with customer context
        enhanced_inquiry = f"{inquiry}\n[Customer Context: {customer_info}]"
        
        return self.process_inquiry(enhanced_inquiry)

# Usage
agent = EnhancedSupportAgent()
response = agent.process_inquiry_with_customer_context("CUST_001", "Where's my order?")
print(response)
```

## 🚀 Production Deployment

### Docker Integration
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment
ENV MODEL_TYPE=ollama
ENV MODEL_NAME=llama3.2:latest
ENV VERBOSE_LEVEL=1

# Run support system
CMD ["python", "support_main.py"]
```

Build and run:
```bash
docker build -t support-system .
docker run -p 8000:8000 support-system
```

---

**Need more examples?** Check [SUPPORT_SYSTEM.md](SUPPORT_SYSTEM.md) for detailed documentation.
