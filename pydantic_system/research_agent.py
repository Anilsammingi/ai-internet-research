import truststore
truststore.inject_into_ssl()
import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from tools.web_search_tool import web_search as internet_search


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Check your .env file.")


# Configure Groq
provider = OpenAIProvider(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)

model = OpenAIChatModel(
    "openai/gpt-oss-120b",
    provider=provider,
)


# Create the PydanticAI agent
research_agent = Agent(
    model,
    instructions="""
    You are an expert internet research assistant.

    When a user asks a research question:
    1. Use the search_web tool to find relevant information.
    2. Analyze the search results carefully.
    3. Summarize the most useful findings.
    4. Include source URLs when available.
    5. Clearly mention when information is uncertain.
    6. Never invent facts or sources.
    """,
)


# Register our custom internet search tool
@research_agent.tool_plain
def search_web(query: str) -> str:
    """Search the internet using our custom search tool."""
    return internet_search(query, max_results=5)

