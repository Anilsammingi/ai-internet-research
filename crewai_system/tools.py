
import re
import truststore

truststore.inject_into_ssl()

from typing import Type

from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from tools.web_search_tool import web_search as internet_search
from tools.webpage_reader import extract_webpage


class WebSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The internet search query to investigate."
    )


class WebSearchTool(BaseTool):
    name: str = "Internet Search and Webpage Reader"

    description: str = (
        "Search the internet, retrieve relevant webpages, "
        "and return extracted content with source titles and URLs."
    )

    args_schema: Type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:

        search_results = internet_search(query, max_results=3)

        # Extract title, description and URL from search results.
        pattern = (
            r"Result \d+\s*\n"
            r"Title:\s*(.*?)\n"
            r"Description:\s*(.*?)\n"
            r"URL:\s*(.*?)\s*"
            r"(?=\nResult \d+|\Z)"
        )

        matches = re.findall(pattern, search_results, re.DOTALL)

        if not matches:
            return search_results

        research_output = []

        for index, (title, description, url) in enumerate(
            matches[:2], start=1
        ):
            title = title.strip()
            description = description.strip()
            url = url.strip()

            research_output.append(
                f"\n{'=' * 60}\n"
                f"Source {index}\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Search Description: {description}\n"
            )

            # Retrieve and extract webpage content.
            webpage_content = extract_webpage(
                url,
                max_chars=1200
            )

            research_output.append(
                f"Webpage Content:\n{webpage_content}\n"
            )

        return "\n".join(research_output)
