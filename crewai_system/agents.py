
import truststore
truststore.inject_into_ssl()

import os

from dotenv import load_dotenv
from crewai import Agent, LLM

from crewai_system.tools import WebSearchTool


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Check your .env file.")


# Configure Groq LLM
llm = LLM(
    model="openai/openai/gpt-oss-120b",
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)


# Initialize custom internet search tool
web_search_tool = WebSearchTool()


# Research Agent
researcher = Agent(
    role="Internet Research Specialist",
    goal=(
        "Research {topic} using reliable internet search results "
        "and collect useful facts and source URLs."
    ),
    backstory=(
        "You are an experienced internet researcher. "
        "You investigate topics carefully, collect relevant "
        "information, and avoid unsupported claims."
    ),
    tools=[web_search_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=4,
)

# Summarizer Agent
summarizer = Agent(
    role="Research Report Summarizer",
    goal=(
        "Analyze the research findings about {topic} and produce "
        "a clear, accurate, well-structured research report."
    ),
    backstory=(
        "You are an expert research analyst and technical writer. "
        "You transform collected research findings into concise, "
        "easy-to-understand reports. You preserve important facts, "
        "include source URLs, and never invent information."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


