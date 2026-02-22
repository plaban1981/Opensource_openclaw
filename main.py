"""
OpenClaw - Agentic Framework using CrewAI with LLM (ollama/minimax-m2.5:cloud)

A multi-agent AI system for research, coding, review, and execution tasks.
"""

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS
from dotenv import load_dotenv

load_dotenv()


# ============== Tools ==============

@tool("DuckDuckGo Search")
def ddg_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.
    Use this tool to find information, news, and resources.

    Args:
        query: The search query string

    Returns:
        Search results as a string
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        return str(list(results))


@tool("Web Content Fetcher")
def fetch_web_content(url: str) -> str:
    """
    Fetch content from a web URL.

    Args:
        url: The URL to fetch content from

    Returns:
        The web page content as a string
    """
    import requests
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text[:5000]  # Limit to first 5000 chars
    except Exception as e:
        return f"Error fetching content: {str(e)}"


@tool("Code Executor")
def execute_code(code: str, language: str = "python") -> str:
    """
    Execute code and return the output.

    Args:
        code: The code to execute
        language: The programming language (python, javascript, bash)

    Returns:
        The execution output
    """
    import subprocess
    import tempfile
    import os

    extensions = {"python": ".py", "javascript": ".js", "bash": ".sh"}

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=extensions.get(language, ".txt"),
        delete=False,
    ) as f:
        f.write(code)
        temp_file = f.name

    try:
        if language == "python":
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30,
            )
        elif language == "javascript":
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=30,
            )
        elif language == "bash":
            result = subprocess.run(
                ["bash", temp_file],
                capture_output=True,
                text=True,
                timeout=30,
            )
        else:
            return f"Unsupported language: {language}"

        output = result.stdout if result.stdout else result.stderr
        return output if output else "Code executed successfully (no output)"
    except subprocess.TimeoutExpired:
        return "Execution timed out"
    except Exception as e:
        return f"Execution error: {str(e)}"
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@tool("File Writer")
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.

    Args:
        file_path: The path to write the file to
        content: The content to write

    Returns:
        Success or error message
    """
    try:
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool("File Reader")
def read_file(file_path: str) -> str:
    """
    Read content from a file.

    Args:
        file_path: The path to read the file from

    Returns:
        The file content
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


# ============== LLM Setup ==============

def get_llm(
    model: str = "ollama/ollama/minimax-m2.5:cloud",
    temperature: float = 0.7,
) -> LLM:
    """
    Create an LLM LLM instance for CrewAI.

    Args:
        model: The model name (default: ollama/ollama/minimax-m2.5:cloud)
        temperature: Sampling temperature

    Returns:
        LLM instance
    """
    return LLM(
        model=model,
        temperature=temperature,
        base_url="http://localhost:11434",
    )


# ============== Agent Definitions ==============

def create_researcher_agent(llm: LLM) -> Agent:
    """Create the Researcher Agent."""
    return Agent(
        role="Senior Research Analyst",
        goal="Research and gather comprehensive information on any topic",
        backstory=(
            "You are a senior research analyst with expertise in finding "
            "and synthesizing information from various sources. You excel "
            "at deep research and presenting findings in a clear, organized manner."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[ddg_search, fetch_web_content],
    )


def create_coder_agent(llm: LLM) -> Agent:
    """Create the Coder Agent."""
    return Agent(
        role="Senior Software Engineer",
        goal="Write high-quality, efficient, and well-documented code",
        backstory=(
            "You are a senior software engineer with extensive experience in "
            "multiple programming languages. You write clean, maintainable code "
            "following best practices and design patterns."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[write_file, read_file, execute_code],
    )


def create_reviewer_agent(llm: LLM) -> Agent:
    """Create the Reviewer Agent."""
    return Agent(
        role="Code Reviewer",
        goal="Review code for bugs, security issues, and best practices",
        backstory=(
            "You are an expert code reviewer with deep knowledge of software "
            "security, performance, and best practices. You provide constructive "
            "feedback and identify potential issues in code."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[read_file, ddg_search],
    )


def create_executor_agent(llm: LLM) -> Agent:
    """Create the Executor Agent."""
    return Agent(
        role="DevOps Engineer",
        goal="Execute tasks, run code, and manage project execution",
        backstory=(
            "You are a DevOps engineer with expertise in running and managing "
            "software execution. You handle deployment, testing, and automation tasks."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[execute_code, ddg_search],
    )


# ============== Task Definitions ==============

def create_research_task(agent: Agent, topic: str) -> Task:
    """Create a research task."""
    return Task(
        description=f"Research the following topic comprehensively: {topic}\n\n"
                   "Provide detailed findings with sources.",
        agent=agent,
        expected_output=(
            "A comprehensive research report with key findings, "
            "sources, and insights"
        ),
    )


def create_coding_task(agent: Agent, task_description: str) -> Task:
    """Create a coding task."""
    return Task(
        description=f"Complete the following coding task: {task_description}\n\n"
                   "Write clean, well-documented code.",
        agent=agent,
        expected_output=(
            "Complete, functional code with proper documentation"
        ),
    )


def create_review_task(agent: Agent, code_path: str) -> Task:
    """Create a code review task."""
    return Task(
        description=f"Review the code at: {code_path}\n\n"
                   "Check for bugs, security issues, and best practices.",
        agent=agent,
        expected_output=(
            "A detailed code review with findings and recommendations"
        ),
    )


def create_execution_task(agent: Agent, task: str) -> Task:
    """Create an execution task."""
    return Task(
        description=f"Execute the following task: {task}",
        agent=agent,
        expected_output=(
            "Execution results with output and status"
        ),
    )


# ============== Crew Factory ==============

def create_crew(
    task: str,
    model: str = "ollama/minimax-m2.5:cloud",
    process: Process = Process.hierarchical,
) -> Crew:
    """
    Create a complete crew with all agents.

    Args:
        task: The task to accomplish
        model: The LLM model to use
        process: The process type (hierarchical or sequential)

    Returns:
        Configured Crew instance
    """
    llm = get_llm(model=model)

    # Create agents
    researcher = create_researcher_agent(llm)
    coder = create_coder_agent(llm)
    reviewer = create_reviewer_agent(llm)
    executor = create_executor_agent(llm)

    # Create tasks
    research_task = create_research_task(researcher, task)
    coding_task = create_coding_task(coder, task)
    review_task = create_review_task(reviewer, ".")
    execution_task = create_execution_task(executor, task)

    # Create crew
    crew = Crew(
        agents=[researcher, coder, reviewer, executor],
        tasks=[research_task, coding_task, review_task, execution_task],
        process=process,
        verbose=True,
        memory=True,
    )

    return crew


def create_simple_crew(
    task: str,
    model: str = "ollama/minimax-m2.5:cloud",
) -> Crew:
    """
    Create a simplified crew with Researcher and Coder agents.

    Args:
        task: The task to accomplish
        model: The LLM model to use

    Returns:
        Configured Crew instance
    """
    llm = get_llm(model=model)

    # Create agents
    researcher = create_researcher_agent(llm)
    coder = create_coder_agent(llm)

    # Create tasks
    research_task = create_research_task(researcher, task)
    coding_task = create_coding_task(coder, task)

    # Create crew
    crew = Crew(
        agents=[researcher, coder],
        tasks=[research_task, coding_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


# ============== Main Execution ==============

def main():
    """Main entry point for OpenClaw."""
    print("=" * 60)
    print("OpenClaw - Agentic Framework")
    print("Using CrewAI with LLM (ollama/minimax-m2.5:cloud)")
    print("=" * 60)

    # Example task
    task = "Create a simple REST API with Flask"

    print(f"\nTask: {task}")
    print("\nStarting crew execution...\n")

    # Create and run crew
    crew = create_simple_crew(task)
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("RESULT:")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
