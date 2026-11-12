
from crewai import Crew, Process

from crewai_system.agents import researcher, summarizer
from crewai_system.tasks import research_task, summarization_task


# Create the CrewAI workflow
research_crew = Crew(
    agents=[
        researcher,
        summarizer,
    ],
    tasks=[
        research_task,
        summarization_task,
    ],
    process=Process.sequential,
    verbose=True,
)
