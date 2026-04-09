"""
CrewAI Agents: Planner, Writer, and Editor
Simple multi-agent system for content creation
"""

from crewai import Agent, Task, Crew
from llm_factory import create_llm
from config import get_model_config, get_model_info


def create_planner_agent():
    """Create Planner Agent - Plans the task"""
    return Agent(
        role="Content Planner",
        goal="Create a detailed plan for the writing task",
        backstory="""You are an expert content strategist who excels at breaking down
        complex topics into manageable sections. You understand audience needs and
        create structured outlines that guide writers to produce high-quality content.""",
        llm=create_llm(),
        verbose=get_model_config()["verbose"],
        allow_delegation=False,
    )


def create_writer_agent():
    """Create Writer Agent - Writes the content"""
    return Agent(
        role="Content Writer",
        goal="Write engaging and informative content based on the plan",
        backstory="""You are a talented writer who transforms plans into well-written,
        engaging content. You have a clear voice, strong research skills, and can adapt
        your writing style to different audiences. You follow the outline provided and
        add depth and clarity to each section.""",
        llm=create_llm(),
        verbose=get_model_config()["verbose"],
        allow_delegation=False,
    )


def create_editor_agent():
    """Create Editor Agent - Reviews and provides feedback"""
    return Agent(
        role="Content Editor",
        goal="Review content for quality, clarity, and alignment with brand guidelines",
        backstory="""You are an experienced editor with a keen eye for detail. You
        ensure content is clear, concise, and aligned with brand guidelines and principles.
        You provide constructive feedback that improves the overall quality of the work
        while preserving the author's voice. You focus on: clarity, consistency, tone,
        factual accuracy, and adherence to style guidelines.""",
        llm=create_llm(),
        verbose=get_model_config()["verbose"],
        allow_delegation=False,
    )


def create_planning_task(topic: str, planner_agent: Agent) -> Task:
    """Create planning task"""
    return Task(
        description=f"""Create a detailed, structured plan for writing about: {topic}

        Your plan should include:
        1. Main sections/chapters
        2. Key points to cover in each section
        3. Target audience and tone
        4. Estimated length for each section
        5. Key takeaways for readers

        Be specific and actionable - this will guide the writer.""",
        agent=planner_agent,
        expected_output="A detailed outline with sections, subsections, and key points",
    )


def create_writing_task(topic: str, writer_agent: Agent) -> Task:
    """Create writing task"""
    return Task(
        description=f"""Write comprehensive content about: {topic}

        Guidelines:
        - Follow the provided plan structure
        - Write clear, engaging prose
        - Include practical examples where relevant
        - Use a consistent, professional tone
        - Target audience: professionals interested in learning
        - Aim for depth and clarity

        Start with an introduction, develop each section thoroughly,
        and conclude with key takeaways.""",
        agent=writer_agent,
        expected_output="Complete, well-written content with all sections fully developed",
    )


def create_editing_task(editor_agent: Agent) -> Task:
    """Create editing task"""
    return Task(
        description="""Review the written content and provide constructive feedback.

        Focus on:
        1. CLARITY: Is the content clear and easy to understand?
        2. CONSISTENCY: Is the tone consistent throughout?
        3. STRUCTURE: Does it follow the planned outline?
        4. ENGAGEMENT: Is it interesting and compelling?
        5. BRAND ALIGNMENT: Does it follow these principles?
           - Professional and authoritative tone
           - Clear, jargon-free explanations
           - Practical and actionable content
           - Inclusive and accessible language

        Provide specific, constructive feedback with suggestions for improvement.
        Highlight what works well and what could be enhanced.""",
        agent=editor_agent,
        expected_output="Detailed editorial feedback with specific suggestions for improvement",
    )


def create_content_crew(topic: str) -> Crew:
    """Create and configure the content creation crew"""

    # Create agents
    planner = create_planner_agent()
    writer = create_writer_agent()
    editor = create_editor_agent()

    # Create tasks
    planning_task = create_planning_task(topic, planner)
    writing_task = create_writing_task(topic, writer)
    editing_task = create_editing_task(editor)

    # Set task dependencies
    writing_task.context = [planning_task]
    editing_task.context = [writing_task]

    # Create crew
    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[planning_task, writing_task, editing_task],
        verbose=get_model_config()["verbose"],
        process=None,  # Sequential process by default
    )

    return crew


if __name__ == "__main__":
    print(f"\n{get_model_info()}\n")
