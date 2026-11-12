from ddgs import DDGS
from ddgs.exceptions import DDGSException


def web_search(query: str, max_results: int = 5) -> str:
    """Search the internet and return formatted results."""

    if not query or not query.strip():
        return "Error: Search query cannot be empty."

    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        if not results:
            return "No search results found for this query."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            formatted_results.append(
                f"""
Result {index}
Title: {result.get('title', 'No title')}
Description: {result.get('body', 'No description')}
URL: {result.get('href', 'No URL')}
"""
            )

        return "\n".join(formatted_results)

    except DDGSException as error:
        return f"Search provider error: {error}"

    except Exception as error:
        return f"Unexpected search error: {error}"

