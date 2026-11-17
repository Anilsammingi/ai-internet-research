from ddgs import DDGS
from ddgs.exceptions import DDGSException


def _format_value(value, default, max_length):
    """Format a search result field safely."""

    if not isinstance(value, str) or not value.strip():
        return default

    value = value.strip()

    if len(value) > max_length:
        return value[:max_length] + "..."

    return value


def web_search(query: str, max_results: int = 5) -> str:
    """Search the internet and return formatted results."""

    if not isinstance(query, str):
        return "Error: Search query must be a non-empty string."

    if not query.strip():
        return "Error: Search query cannot be empty."

    if (
        not isinstance(max_results, int)
        or isinstance(max_results, bool)
        or max_results <= 0
    ):
        return "Error: max_results must be a positive integer."

    query = query.strip()

    try:
        results = DDGS().text(
            query,
            max_results=max_results
        )

        if not results:
            return "No search results found for this query."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            if not isinstance(result, dict):
                continue

            title = _format_value(
                result.get("title"),
                "No title",
                300
            )

            description = _format_value(
                result.get("body"),
                "No description",
                1500
            )

            url = _format_value(
                result.get("href"),
                "No URL",
                2000
            )

            formatted_results.append(
                f"""
Result {index}
Title: {title}
Description: {description}
URL: {url}
"""
            )

        if not formatted_results:
            return "No usable search results found for this query."

        return "\n".join(formatted_results)

    except DDGSException as error:
        return f"Search provider error: {error}"

    except Exception as error:
        return f"Unexpected search error: {error}"
