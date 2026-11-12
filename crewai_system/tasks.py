
from crewai import Task

from crewai_system.agents import researcher, summarizer


# Research Task
research_task = Task(
    description=(
        "Research the topic: {topic} using the Internet Search and "
        "Webpage Reader tool.\n\n"

        "Research instructions:\n"
        "1. Perform no more than 3 focused searches. Avoid repeating queries.\n"
        "2. Prefer authoritative sources and recent information relevant to the topic.\n"
        "3. The tool retrieves and extracts webpage content. Use that content "
        "as the primary evidence when extraction succeeds.\n"
        "4. Use search descriptions only as supporting context when full-page "
        "extraction is unavailable.\n"
        "5. Preserve exact source titles and URLs.\n"
        "6. Do not treat failed, blocked, or empty webpage extractions as evidence.\n"
        "7. Do not invent facts, statistics, dates, or URLs.\n"
        "8. Clearly distinguish verified findings from uncertainties.\n"
        "9. Keep the research concise and avoid unnecessary detail.\n\n"

        "Return findings using this structure:\n"
        "A. Topic overview\n"
        "B. Key findings\n"
        "C. Important developments\n"
        "D. Applications, benefits, and risks\n"
        "E. Source references (exact titles and URLs)\n"
        "F. Information gaps and uncertainties"
    ),
    expected_output=(
        "A concise research collection about {topic}, based on successfully "
        "extracted webpage content where available, with exact source titles "
        "and URLs and clearly identified uncertainties."
    ),
    agent=researcher,
)


# Summarization Task
summarization_task = Task(
    description=(
        "Prepare a clear and accurate research report about {topic}, "
        "using the Research Task output as your primary source.\n\n"

        "Instructions:\n"
        "1. Summarize the research findings without changing their meaning.\n"
        "2. Preserve exact source titles and URLs.\n"
        "3. Include source references alongside relevant findings.\n"
        "4. Do not invent facts, statistics, dates, or citations.\n"
        "5. Clearly identify unsupported claims and information gaps.\n"
        "6. Do not introduce unrelated information from your own knowledge.\n"
        "7. Keep the report concise and avoid repeating information.\n\n"

        "Use this report structure:\n"
        "1. Introduction\n"
        "2. Key Findings\n"
        "3. Important Developments\n"
        "4. Applications and Benefits\n"
        "5. Risks and Challenges\n"
        "6. Conclusion\n"
        "7. Source References"
    ),
    expected_output=(
        "A concise, structured research report about {topic}, including "
        "key findings, developments, applications, benefits, risks, "
        "conclusion, and exact source titles and URLs."
    ),
    agent=summarizer,
    context=[research_task],
)



