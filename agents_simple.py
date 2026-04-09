"""
Simple Multi-Agent Content Creation System
Direct Ollama API calls - No complex dependencies
Python 3.9+ compatible
"""

import requests
import json
from typing import Dict
from config import get_model_config, get_model_info


class SimpleAgent:
    """Base agent using direct Ollama API"""

    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.config = get_model_config()
        self.model = self.config["model"]
        self.ollama_url = "http://localhost:11434"
        self.verbose = self.config["verbose"]

    def print_header(self, text: str):
        """Print formatted header"""
        if self.verbose > 0:
            print(f"\n{'='*70}")
            print(f"  {text}")
            print(f"{'='*70}\n")

    def print_response(self, label: str, text: str):
        """Print response with ellipsis if too long"""
        if self.verbose > 0:
            display = text if len(text) < 300 else text[:300] + "..."
            print(f"{label}")
            print(display)

    def call_ollama(self, prompt: str) -> str:
        """Call Ollama API with the prompt"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.config["temperature"],
                    "stream": False,
                },
                timeout=300,
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            raise Exception(
                f"❌ Cannot connect to Ollama at {self.ollama_url}\n"
                "Make sure Ollama is running: ollama serve"
            )
        except requests.exceptions.Timeout:
            raise Exception("⏱️  Ollama request timed out (model might be slow)")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")


class SimplePlannerAgent(SimpleAgent):
    """Creates detailed content plans"""

    def __init__(self):
        super().__init__(
            role="Content Planner",
            goal="Create a detailed plan for the writing task",
            backstory="""You are an expert content strategist who excels at breaking down
complex topics into manageable sections. You understand audience needs and
create structured outlines that guide writers to produce high-quality content.""",
        )

    def create_plan(self, topic: str) -> str:
        """Create a detailed plan"""
        self.print_header(f"📋 PLANNER: Planning Content About '{topic}'")

        prompt = f"""You are a {self.backstory}

Create a detailed, structured plan for writing about: {topic}

Your plan should include:
1. Main sections/chapters
2. Key points to cover in each section
3. Target audience and tone
4. Estimated length for each section
5. Key takeaways for readers

Be specific and actionable - this will guide the writer."""

        if self.verbose > 1:
            print(f"📝 Sending prompt to Ollama ({self.model})...")

        result = self.call_ollama(prompt)

        if self.verbose > 0:
            self.print_response("📋 Plan Created:\n", result)

        return result


class SimpleWriterAgent(SimpleAgent):
    """Writes engaging content"""

    def __init__(self):
        super().__init__(
            role="Content Writer",
            goal="Write engaging and informative content based on the plan",
            backstory="""You are a talented writer who transforms plans into well-written,
engaging content. You have a clear voice and can adapt your writing style to
different audiences. Follow the outline and add depth and clarity.""",
        )

    def write_content(self, topic: str, plan: str) -> str:
        """Write comprehensive content"""
        self.print_header(f"✍️  WRITER: Writing Content About '{topic}'")

        prompt = f"""You are a {self.backstory}

Here is the plan:
{plan}

Now write comprehensive content about: {topic}

Guidelines:
- Follow the plan structure
- Write clear, engaging prose
- Include practical examples
- Use professional tone
- Target: professionals interested in learning
- Aim for depth and clarity

Start with an introduction, develop each section thoroughly,
and conclude with key takeaways."""

        if self.verbose > 1:
            print(f"📝 Writing content ({self.model})...")

        result = self.call_ollama(prompt)

        if self.verbose > 0:
            display = result[:300] + "..." if len(result) > 300 else result
            self.print_response("✍️  Content Written:\n", display)

        return result


class SimpleEditorAgent(SimpleAgent):
    """Reviews content for quality"""

    def __init__(self):
        super().__init__(
            role="Content Editor",
            goal="Review content for quality, clarity, and brand alignment",
            backstory="""You are an experienced editor with a keen eye for detail.
You ensure content is clear, concise, and aligned with brand guidelines.
You provide constructive feedback that improves overall quality.""",
        )

    def review_content(self, topic: str, content: str) -> str:
        """Review content and provide feedback"""
        self.print_header(f"🔍 EDITOR: Reviewing Content About '{topic}'")

        prompt = f"""You are a {self.backstory}

Review this content about {topic}:

{content}

Provide constructive feedback focusing on:
1. CLARITY: Is it clear and easy to understand?
2. CONSISTENCY: Is the tone consistent?
3. STRUCTURE: Is it well-organized?
4. ENGAGEMENT: Is it interesting?
5. BRAND ALIGNMENT: Does it follow these principles?
   - Professional and authoritative tone
   - Clear, jargon-free explanations
   - Practical and actionable content
   - Inclusive and accessible language

Highlight what works well and suggest improvements."""

        if self.verbose > 1:
            print(f"📝 Reviewing content ({self.model})...")

        result = self.call_ollama(prompt)

        if self.verbose > 0:
            display = result[:300] + "..." if len(result) > 300 else result
            self.print_response("🔍 Editorial Feedback:\n", display)

        return result


class SimpleContentCrew:
    """Manages the workflow"""

    def __init__(self):
        self.planner = SimplePlannerAgent()
        self.writer = SimpleWriterAgent()
        self.editor = SimpleEditorAgent()
        self.config = get_model_config()

    def execute(self, topic: str) -> Dict[str, str]:
        """Execute the complete workflow"""
        print(f"\n{'='*70}")
        print(f"  🚀 Content Creation Workflow")
        print(f"{'='*70}")
        print(f"\n📝 Topic: {topic}")
        print(f"🤖 Model: {get_model_info()}")
        print(f"📊 Verbose: {self.config['verbose']}")
        print(f"🌡️  Temperature: {self.config['temperature']}")

        try:
            # Step 1: Planning
            print("\n📍 Step 1️⃣  - PLANNING")
            plan = self.planner.create_plan(topic)

            # Step 2: Writing
            print("\n📍 Step 2️⃣  - WRITING")
            content = self.writer.write_content(topic, plan)

            # Step 3: Editing
            print("\n📍 Step 3️⃣  - EDITING")
            feedback = self.editor.review_content(topic, content)

            # Results
            results = {"plan": plan, "content": content, "feedback": feedback}

            print(f"\n{'='*70}")
            print(f"  ✅ WORKFLOW COMPLETED SUCCESSFULLY")
            print(f"{'='*70}\n")

            return results

        except Exception as e:
            print(f"\n{'='*70}")
            print(f"  ❌ WORKFLOW FAILED")
            print(f"{'='*70}")
            print(f"\n❌ Error: {str(e)}\n")
            raise


def create_content_crew() -> SimpleContentCrew:
    """Factory function to create a content crew"""
    return SimpleContentCrew()


if __name__ == "__main__":
    crew = create_content_crew()
    results = crew.execute("machine learning basics")

    print("\n📊 RESULTS SUMMARY")
    print("="*70)
    print(f"📌 Plan:     {len(results['plan'])} characters")
    print(f"📌 Content:  {len(results['content'])} characters")
    print(f"📌 Feedback: {len(results['feedback'])} characters")
