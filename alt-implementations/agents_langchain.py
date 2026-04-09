"""
Multi-Agent Content Creation System Using LangChain
Planner → Writer → Editor (Python 3.9 compatible)
"""

from typing import Dict, List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.language_models import BaseChatModel
from llm_factory import create_llm
from config import get_model_config


class ContentAgent:
    """Base agent for content creation tasks"""

    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = create_llm()
        self.verbose = get_model_config()["verbose"]

    def print_header(self, text: str):
        """Print formatted header"""
        if self.verbose > 0:
            print(f"\n{'='*70}")
            print(f"  {text}")
            print(f"{'='*70}\n")

    def print_section(self, text: str):
        """Print formatted section"""
        if self.verbose > 0:
            print(f"\n{'-'*70}")
            print(f"  {text}")
            print(f"{'-'*70}\n")


class PlannerAgent(ContentAgent):
    """Creates detailed outlines and plans"""

    def __init__(self):
        super().__init__(
            role="Content Planner",
            goal="Create a detailed plan for the writing task",
            backstory="""You are an expert content strategist who excels at breaking down
complex topics into manageable sections. You understand audience needs and
create structured outlines that guide writers to produce high-quality content.""",
        )

    def create_plan(self, topic: str) -> str:
        """Create a detailed plan for the topic"""
        self.print_header(f"📋 PLANNER: Planning Content About '{topic}'")

        prompt = PromptTemplate(
            input_variables=["topic", "backstory", "goal"],
            template="""You are a {backstory}

Your goal: {goal}

Create a detailed, structured plan for writing about: {topic}

Your plan should include:
1. Main sections/chapters
2. Key points to cover in each section
3. Target audience and tone
4. Estimated length for each section
5. Key takeaways for readers

Be specific and actionable - this will guide the writer.""",
        )

        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=False)
        result = chain.run(topic=topic, backstory=self.backstory, goal=self.goal)

        if self.verbose > 0:
            print("📋 Plan Created:")
            print(result)

        return result


class WriterAgent(ContentAgent):
    """Writes engaging content based on a plan"""

    def __init__(self):
        super().__init__(
            role="Content Writer",
            goal="Write engaging and informative content based on the plan",
            backstory="""You are a talented writer who transforms plans into well-written,
engaging content. You have a clear voice, strong research skills, and can adapt
your writing style to different audiences. You follow the outline provided and
add depth and clarity to each section.""",
        )

    def write_content(self, topic: str, plan: str) -> str:
        """Write comprehensive content based on the plan"""
        self.print_header(f"✍️  WRITER: Writing Content About '{topic}'")

        prompt = PromptTemplate(
            input_variables=["topic", "plan", "backstory", "goal"],
            template="""You are a {backstory}

Your goal: {goal}

Here is the plan for the content:
{plan}

Now write comprehensive content about: {topic}

Guidelines:
- Follow the provided plan structure
- Write clear, engaging prose
- Include practical examples where relevant
- Use a consistent, professional tone
- Target audience: professionals interested in learning
- Aim for depth and clarity

Start with an introduction, develop each section thoroughly,
and conclude with key takeaways.""",
        )

        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=False)
        result = chain.run(topic=topic, plan=plan, backstory=self.backstory, goal=self.goal)

        if self.verbose > 0:
            print("✍️  Content Written:")
            print(result[:500] + "..." if len(result) > 500 else result)

        return result


class EditorAgent(ContentAgent):
    """Reviews content for quality and brand alignment"""

    def __init__(self):
        super().__init__(
            role="Content Editor",
            goal="Review content for quality, clarity, and alignment with brand guidelines",
            backstory="""You are an experienced editor with a keen eye for detail. You
ensure content is clear, concise, and aligned with brand guidelines and principles.
You provide constructive feedback that improves the overall quality of the work
while preserving the author's voice. You focus on: clarity, consistency, tone,
factual accuracy, and adherence to style guidelines.""",
        )

    def review_content(self, topic: str, content: str) -> str:
        """Review content and provide feedback"""
        self.print_header(f"🔍 EDITOR: Reviewing Content About '{topic}'")

        prompt = PromptTemplate(
            input_variables=["topic", "content", "backstory", "goal"],
            template="""You are a {backstory}

Your goal: {goal}

Review the following content about {topic}:

{content}

Provide constructive feedback focusing on:
1. CLARITY: Is the content clear and easy to understand?
2. CONSISTENCY: Is the tone consistent throughout?
3. STRUCTURE: Is it well-organized and logical?
4. ENGAGEMENT: Is it interesting and compelling?
5. BRAND ALIGNMENT: Does it follow these principles?
   - Professional and authoritative tone
   - Clear, jargon-free explanations
   - Practical and actionable content
   - Inclusive and accessible language

Provide specific, constructive feedback with suggestions for improvement.
Highlight what works well and what could be enhanced.""",
        )

        chain = LLMChain(llm=self.llm, prompt=prompt, verbose=False)
        result = chain.run(topic=topic, content=content, backstory=self.backstory, goal=self.goal)

        if self.verbose > 0:
            print("🔍 Editorial Feedback:")
            print(result)

        return result


class ContentCrew:
    """Manages the workflow of all agents"""

    def __init__(self):
        self.planner = PlannerAgent()
        self.writer = WriterAgent()
        self.editor = EditorAgent()

    def execute(self, topic: str) -> Dict[str, str]:
        """Execute the complete workflow"""
        print(f"\n{'='*70}")
        print(f"  🚀 Content Creation Workflow: {topic}")
        print(f"{'='*70}\n")

        print(f"📊 Verbose Level: {get_model_config()['verbose']}")
        print(f"🤖 Model: {get_model_config()['model']}\n")

        # Step 1: Planning
        print("📍 Step 1️⃣  - PLANNING")
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
        print(f"  ✅ WORKFLOW COMPLETED")
        print(f"{'='*70}\n")

        return results


def create_content_crew() -> ContentCrew:
    """Factory function to create a content crew"""
    return ContentCrew()


if __name__ == "__main__":
    crew = create_content_crew()
    results = crew.execute("machine learning basics")

    print("\n📋 RESULTS SUMMARY")
    print("="*70)
    print(f"\n📌 Plan Length: {len(results['plan'])} characters")
    print(f"📌 Content Length: {len(results['content'])} characters")
    print(f"📌 Feedback Length: {len(results['feedback'])} characters")
