import pytest

from tools import web_search_tool

def test_web_search_rejects_empty_query():
    result = web_search_tool.web_search("")
    assert result == "Error: Search query cannot be empty."

def test_web_search_rejects_whitespace_query():
    result = web_search_tool.web_search("   ")
    assert result == "Error: Search query cannot be empty."

def test_web_search_success(monkeypatch):
    class MockDDGS:
        def text(self, query, max_results):
            assert query == "Python testing"
            assert max_results == 5
            return [{
                "title": "Python Testing Guide",
                "body": "A guide to testing Python applications.",
                "href": "https://example.com/python-testing"
            }]

    monkeypatch.setattr(web_search_tool, "DDGS", MockDDGS)
    result = web_search_tool.web_search("Python testing")

    assert "Python Testing Guide" in result
    assert "A guide to testing Python applications." in result
    assert "https://example.com/python-testing" in result

def test_web_search_handles_no_results(monkeypatch):
    class MockDDGS:
        def text(self, query, max_results):
            return []

    monkeypatch.setattr(web_search_tool, "DDGS", MockDDGS)
    result = web_search_tool.web_search("unknown query")

    assert result == "No search results found for this query."

def test_web_search_handles_provider_error(monkeypatch):
    class MockDDGS:
        def text(self, query, max_results):
            raise web_search_tool.DDGSException("Provider unavailable")

    monkeypatch.setattr(web_search_tool, "DDGS", MockDDGS)
    result = web_search_tool.web_search("Python")

    assert "Search provider error" in result

def test_web_search_handles_unexpected_error(monkeypatch):
    class MockDDGS:
        def text(self, query, max_results):
            raise RuntimeError("Unexpected failure")

    monkeypatch.setattr(web_search_tool, "DDGS", MockDDGS)
    result = web_search_tool.web_search("Python")

    assert "Unexpected search error" in result

@pytest.mark.parametrize("max_results", [0, -1, 2.5, "5", None])
def test_web_search_rejects_invalid_max_results(max_results):
    result = web_search_tool.web_search(
        "Python testing",
        max_results=max_results
    )

    assert "max_results must be a positive integer" in result


@pytest.mark.parametrize("query", [None, 123, [], {}])
def test_web_search_rejects_invalid_query_type(query):
    result = web_search_tool.web_search(query)

    assert "Search query must be a non-empty string" in result


def test_web_search_rejects_boolean_max_results():
    result = web_search_tool.web_search(
        "Python testing",
        max_results=True
    )

    assert "max_results must be a positive integer" in result
